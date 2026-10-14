# Title block

Every page opens with language, not metrics: eyebrow, title, one-line
subhead, rule. Rows 3–6 or 1–4 — the shell table's column; the rule
sits directly under the subhead, never a blank row between.

```python
# build this once per page, on that page's handle (home, scenarios, …);
# the structural wrapper makes the three lines read as one unit.
tb = home.add_container()
tb.set_frame(1, 3, 13, 3)                    # (1, 1, 13, 3) at rows 1–4
tb.set_column_density('high')
tb.set_padding(False)
tb.set_gap(False)
tb.set_background_color(None)
tb.set_border(None)
eyebrow = tb.add_text('<p class="p-small"><span style="color: ' + PRIMARY + '"><CONTEXT LINE, CAPS></span></p>')
eyebrow.set_frame(1, 1, 24, 1)
title = tb.add_text('### <Page title>')
title.set_frame(1, 2, 24, 1)
sub = tb.add_text('<p class="p-small"><span style="color: ' + MUTED + '"><One sentence: the job this page does.></span></p>')
sub.set_frame(1, 3, 24, 1)
rule = home.add_divider()          # the rule stays on the page, full width
rule.set_frame(1, 6, 24, 1)                  # (1, 4, 24, 1) at rows 1–4
rule.set_color(HAIRLINE)
```

## Chip

A small status tag — beside the title, on a card's label row, or naming a
capability ("LIVE · SNOWFLAKE").

```python
chip = home.add_text('<p class="p-small" style="text-align: center"><span style="color: ' + PRIMARY + '"><Status></span></p>')
chip.set_frame(21, 3, 4, 1)          # on the page, beside the wrapper; (21, 1, 4, 1) at rows 1–4
chip.set_vertical_align('middle')
chip.set_padding(False)
chip.set_background_color(TINT)
chip.set_border(sigma.border.solid(width=1, color=EDGE, radius='pill'))
```

- A chip whose meaning is fixed at build time takes the semantic pair
  instead — span color and fill `'#008236'` on `'#dcfce7'` (good),
  `'#c10007'` on `'#ffe2e2'` (bad), `'#bb4d00'` on `'#fef3c6'` (warn),
  border `None`; a chip bound to a column cannot vary its fill, so it
  stays `TINT`.

- Titles are imperatives or noun phrases in sentence case ("Build the
  plan", "Pipeline review"); the eyebrow carries period or program context
  in CAPS; the subhead says what the reader does here. An app's Overview,
  or the first page under a sidebar rail, greets instead: `tb.add_text('### Welcome back, {{Name}}', formulas={'Name': sigma.formula.current_user_first_name()})`.
- **Breadcrumb** (multi-page apps, above the eyebrow or replacing it):
  `crumb = home.add_text('<p class="p-small"><span style="color: ' + MUTED + '">Overview  ›  </span><span style="color: ' + BODY + '">Scenarios</span></p>')`
  — trail muted, current page body-ink, never a link hue.
- **Dynamic chip**: a small button with a formula label and no action —
  `chip = home.add_button('{{Status}}', formulas={'Status': sigma.formula.max(base.get_column_by_name('<STATUS>'))})`
  · solid · pill · small · fill `TINT` · font `PRIMARY` — live status
  ("Draft", "Last updated…") beside the title. An app's count chip binds
  the input table: `'{{n}} pending'` with
  `{'n': sigma.formula.count_if(sigma.formula.eq(it.get_column_by_name('Status'), sigma.formula.const_text('Pending')))}`.
- Columns 14–24 beside the title are reserved for page actions — rows per
  `blocks/buttons.md`.
- When the page's KPIs need a sentence to relate them, follow
  the title block with an insight callout (`blocks/insight.md`), not a
  longer subhead.

## Progress rail

Which step of an ordered flow the reader is on — intake → review → approve.
Navigation says where you can go; this says where you are. One structural
band under the title rule, so the page body starts at `y = 9` (7 at rows 1–4).

```python
prog = home.add_container()
prog.set_frame(1, 7, 24, 2)
prog.set_column_density('high')
prog.set_padding(False)
prog.set_background_color(None)
prog.set_border(None)
s1 = prog.add_text('<p class="p-small"><span style="color: ' + PRIMARY + '">➊  Commentary</span></p>')
s1.set_frame(1, 1, 7, 2)
s1.set_vertical_align('middle')
d1 = prog.add_divider('vertical')
d1.set_frame(8, 1, 1, 2)
d1.set_color(HAIRLINE)
# ➋ at (9,1,7,2), divider at (16,1,1,2), ➌ at (17,1,8,2) — the same calls
```

- Three or four steps; past that it is navigation, not a rail. Each page
  rebuilds it, and the **only** thing that changes is which step carries
  `PRIMARY` — the rest stay `MUTED`.
