#!/usr/bin/env python3
"""Check a quickstart program, or a step-4 element dump, before it costs a call.

Run it — do not read it. It catches the two classes of failure that otherwise
only surface remotely: constructs the Code Mode dialect rejects (a typecheck
error, nothing runs, the whole program is resubmitted) and geometry mistakes
(frames that overlap and silently relocate elements, children that overrun
their container, blank rows between bands).

    python3 scripts/check.py program.py     # a program, before build_workbook
    python3 scripts/check.py dump.txt       # the step-4 host|id|name|frame dump
    cat program.py | python3 scripts/check.py -
    python3 scripts/check.py --fragment snippet.py   # one block, not a whole program

Findings are `ERROR` (this will not build, or will build wrong) and `WARN`
(look at it). Exit status is 1 when anything is an ERROR. A clean run is not a
promise the build succeeds — it is the local half of the check, and step 5's
screenshots are still the other half.
"""

import ast
import builtins
import io
import json
import re
import sys
import tokenize
from pathlib import Path

DATA = Path(__file__).with_name("design-system.json")

# The builtins a program may call (SKILL.md, "Program rules"). Anything else
# that resolves to a Python builtin is a construct the runtime does not expose.
ALLOWED_BUILTINS = {
    "print", "len", "int", "any", "enumerate", "zip", "range", "list", "reversed",
    "sorted", "min", "max", "str", "isinstance", "type", "datetime", "timedelta", "RuntimeError",
    "Exception", "ValueError", "TypeError", "KeyError", "IndexError", "ZeroDivisionError",
}

# `add_*` calls that do not make a framed element.
NON_ELEMENT = {
    "add_column", "add_editable_column", "add_formula_column",
    "add_conditional_format", "add_source", "add_system_columns",
    "add_pivot_row", "add_pivot_column", "add_pivot_value", "add_ref_band",
    "add_metric", "add_formula", "add_trendline", "add_ref_line", "add_tab",
    "add_tables", "add_action", "add_ai_column", "add_folder", "add_field",
    "add_relationship", "add_source_column",
}
OVERLAY = {"add_popover", "add_modal", "add_drawer"}
PANEL = {"add_header", "add_sidebar"}
PAGE = {"add_page"}
# Hosts whose inner grid has exactly as many rows as their own frame spans.
CONTAINER = {
    "add_container", "add_tabbed_container", "add_single_row_container",
    "add_repeater", "add_form",
}

# add_* -> the row in design-system.json's element_minimums
MINIMUM_FOR = {
    "add_table": "Table", "add_input_table": "Input table",
    "add_linked_input_table": "Input table", "add_pivot_table": "Pivot",
    "add_kpi": "KPI", "add_text": "Text", "add_button": "Button",
    "add_divider": "Divider", "add_container": "Container",
    "add_tabbed_container": "Container", "add_single_row_container": "Container",
    "add_repeater": "Repeater", "add_navigation": "Navigation",
    "add_chat": "Chat", "add_form": "Form", "add_point_map": "Map",
    "add_region_map": "Map",
}

# Findings that need a whole program to mean anything. A block in blocks/ is a
# fragment: its `src`, `sec` and `y` come from the program that pastes it in,
# and it shows one element of a band rather than the finished band.
FRAGMENT_SUPPRESSED = {
    "undefined-name", "missing-token-block", "no-frame", "blank-rows",
    "trailing-empty-row", "action-below-fold",
}

PLACEHOLDER_FORMAT = re.compile(r"\{\{[^}]*\|[^}]*\}\}")
SPAN_FONT = re.compile(r"<span[^>]*font-(size|family)", re.I)
HTML_ENTITY = re.compile(r"&(lt|gt|amp|quot|nbsp|#39);")
DUMP_LINE = re.compile(r"^\s*([^|]+)\|([^|]*)\|([^|]*)\|\s*\(?\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*\)?\s*$")


class Finding:
    def __init__(self, severity, line, code, message):
        self.severity = severity
        self.line = line
        self.code = code
        self.message = message

    def __str__(self):
        where = f"line {self.line}" if self.line else "-"
        return f"{self.severity:5s} {where:>9s}  {self.code}: {self.message}"


class Element:
    def __init__(self, var, kind, host, line):
        self.var = var
        self.kind = kind
        self.host = host
        self.line = line
        self.frame = None
        self.frame_line = None
        self.unfoldable = False
        self.density = None


def load_design_system():
    try:
        return json.loads(DATA.read_text())
    except (OSError, ValueError):
        return None


# ---------------------------------------------------------------- dialect ---


def check_dialect(tree, source, findings):
    assigned = collect_assigned(tree)
    nullable = collect_nullable(tree)
    dict_names = collect_dicts(tree)
    tokens_used = set()
    tokens_assigned = set()
    design = load_design_system()
    token_names = set(design["tokens"]) if design else set()
    type_names = collect_type_names(tree)
    guarded = collect_guarded_calls(tree)

    for node in ast.walk(tree):
        line = getattr(node, "lineno", None)

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            findings.append(Finding("WARN", line, "def-unchecked",
                "frames inside a `def` are not folded here, and the runtime needs "
                "every parameter and the return annotated — inline the calls"))
            parameters = node.args.posonlyargs + node.args.args + node.args.kwonlyargs
            if node.returns is None or any(p.annotation is None for p in parameters):
                findings.append(Finding("ERROR", line, "def-unannotated",
                    "a `def` needs every parameter and its return annotated"))
        elif isinstance(node, ast.ClassDef):
            findings.append(Finding("ERROR", line, "no-class", "`class` is not in the dialect"))
        elif isinstance(node, ast.For) and node.orelse:
            findings.append(Finding("ERROR", line, "no-for-else",
                "`else` on a `for` loop is not in the dialect"))
        elif isinstance(node, ast.Lambda):
            findings.append(Finding("ERROR", line, "no-lambda", "`lambda` is not in the dialect"))
        elif isinstance(node, (ast.While,)):
            findings.append(Finding("ERROR", line, "no-while",
                "`while` is not in the dialect — a `for` over a list is"))
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            findings.append(Finding("WARN", line, "needless-import",
                "no import is needed — `sigma` is already bound"))
        elif isinstance(node, ast.Try):
            findings.append(Finding("WARN", line, "unsupported-statement",
                "`try`/`except` runs, but no block shows it — check the SDK docs before relying on it"))
        elif isinstance(node, (ast.With, ast.Assert)):
            findings.append(Finding("ERROR", line, "no-with-assert",
                f"`{type(node).__name__.lower()}` is not in the dialect"))
        elif isinstance(node, ast.JoinedStr):
            if "{{" in (ast.get_source_segment(source, node) or ""):
                findings.append(Finding("ERROR", line, "no-fstring",
                    "an f-string collapses `{{placeholder}}` to `{placeholder}` and it "
                    "stops binding — build the string with `+`"))

        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Pow, ast.LShift, ast.RShift)):
            findings.append(Finding("ERROR", line, "no-operator",
                f"`{'**' if isinstance(node.op, ast.Pow) else '<<' if isinstance(node.op, ast.LShift) else '>>'}` is not in the dialect"))

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
            findings.append(Finding("ERROR", line, "no-operator", "unary `+` is not in the dialect"))

        if isinstance(node, ast.Constant) and isinstance(node.value, bytes):
            findings.append(Finding("ERROR", line, "no-bytes", "bytes literals are not in the dialect"))

        if isinstance(node, ast.AnnAssign) and isinstance(node.annotation, ast.Name) \
                and node.annotation.id in ("list", "dict", "tuple"):
            findings.append(Finding("ERROR", line, "bare-annotation",
                f"`{node.annotation.id}` needs an element type "
                f"(`x: {node.annotation.id}[str] = ...`)"))

        if isinstance(node, ast.Subscript):
            if (
                isinstance(node.slice, ast.Constant)
                and isinstance(node.slice.value, str)
                and not (isinstance(node.value, ast.Name) and node.value.id in dict_names)
            ):
                findings.append(Finding("ERROR", line, "handle-not-dict",
                    f"handles are objects — call it "
                    f"(`{ast.unparse(node.value)}({node.slice.value!r})`), "
                    f"never `[{node.slice.value!r}]`"))

        if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            if isinstance(node, (ast.SetComp, ast.GeneratorExp)):
                findings.append(Finding("ERROR", line, "list-comprehension-only",
                    "only `[... for x in ...]` and `{k: v for x in ...}` parse — "
                    "a generator or set comprehension does not"))

        if isinstance(node, ast.Set):
            findings.append(Finding("ERROR", line, "no-set", "set literals are not in the dialect"))

        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "format"
            and isinstance(node.func.value, ast.Constant)
            and isinstance(node.func.value.value, str)
            and "{{" in node.func.value.value
        ):
            findings.append(Finding("ERROR", line, "no-format",
                "`.format` collapses `{{placeholder}}` — build the string with `+`"))

        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if PLACEHOLDER_FORMAT.search(node.value):
                findings.append(Finding("ERROR", line, "placeholder-format-spec",
                    "a `{{placeholder}}` takes no format spec — it renders the literal "
                    "string; pre-format the value instead (blocks/formulas.md)"))
            entity = HTML_ENTITY.search(node.value)
            if entity:
                findings.append(Finding("ERROR", line, "html-entity",
                    f"`{entity.group(0)}` renders as those characters on the page — "
                    "a span needs literal < and >; this is what escaping on the way "
                    "into the tool argument looks like"))
            if SPAN_FONT.search(node.value):
                findings.append(Finding("WARN", line, "span-font",
                    "a span sets color only — the type table fixes size, not `font-size`"))

        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id in token_names:
                tokens_used.add(node.id)
            if (
                id(node) not in type_names
                and node.id not in assigned
                and node.id not in ALLOWED_BUILTINS
                and node.id != "sigma"
                and not is_sdk_class(node.id)
            ):
                if hasattr(builtins, node.id):
                    findings.append(Finding("ERROR", line, "builtin-not-exposed",
                        f"`{node.id}` is not one of the exposed builtins"
                        + (" — aggregation is `sigma.formula.sum`" if node.id == "sum" else "")))
                else:
                    findings.append(Finding("ERROR", line, "undefined-name",
                        f"`{node.id}` is never assigned — a NameError at runtime"))

        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.id in token_names:
            tokens_assigned.add(node.id)

        if isinstance(node, ast.Call):
            check_call(node, line, findings)
            if id(node) not in guarded:
                check_nullable_argument(node, line, nullable, findings)

    if token_names:
        missing = sorted(tokens_used - tokens_assigned)
        if missing:
            findings.append(Finding("ERROR", None, "missing-token-block",
                "the opening token block is missing these: " + ", ".join(missing)
                + " — every call for the workbook opens with all twelve "
                  "(scripts/theme.py prints them)"))

def check_call(node, line, findings):
    func = node.func
    name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", None)

    if isinstance(func, ast.Attribute):
        chain = ast.unparse(func)
        if chain.startswith("sigma.data.sql"):
            findings.append(Finding("ERROR", line, "no-in-program-sql",
                "a program runs no SQL — resolve values with the `query` tool in step 3"))
        if name in {"help", "dir"}:
            findings.append(Finding("ERROR", line, "no-probe", "probes are rejected"))

    if name in {"help", "dir"} and not isinstance(func, ast.Attribute):
        findings.append(Finding("ERROR", line, "no-probe",
            "probes (`help()`, `dir()`) are rejected — read the SDK docs instead"))

    if name == "add_column" and len(node.args) >= 2:
        second = node.args[1]
        if isinstance(second, ast.Call) and isinstance(second.func, ast.Attribute):
            if second.func.attr in {"get_column_by_name", "column"}:
                findings.append(Finding("ERROR", line, "add-column-needs-formula",
                    "`add_column` takes a Formula, not a column — wrap it "
                    "(`sigma.formula.text(col)`, `number`, `date`)"))

    if name == "set_surface_color" and node.args:
        value = literal_str(node.args[0])
        if value and value.lower() in {"#ffffff", "#fff", "white"}:
            findings.append(Finding("ERROR", line, "white-surface",
                "a white surface color makes every input lose its border — use '#8c8c8c'"))

    if name == "set_comparison" and len(node.args) == 1 and is_none(node.args[0]):
        findings.append(Finding("WARN", line, "kpi-without-context",
            "a KPI with no comparison leaves a visible gap and tells the reader "
            "nothing — give it a comparison column or a prior period"))

    if name == "duplicate":
        findings.append(Finding("WARN", line, "no-duplicate",
            "`duplicate()` drops the copy a row below the original and keeps the "
            "doubled height — build the second element the long way"))

    if name and name.endswith("_color"):
        for argument in node.args:
            if (
                isinstance(argument, ast.Call)
                and isinstance(argument.func, ast.Attribute)
                and argument.func.attr == "highlight_color"
            ):
                findings.append(Finding("ERROR", line, "highlight-as-color",
                    "the highlight is read to pick a hue row, never passed as a "
                    "color — use SERIES, SERIES_MID, SERIES_GREY or the ramp"))


SDK_CAPS_CLASSES = {"KPI"}


def is_sdk_class(name):
    """`Container`, `ListControl`, `SingleRowContainer` — the classes an
    `isinstance` narrow names are bound by the runtime, not by the program.
    A token is ALL_CAPS, so it never matches here — except `KPI`, the one
    all-caps class."""
    return name in SDK_CAPS_CLASSES or (
        name[:1].isupper() and any(character.islower() for character in name))


def literal_str(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def is_none(node):
    return isinstance(node, ast.Constant) and node.value is None


def collect_nullable(tree):
    """Names that are assigned a bare `None` anywhere in the program."""
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and is_none(node.value):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
    return names


def check_nullable_argument(node, line, nullable, findings):
    """`t = None` then reassigned in a loop types `t` as `None | Source`.

    The typecheck rejects it even when every path assigns something — seed the
    variable from the first real value instead of from None.
    """
    if not isinstance(node.func, ast.Attribute) or not node.func.attr.startswith("add_"):
        return
    for argument in node.args:
        if isinstance(argument, ast.Name) and argument.id in nullable:
            findings.append(Finding("WARN", line, "nullable-argument",
                f"`{argument.id}` is assigned `None` somewhere, so it can type as "
                f"`None | ...` (a loop reassigning it does) and `{node.func.attr}` "
                "rejects that — seed it from the first real value instead"))


def collect_type_names(tree):
    """Names used as a type — in annotations and as `isinstance`'s second argument."""
    exempt = set()

    def mark(expr):
        for inner in ast.walk(expr):
            if isinstance(inner, ast.Name):
                exempt.add(id(inner))

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for argument in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
                if argument.annotation:
                    mark(argument.annotation)
            if node.returns:
                mark(node.returns)
        elif isinstance(node, ast.AnnAssign):
            mark(node.annotation)
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "isinstance"
            and len(node.args) == 2
        ):
            mark(node.args[1])
    return exempt


def collect_guarded_calls(tree):
    """Calls inside `if x is not None:` (or `if x:`) — `x` is narrowed there."""
    guarded = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        test = node.test
        narrows = (
            isinstance(test, ast.Compare)
            and len(test.ops) == 1
            and isinstance(test.ops[0], ast.IsNot)
            and is_none(test.comparators[0])
        ) or isinstance(test, ast.Name)
        if narrows:
            for statement in node.body:
                for inner in ast.walk(statement):
                    if isinstance(inner, ast.Call):
                        guarded.add(id(inner))
    return guarded


def collect_assigned(tree):
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            names.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.arg):
            names.add(node.arg)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            names.add(node.name)
    return names


def collect_dicts(tree):
    """Names assigned a dict literal or dict comprehension — `x['k']` is real there."""
    names = set()
    assigns = [n for n in ast.walk(tree) if isinstance(n, ast.Assign)]
    changed = True
    while changed:
        changed = False
        for node in assigns:
            is_dict = isinstance(node.value, (ast.Dict, ast.DictComp)) \
                or (isinstance(node.value, ast.Name) and node.value.id in names)
            if not is_dict:
                continue
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id not in names:
                    names.add(target.id)
                    changed = True
    return names


# ----------------------------------------------------------------- layout ---


class LayoutModel:
    """Elements, their hosts, and their frames, folded from the program text."""

    def __init__(self):
        self.elements = {}
        self.order = []
        self.ints = {}

    def add(self, element):
        self.elements[element.var] = element
        self.order.append(element.var)

    def fold(self, node):
        """Best-effort integer value of an expression, or None."""
        if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
            return node.value
        if isinstance(node, ast.Name):
            return self.ints.get(node.id)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            inner = self.fold(node.operand)
            return None if inner is None else -inner
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub)):
            left, right = self.fold(node.left), self.fold(node.right)
            if left is None or right is None:
                return None
            return left + right if isinstance(node.op, ast.Add) else left - right
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            # prev.y() / prev.height() — the y-cursor idiom
            owner = node.func.value
            if isinstance(owner, ast.Name):
                element = self.elements.get(owner.id)
                if element and element.frame:
                    index = {"x": 0, "y": 1, "width": 2, "height": 3}.get(node.func.attr)
                    if index is not None:
                        return element.frame[index]
        return None


def build_layout(tree, findings):
    model = LayoutModel()

    for statement in walk_statements(tree):
        if isinstance(statement, ast.Assign) and len(statement.targets) == 1:
            target = statement.targets[0]
            value = statement.value
            if isinstance(target, ast.Name):
                folded = model.fold(value)
                if folded is not None:
                    model.ints[target.id] = folded
                if isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute):
                    record_element(model, target.id, value, statement.lineno)

        elif isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call):
            call = statement.value
            if (
                isinstance(call.func, ast.Attribute)
                and call.func.attr == "set_column_density"
                and isinstance(call.func.value, ast.Name)
                and call.args
                and isinstance(call.args[0], ast.Constant)
            ):
                element = model.elements.get(call.func.value.id)
                if element:
                    element.density = {"low": 6, "medium": 12, "high": 24}.get(call.args[0].value)
            if isinstance(call.func, ast.Attribute) and call.func.attr == "set_frame":
                owner = call.func.value
                if isinstance(owner, ast.Name):
                    apply_frame(model, owner.id, call, findings)

    return model


def walk_statements(tree):
    """Statements in source order, descending into `for` bodies."""
    for statement in tree.body:
        yield statement
        if isinstance(statement, ast.For):
            for inner in statement.body:
                yield inner


def record_element(model, var, call, line):
    kind = call.func.attr
    if not kind.startswith("add_") or kind in NON_ELEMENT:
        return
    owner = call.func.value
    if isinstance(owner, ast.Name):
        host = owner.id
    else:
        host = ast.unparse(owner)
    if host.startswith("sigma."):
        # `sigma.control.add_list_control(bar, ...)` and friends take their host
        # as the first argument; `sigma.workbook.add_popover(trigger, ...)` makes
        # an overlay page rather than an element on the trigger's host.
        if kind in OVERLAY:
            host = "<overlay>"
        elif call.args and isinstance(call.args[0], ast.Name):
            host = call.args[0].id
        else:
            host = "<workbook>"
    model.add(Element(var, kind, host, line))


def apply_frame(model, var, call, findings):
    element = model.elements.get(var)
    if element is None:
        return
    named = {k.arg: k.value for k in call.keywords}
    order = ["x", "y", "width", "height"]
    arguments = list(call.args) + [named[n] for n in order[len(call.args):] if n in named]
    if len(arguments) != 4:
        findings.append(Finding("ERROR", call.lineno, "frame-arity",
            "set_frame takes four integers (x, y, width, height)"))
        return
    values = [model.fold(argument) for argument in arguments]
    element.frame_line = call.lineno
    if any(value is None for value in values):
        element.unfoldable = True
        return
    element.frame = tuple(values)


def columns_for(model, host):
    element = model.elements.get(host)
    if host == "<overlay>":
        return 12
    if element and element.kind == "add_repeater":
        return 12
    if element and element.kind == "add_container":
        return element.density or 12    # an unset container is 12 columns
    return 24


def check_layout(model, findings):
    design = load_design_system()
    minimums = design["element_minimums"] if design else {}
    grid = design["grid"] if design else {}
    fold_row = grid.get("fold_row", 28)

    by_host = {}
    for var in model.order:
        element = model.elements[var]
        by_host.setdefault(element.host, []).append(element)

    for var in model.order:
        element = model.elements[var]
        if element.kind in OVERLAY | PANEL | PAGE:
            continue
        if element.frame is None and not element.unfoldable:
            findings.append(Finding("WARN", element.line, "no-frame",
                f"`{element.var}` never gets a set_frame — there is no auto height"))
            continue
        if element.frame is None:
            continue

        x, y, width, height = element.frame
        if x < 1 or y < 1:
            findings.append(Finding("ERROR", element.frame_line, "frame-origin",
                f"`{element.var}` starts at ({x}, {y}) — the grid origin is (1, 1)"))
        limit = columns_for(model, element.host)
        if x + width - 1 > limit:
            findings.append(Finding("ERROR", element.frame_line, "off-grid",
                f"`{element.var}` ends at column {x + width - 1}, past the "
                f"{limit}-column grid of its host"))

        row = MINIMUM_FOR.get(element.kind)
        if row and row in minimums:
            min_width, min_height = minimums[row]
            if width < min_width or height < min_height:
                findings.append(Finding("ERROR", element.frame_line, "below-minimum",
                    f"`{element.var}` is {width}x{height}; a {row} clips below "
                    f"{min_width}x{min_height}"))

        if element.kind == "add_button":
            absolute = absolute_y(model, element)
            if absolute is not None and absolute > fold_row:
                findings.append(Finding("WARN", element.frame_line, "action-below-fold",
                    f"`{element.var}` sits at page row {absolute} — a reader never "
                    f"scrolls to act; move its band above row {fold_row}"))

    for host, children in by_host.items():
        framed = [child for child in children if child.frame]
        check_overlaps(host, framed, findings)
        check_host_fit(model, host, framed, findings)


def check_overlaps(host, framed, findings):
    for index, first in enumerate(framed):
        for second in framed[index + 1 :]:
            if rectangles_overlap(first.frame, second.frame):
                findings.append(Finding("ERROR", second.frame_line, "overlapping-frames",
                    f"`{second.var}` overlaps `{first.var}` inside `{host}` — an "
                    "overlapping frame silently relocates the elements already placed"))


def rectangles_overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


def check_host_fit(model, host, framed, findings):
    if not framed:
        return
    grid = (load_design_system() or {}).get("grid", {})
    element = model.elements.get(host)
    bottom = max(child.frame[1] + child.frame[3] - 1 for child in framed)

    if element is not None and element.kind in CONTAINER and element.frame:
        rows = element.frame[3]
        if element.kind == "add_repeater":
            rows = grid.get("repeater_card_rows", 5)
        if bottom > rows:
            findings.append(Finding("ERROR", element.frame_line, "child-overruns-host",
                f"a child of `{host}` ends on row {bottom} but its inner grid has "
                f"{rows} — it grows the host and pushes the bands below it down"))
        elif bottom < rows and not sized_to_something_else(element, rows, grid):
            findings.append(Finding("WARN", element.frame_line, "trailing-empty-row",
                f"`{host}` spans {rows} rows but its last child ends on row "
                f"{bottom} — a reserved row renders as a visible gap"))

    if element is None or element.kind in PAGE:
        for low, high in uncovered_runs(framed):
            findings.append(Finding("WARN", framed[0].frame_line, "blank-rows",
                f"rows {low}-{high} on `{host}` hold nothing — the y-cursor leaves "
                "no gap between bands"))


def sized_to_something_else(element, rows, grid):
    """Hosts the "size a card to its content" rule exempts.

    A full-height column runs the page rather than its contents, a tabbed main
    is sized by the page, and an input table or form is sized by its rows — all
    of them legitimately end well short of their last row. A repeater card is
    not exempt: its template still has to end on row 5.
    """
    if element.kind in {"add_input_table", "add_linked_input_table", "add_form",
                        "add_tabbed_container"}:
        return True
    if element.kind == "add_repeater":
        return False
    return rows > grid.get("band_height_max", 18)


def uncovered_runs(framed):
    """Row spans between the first and last occupied row that nothing sits on.

    Coverage, not pairwise gaps: a chip beside a title, a mosaic's shallow
    cards, and both halves of a split band all overlap in rows by design, and
    walking siblings in y order reads every one of them as a hole.
    """
    covered = set()
    for child in framed:
        _, y, _, height = child.frame
        covered.update(range(y, y + height))
    if not covered:
        return []
    runs, start = [], None
    for row in range(min(covered), max(covered) + 1):
        if row not in covered and start is None:
            start = row
        elif row in covered and start is not None:
            runs.append((start, row - 1))
            start = None
    return runs


def absolute_y(model, element):
    y = element.frame[1]
    host = element.host
    seen = set()
    while host in model.elements and host not in seen:
        seen.add(host)
        parent = model.elements[host]
        if parent.kind in PAGE | PANEL | OVERLAY or parent.frame is None:
            break
        y += parent.frame[1] - 1
        host = parent.host
    return y


# ------------------------------------------------------------------- dump ---


def check_dump(text, findings):
    """The step-4 dump: `host|el.id()|el.name()|el.frame()`, one line each."""
    model = LayoutModel()
    count = 0
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or "|" not in line:
            continue
        match = DUMP_LINE.match(line)
        if not match:
            continue
        host, identifier, name, x, y, width, height = match.groups()
        count += 1
        var = (name.strip() or identifier.strip() or f"row {number}")
        if var in model.elements:
            var = f"{var} ({number})"
        element = Element(var, "add_container", host.strip(), number)
        element.frame = (int(x), int(y), int(width), int(height))
        element.frame_line = number
        model.add(element)

    if not count:
        findings.append(Finding("ERROR", None, "no-dump-rows",
            "no `host|id|name|(x, y, w, h)` rows found"))
        return

    by_host = {}
    for var in model.order:
        element = model.elements[var]
        by_host.setdefault(element.host, []).append(element)

    for host, children in by_host.items():
        check_overlaps(host, children, findings)
        for child in children:
            x, _, width, _ = child.frame
            if x + width - 1 > 24:
                findings.append(Finding("ERROR", child.frame_line, "off-grid",
                    f"`{child.var}` ends at column {x + width - 1}, past 24"))
        ordered = sorted(children, key=lambda child: child.frame[1])
        for previous, following in zip(ordered, ordered[1:]):
            bottom = previous.frame[1] + previous.frame[3] - 1
            if following.frame[1] > bottom + 1:
                findings.append(Finding("WARN", following.frame_line, "blank-rows",
                    f"rows {bottom + 1}-{following.frame[1] - 1} are blank between "
                    f"`{previous.var}` and `{following.var}` under `{host}`"))

    print(f"# read {count} elements across {len(by_host)} hosts", file=sys.stderr)


# ------------------------------------------------------------------- main ---


def looks_like_dump(text):
    rows = [line for line in text.splitlines() if DUMP_LINE.match(line)]
    return len(rows) >= 2 and len(rows) >= len([l for l in text.splitlines() if l.strip()]) // 2


def check_program(source, findings, fragment=False):
    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        findings.append(Finding("ERROR", error.lineno, "syntax",
            f"{error.msg} — `{(error.text or '').strip()}`"))
        return
    check_dialect(tree, source, findings)
    model = build_layout(tree, findings)
    check_layout(model, findings)
    if fragment:
        findings[:] = [f for f in findings if f.code not in FRAGMENT_SUPPRESSED]


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in {"-h", "--help"}:
        print(__doc__)
        return 0

    fragment = "--fragment" in argv
    argv = [a for a in argv if a != "--fragment"]
    if not argv:
        print(__doc__)
        return 0

    target = argv[0]
    if target == "-":
        source = sys.stdin.read()
        label = "<stdin>"
    else:
        path = Path(target)
        if not path.exists():
            print(f"error: no such file: {target}", file=sys.stderr)
            return 2
        source = path.read_text()
        label = path.name

    findings = []
    if looks_like_dump(source):
        check_dump(source, findings)
    else:
        check_program(source, findings, fragment=fragment)

    errors = [f for f in findings if f.severity == "ERROR"]
    warnings = [f for f in findings if f.severity == "WARN"]
    for finding in sorted(findings, key=lambda f: (f.severity != "ERROR", f.line or 0)):
        print(finding)

    if not findings:
        print(f"{label}: clean — no dialect or geometry findings")
    else:
        print(f"\n{label}: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
