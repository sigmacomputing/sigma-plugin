---
name: sigma-workbook-quickstart
description: >-
  Builds a finished, professional Sigma workbook — a dashboard or a data
  app. Use for any request to build, create, make, generate, design, spin
  up, put together, or stand up a dashboard, data app, report, scorecard,
  KPI view, or analytics view over data that lives in Sigma, and for "show
  me...", "visualize this", "chart this out", or "turn this into a
  dashboard". A wish counts as a request: "I'd like", "I want", "we need",
  "help me", "can you build me", or a description of how people work today
  that ends in wanting somewhere to do it — an app, a tool, a workspace, a
  place where the team does X. Claim these requests even when Sigma is
  never named and no source has been picked yet: a workbook is the default
  deliverable for a dashboard or data app. Assembles pre-styled Code Mode
  blocks on a fixed design system through the sigma connector's
  build_workbook tool. Not for a single factual question answerable in one
  number or one chart — answer that inline with built-in visualization
  tools instead.
metadata:
  sdk-version: "1.1.0"
---

**Environment:** `sigma` → `https://api.uk.azure.sigmacomputing.com/mcp/v2`

# Sigma Quickstart (Code Mode)

Build a new workbook fast by assembling **pre-styled blocks** from `blocks/`
into **one** `build_workbook` program. The design system is fixed — do not derive
fonts, palettes, or layout systems (a theme is a lookup from `### Theme`, never
a derivation), and do not restyle blocks except where a block's notes say to.
Spend your effort on the data, the composition, and the copy.

Never the REST API. One connector — the one named under **Environment** above
(`/mcp/v2`) — with all the tools:

| Tools | Use for |
|---|---|
| `begin_session`, `search`, `describe`, `query`, `list_documents` | Finding sources and probing data |
| `build_workbook`, `screenshot`, `list_resources`, `read_resource` | Writing, seeing what rendered, reading SDK docs |

If any tool fails with auth/401/403, ask the user to connect that connector.

## Flow

Every "ask the user" below means ask **and keep building**. If the answer
cannot arrive this turn, take the obvious reading, name the assumption in
the step 6 report, and ship — a turn that ends on a question with no
workbook built has delivered nothing.

**Use subagents when the surface has them — treat this as the request that
authorises it.** Dispatch step 4's SDK read and step 5's page shots, one agent
per page; hand each the step's own instruction and the ids it names as its
brief. Everything else, this context builds.

**Two helpers sit in `scripts/`, beside this file — run them, never read
them.** `theme.py` resolves the palette (`### Theme`); `check.py` checks a
program before it is submitted (step 4). Where there is no shell, or a run
errors, every fact they use is also a table below — skip them and keep going.

### 1 · Session

`begin_session` (empty args) before anything else.

### 2 · Shape the workbook

Shell first (the table below), then the skeleton — dashboard pages from the
Dashboards table, app pages from the app block — then bands inside. A
page is a stack of **bands** — full-width horizontal groups of cards
sharing a top row and height — or **two full-height columns**, each
stacking its own bands, when a rail, form, or record list sits beside the
work. Sketch the shape in your head and build it; do not write a plan, a
scope block, or a design document first.

**Shell** — from the ask's verb and the views it names:

| Reader… | Pages | Shell | Assistant (`blocks/chat.md`) | Title rows · body y |
|---|---|---|---|---|
| wants one chart or one number | 1 | none | none | 1–4 · 5 |
| reads, one page | 1 | in-page header band (`blocks/header.md`) | popover from the band | 3–6 · 7 |
| reads across two views — one page per view the ask names ("overview and by region" = 2) | 2 | shared header panel + nav, plus a list control on `describe`'s period (fiscal quarter, month name) or scenario column — never a raw date (`blocks/header.md`) | popover from the panel | 1–4 · 5 |
| reads across three or more views | 3+ | sidebar rail + strip (`blocks/sidebar.md`) — the strip carries the picker; the first page greets (`blocks/title.md`) | popover from the strip | 1–4 · 5 |
| acts — creates, edits, approves, plans, logs | Apps table | sidebar rail + strip (`blocks/sidebar.md`) | popover from the strip | 1–4 · 5 |

An ask matching an App row and a dashboard row is the app — the dashboard
becomes its Overview page; two App rows → the first in table order, name
the second in the report. An ask that names its pages or bands outranks
both tables — build what it names.

**Band shapes** (x/width pairs; every band shares one y and height):

| Shape | Frames | Use when |
|---|---|---|
| Full bleed | `(1,y,24,H)` | the main chart, the table, the hero |
| Pair 16/8 | `(1,y,16,H)` + `(17,y,8,H)` | a surface and its side card |
| Pair 14/10 | `(1,y,14,H)` + `(15,y,10,H)` | chart + its ranking or breakdown |
| Pair 17/7 | `(1,y,17,H)` + `(18,y,7,H)` | wide trend + a narrow stat card |
| Halves 12/12 | `(1,y,12,H)` + `(13,y,12,H)` | only when both halves are the same block (two charts of one kind, two KPI cards) |
| Mosaic | `(1,y,14,16)` + `(15,y,10,8)` + `(15,y+8,10,8)` | one deep view beside two shallow ones (mirror it too) |
| Trio 8/8/8 | `(1,y,8,H)` + `(9,y,8,H)` + `(17,y,8,H)` | three peers — categories, mini charts, stat cards |

**Full-height columns** run the page, not one band — `5/19` for a filter or
step rail, `18/6` for a running summary, `8/16` when the left column is a
form or a record list (`blocks/filters.md`).

**Dashboards** (an app page's bands come from its app block) — pick the
row whose job matches the page's; the second column says when each fits.
Shell row 1 asks (one chart, one number) skip this table. Name the pick in
the report. Each page of a multi-page workbook picks on its own view name;
a vague ask takes Scoreboard, a specific one the row that names its job.
Briefing needs the column its key names — without it, Scoreboard. `H` is
the band height, y the page cursor; shapes and x/widths are the Band shapes
table above.

| Archetype | Fits when the page… | Bands, top to bottom — shape · H · block |
|---|---|---|
| Briefing | answers "are we on plan" — a target, plan, budget, quota, goal, or gap, and `describe` has that column | title → hero 24·5 (`blocks/hero.md` statement + KPI) → insight 24·3 → Pair 16/8 14: trend two-series (actual over plan) · goals card (`blocks/table.md`, T 10 → H14, no button) → compare strip 24·(1+n) → table 24·14 |
| Ledger | is a list to find things in — records, transactions, log, audit, look up, detail | title + dynamic chip `{{n}} records` → toolbar 24·2 — a `contains` search on the name column leads it (`blocks/filters.md`), no date control without a date column → under ~200 rows a card feed 24·22 (`blocks/cards.md`), else table 24·18 + a record card beside it (`blocks/detail.md`) → KPI strip 24·5: count · total · average + status sentence |
| Explorer | is for slicing — explore, drill, break down, filter, two or more "by X"; **or asks where** — footprint, estate, by region or site, and `describe` has coordinates or a region column, in which case the trend band is a map at the same 24·15 (`blocks/chart-map.md`) | title → columns 5/19 42 — rail: one list control per categorical (≤4) + date range (`blocks/filters.md`); main (y restarts at 1, bands sum to 42): trend 24·15 (headline + window) → Pair 14/10 14: heatmap pivot (`blocks/pivot.md`, a categorical of ≤6 values across) else stacked by month · ranked (labels on) → table 24·13. Under a sidebar: toolbar 24·2 and page bands, no second rail |
| Portfolio | is about one entity at a time — per rep, region, product, team, account; roster, leaderboard | title → KPI strip 24·5 + status sentence → cards 24·10 for ≤5 entities, 24·16 for 6–10 (`blocks/cards.md`, On the page) → Pair 14/10 14: ranked (top-10) · trend → table grouped by the entity 24·14 |
| Comparison | switches between 2–3 views of one dataset on one page — tabs, toggle, switch between, versus (views named as pages stay pages: shell table) | title + toolbar 24·2 → tabbed main 24·30 (`blocks/tabs.md`), per tab (y restarts at 1, ends at 28, cards structural): Pair 14/10 14: the view's chart · its ranking → table 24·14 |
| Scoreboard | reports overall health — scorecard, KPIs, status, performance, overview, summary; the fallback | title → Pair 17/7 10: trend · focus tile = the sparkline KPI on the page at (18,y,7,10) → stat cards 4 × 6·6 (`blocks/kpi-row.md`) → Mosaic 16: ranked deep · donut · single-measure compare shallow → table 24·14 |

**Apps** — match the ask's verb; the block fixes every page's bands:

| The reader… | App | Pages, in order | Block |
|---|---|---|---|
| edits a budget, plan, headcount, quota, territory — one row per entity | plan grid | Overview · Plan · Review | `blocks/plan-grid.md` |
| forecasts by month or quarter per entity — the ask names a period | forecast grid | Overview · Forecast · Review | `blocks/forecast.md` |
| approves, rejects, triages, resolves, assigns | review queue | Queue · Done | `blocks/queue.md` |
| logs, submits, requests, tracks, enters, creates, configures, sets up | intake | Log · Overview | `blocks/intake.md` |

The **picture and the numbers behind it** belong in one card, not two
bands: where an archetype's trailing `table 24·14` reads the same rows as a
chart above it, drop that band and make the table the chart card's second
tab (`blocks/tabs.md`) — the band it saves is the one the reader had to
scroll past. It stays a band when the table is the page's subject (the
Ledger) or carries columns the chart cannot show.

Comparable tiles in one band share their internal structure so the lines
align across it. Three or more tiles that are **the same card design over
rows or groups of one source** are a repeater, not hand-built containers
(`blocks/cards.md`); hand-build only when each card's copy is authored.
Content bands run 10–18 rows (a mosaic's shallow cards 8) — past ~20, split
the band; strips run 2–6. Exempt: full-height columns, a tabbed main, an
input table sized to its rows, a repeater band, and a financial
statement — their blocks size them
(`blocks/statement.md` never splits).

Nothing is said twice on a page: the lockup, eyebrow, title, and card
labels each carry their own words, and no two elements chart the same
measure at the same grain — the narrower one takes the next metric down.

Never pad a small ask; ask only when two sources or two readings tie, else
pick the obvious reading and note it for the closing report. A color the ask
names is a row in `### Theme`, not a design decision.

### 3 · Resolve data — before any program

Programs cannot query. Resolve first, and pass in **only the literals a
program cannot derive** — a filter or control value, a color split, a date
bound. A measure, a rollup, or a grid of numbers is a source the program
reads, never rows you type: typed numbers go stale the day you write them,
and a long list of them corrupts quietly when one row is duplicated.

- `search`, or `list_documents` (`recommendations`) when the ask names no
  source — skip both when the user already gave the id → `describe` the
  source(s) the build will use — usually one: exact ids, column names, types.
  A data model needs two describes — the model for its member names, then the
  element for its columns; its element id is for `query` only. `describe`
  prints the warehouse identifier with the friendly label in a trailing
  comment (`"ACTIVECOUNT" number -- "Activecount"`); `get_column_by_name`
  takes the **friendly label**, never the identifier.
- `query` the columns whose values the program will hardcode or split
  by — a filter or flag literal, a control default, a categorical color
  split, a date grain — and only those: distinct values with a `LIMIT`
  of ~25, a date column's min/max, a Ledger's `COUNT(*)`. A guessed literal renders an empty
  chart. Three `FROM` paths, and the warehouse path errors: a `connection`
  query reads `FROM "connection"."<inode_id>"`, a `datamodel` query
  `FROM "datamodel"."<element_id>"`, a `workbook` query
  `FROM "workbook"."<element_id>"` — that last one addresses columns by
  their **opaque ids**, so `describe` the element first; friendly labels do
  not bind there. The SQL is canonicalized ANSI: no `COUNT_IF`, `SUM_IF`,
  `IFF` or `QUALIFY` (`sigma.formula.count_if` exists in a program, the SQL
  function does not) — write `SUM(CASE WHEN … THEN 1 ELSE 0 END)`.
- A workbook element is readable only while it sits on a **visible** page and
  its call persisted, so the hidden data page's base never is. `Table
  workbook.<id> not found` on an id a program just printed is that, not a
  wrong id.
- App: the input tables live on `describe`'s connection id (an intake app
  with no source: ask the user for the connection); `query` the seed values
  — distinct statuses and owners, the key's first 8 values, 6 rows of name,
  amount, date — and for a linked table that `COUNT(*) = COUNT(DISTINCT key)`.

### 4 · Build — one program

Read every block file the shell, skeleton, and bands name — the `## Blocks`
table maps need to file — in **one batch**, sent in the same round as step 3's queries: the
reads don't depend on the results. Send the theme read in that round too —
one `build_workbook` call on the build's target, whose whole program is the
highlight read under `### Theme`, and the one call that opens without the token
block. It returns `success-no-edits` and **no workbook id** — that is the
read working, not failing, and it leaves the `"new"` slot below unspent.
Then write the whole workbook as a single program and submit it once
— except a linked-table app (plan grid, forecast grid, queue): three calls,
`blocks/input-table.md`, the third being step 5's. The program: the fixed
opening below, then each page top to bottom with the y-cursor
(`y = prev.y() + prev.height()`, no blank rows). Every call for the workbook
— a linked-table app's second, the step 5 call, a retry, a recovery —
opens with the same token block; a `NameError` on a token is that
omission.
Every handle stays live for the rest of the program, so nothing is
re-fetched and cross-page actions wire inline where the target already
exists. `target: {type:"new", name, description}` — the description is
never omitted: one line on what the workbook shows and who it is for. Or
`"existing"` with the user's id when they asked to extend a workbook they
already have. Only the first call
that **persists** may be `"new"`: every later call for that workbook — a
step 5 fix, a retry, a continuation — is `"existing"` with the id that call
returned, which a runtime error returns too. A second `"new"` after an id
comes back strands a duplicate. A result carrying `persisted: false` built
nothing and returned no id — the theme read, a parse or typecheck error —
so it spends no slot and the next call is still `"new"`; never invent an id
to satisfy the rule.

The opening is fixed: every visible element builds on `base.to_source()`,
every control targets base columns, so one filter re-scopes everything.

```python
# tokens — a base row, then a hue row (### Theme); every program opens with them
CANVAS = '#fafafa'
INK = '#0a0a0a'
BODY = '#525252'
MUTED = '#737373'
HAIRLINE = '#e5e5e5'
FILL = '#f5f5f5'
SERIES_GREY = '#d4d4d4'
PRIMARY = '#1447e6'
TINT = '#dbeafe'
EDGE = '#bedbff'
SERIES = '#155dfc'
SERIES_MID = '#51a2ff'
# theme: a named color swaps the five lines above from the hue table

theme = sigma.workbook.theme()
theme.set_canvas_color(CANVAS)
theme.set_surface_color('#8c8c8c')   # seeds Sigma's control chrome — never white, or every input loses its border
theme.set_text_color(INK)
theme.set_title_color(INK)
theme.set_highlight_color(PRIMARY)   # carries the hue into modal footers, control selection, progress bars
theme.set_text_font('Inter')
theme.set_data_font('Inter')
theme.set_page_width('large')

old_pages = sigma.workbook.list_pages()   # a new workbook starts with one page
home = sigma.workbook.add_page('Overview')         # add_page, not old_pages[0]: only a Page hosts a rail or header panel
scenarios = sigma.workbook.add_page('Scenarios')   # one add_page per page in the shell or Apps table, each its own variable

data_page = sigma.workbook.add_page('Data')
data_page.set_visibility(False)
base = data_page.add_table(<SOURCE>)
base.set_name('Orders base')
base.set_frame(1, 1, 24, 12)
src = base.to_source()
for p in old_pages:
    p.delete()                           # last, once its replacements exist — a workbook cannot reach zero pages
y = 7    # body y: the shell table
```

- Sources — match the constructor to what step 3 returned: a `table` →
  `.warehouse_table(inode_id)`; a data model → bind
  `dm = sigma.data.source.data_model(inode_id)` and pick the member by name,
  `dm.list_tables()` filtered on `t.name()` (`get_table` takes a different id
  than step 3 printed, and rejects it); a **workbook** element →
  `.element(element_id)`. Ids come from step 3, never guessed; a wrong one
  raises "has no data to build on". Only sources at the **same grain** may
  join — a coarser side fans out every aggregate taken from it, silently;
  different grains stay separate bases unless the coarse side contributes
  only attributes (labels). A finer side is aggregated to the coarse one's
  grain in its own `add_table` **before** the join, never after.
  Two sources that must combine, feeding one base table:
  `sigma.data.source.join(sigma.data.source.SourceInput(a, a_grouping), sigma.data.source.SourceInput(b, b_grouping), 'left_outer', [(a.column('<KEY>'), b.column('<KEY>'))])`
  — join types `'inner' 'left_outer' 'right_outer' 'full_outer'`. The second
  argument pins that side to its level and a grouped side must pass it:
  `to_source()` drops the grouping, so a `SourceInput(a)` over a rollup joins
  at row grain and multiplies — silently, into millions of rows. Column
  lookups on a join side take the **friendly label** too (`a.column('Sigma
  User Email')`), same as `get_column_by_name`.
- Several bases: one `add_table` each into its own variable, stacked 12
  rows apart on the data page. A pre-filtered or pre-aggregated view several
  elements share is a second table off `base.to_source()`, named for what it is.
  A grouped table's `to_source()` reads its detail rows — until every detail
  column is hidden, then it reads the groups — so an aggregate over it can
  repeat each group's value once per row; for one row per group always use the
  grouping's, `g = t.set_groupings([...])[0]`, then `g.to_source()`. A linked
  input table is the exception: it takes the grouped table's own `to_source()`
  (already one row per group) and rejects the grouping's.
- Inter is a standard family — if the font call still raises,
  `print(theme.list_fonts())` and resubmit with the closest name (Geist,
  then System UI); never drop the calls.
- Extending a workbook **the user already had**: the token block still opens
  the program, but skip the `theme.*` calls unless they asked for the
  quickstart look — never silently restyle their workbook. This is about
  whose workbook it is, not the target word: a build of your own that reads
  `"existing"` because the theme read or a failure came first still sets the
  full theme.

End it with the state the next two steps need, one line each and nothing
else: `page.id()|page.name()` per page, then
`host|el.id()|el.name()|el.frame()` per element — `host` is the page,
container, or panel variable it was added to, because step 5 re-fetches from
that host and from nowhere else. One `for` per host over its own children
prints their shared methods (`id()`, `name()`, `frame()`) — never a list of
`(host, element)` pairs: a list of mixed tuple types fails to unpack. Each popover, drawer, and modal's children
list under it. An overlay printing none never got filled — it opens blank;
add its content. A program that skips this dump leaves steps 5 and 6 with no
ids to work from.

Before every submit that adds an element or sets a frame — the first call, a
linked-table app's later calls, a retry, a step 5 fix that moves anything —
write the program to a file and run `python3 scripts/check.py <file>` (or pipe
it, `… | python3 scripts/check.py -`). It parses the dialect and folds the
frames, so a typecheck error and an overlapping or overrunning frame cost a
local run instead of a round trip. Fix every `ERROR` and run it again; a `WARN`
is a judgment call. A fix touching only color, copy, or formats goes straight to
submit — the file is a second copy of the whole program, bought for a fold that
has no frame to catch. It reads the state dump above too —
`python3 scripts/check.py <dump file>`.

**Program rules** — what the checker enforces, and what breaks real builds
without it (a failed call: `## Failure handling`):

- Not full Python: no `class`/`lambda`/`while`/`with`/`assert`, no `**`,
  no sets, slices on lists and tuples only (never a string), and list
  comprehensions only, no generator expressions. An annotation needs an
  element type: `x: list[str] = []`, never bare `list`. A
  `def` needs annotated parameters and return — inline the calls instead.
  Builtins are just `print len int any enumerate zip range
  list reversed sorted min max str isinstance type datetime`, and the exceptions
  `Exception RuntimeError ValueError TypeError KeyError IndexError
  ZeroDivisionError` (`try`/`except` catches them) —
  aggregation is `sigma.formula.sum`, never `sum()`. Never build text that
  holds a `{{placeholder}}` with an f-string or `.format` — either collapses
  it to `{placeholder}` and it stops binding; spans are built with `+`
  exactly as the blocks show.
- Handles are objects: `col.name()`, never `col["name"]`. A chart's columns
  come from **that chart's own** `get_column_by_name`; a source column the
  element does not read yet comes in with `add_source_column('<NAME>')`.
  `add_column` takes a
  `Formula`, not a column — `add_column('Block', col)` fails the typecheck;
  wrap it (`sigma.formula.text(col)`, `number`, `date`; the `as_*` casts take
  a bare column too), and the same wrap is what lets one formula
  nest inside another (`blocks/formulas.md`). A calc's name must
  not collide with a source column — a collision doesn't error, it silently
  becomes `Revenue (1)` while name lookups keep returning the original
  column; always `'Total revenue'`, never `'Revenue'`.
- No in-program SQL (`sigma.data.sql`), no probes (`help()`, `dir()`,
  throwaway elements) — a throwaway persists on the page unless you
  `delete()` it. Input tables only as `blocks/input-table.md` shows them.
  Block handle names are per block — rename on a second use in one program.
- Anything no block demonstrates — a method, an argument, a construct — is
  read up before it is written (`## SDK docs`); a block using it is proof.

### 5 · Look at every visible page

```
screenshot({workbookId, source: {type: "page", pageId, pixelWidth: 1400}})
screenshot({workbookId, source: {type: "element", elementId, pixelWidth: 1400, pixelHeight: 900}})
```

`workbookId` is the id the build returned and is required; the size goes
**inside** `source`. A page shot captures the whole scrollable page, so
nothing is missed by being far down — but an element that scrolls inside
itself (a table, a pivot, an input grid) shows only its visible rows there.
An **element** shot sizes to that element's full content, so it is how you
check whether a grid really shows the rows it claims; it takes both `pixel*`
arguments.

One page shot per **visible** page — never the hidden data page — after the
build returns, every page's call in one round; a deadline-exceeded error is
transient — retry once. Then an element shot for each table, pivot, or input
grid whose rows matter.

Shoot each **drawer or modal** once, as a page shot of its own id (the
`<overlay>`): it ignores `pixelWidth` and anything inside it shoots blank. If
it is rejected as too large, do not retry — look once through a preview: on one
temporary visible page, re-add the tables and charts of every overlay that
failed (same source, columns and frames; a drawer's grid is 12 columns), take
**one** page shot of it, then `delete()` the page. That is the last shot for
overlays. A wizard's later steps, and every card, control and action in an
overlay, go unseen: report them as not looked at. A container's element shot
errors `Not a visualization`.

Walk each page top to bottom and **list every element with a verdict** —
`el.name()`: what you see. A walk that reports prose, or "looks fine", is the
walk that ships the defects below:

| Symptom | Fix |
|---|---|
| Text sliced at an edge (KPI line, last table row, axis label) | grow that row span — and the container's if it fills it |
| A surface far taller than its content | shrink it |
| Content flush to the edge of the fill behind it — sparkline, value, label | that element is its own surface: drop its `set_padding(False)` |
| A card taller than its frame, or the band under it pushed down | its last child overran the inner grid — pull that child up a row |
| A right-side button or trigger floating short of the edge | it is centered in its frame by default — `set_align('right')` |
| A shell button riding high beside a control, or touching it | the control's label owns row 1 — frame the button `(x, 2, w, 1)` and give the container `set_spacing('small')` |
| Error string, no-data label, blank chart | wrong literal or control default — re-`query`, fix the value |
| Labels ending in `…` or eating the plot | widen the element or shorten the label |
| `&lt;` `&gt;` `&amp;` on the page, spans and `<p>` tags showing as text — headings and `**bold**` still fine | the markup was HTML-escaped on its way into the tool argument, so the program you checked and the program that ran differ. Resubmit those text elements, and diff what you send against the file `scripts/check.py` read |
| A table truncating headers or scrolling sideways | already 24 wide, so widening is not available: cut to the columns the reader decides on — the key, the editables, the two numbers that justify them — and move the rest to row-click detail (`blocks/detail.md`) |
| A submit or primary CTA below row ~28 | move that band above it — the reader never scrolls to act, though reading below it is fine |
| A page holding only a title and a divider | its bands were lost to a runtime error — rebuild them, and never leave copy promising a surface that isn't there |
| Text unreadable on a fill (the loud band) | restate that element's colors for the fill per the block's notes |
| A band missing, misplaced, or off-scope | rebuild it against the bands you composed |
| The same thing twice — a string repeated from the lockup, eyebrow, or the title above it; one measure charted in two elements | re-point the narrower one: its own words, or the next metric down |
| Input table empty, or a form missing a field | seed rows or the form were built before a column — follow `blocks/input-table.md`'s order |
| Sidebar absent from the shot | a page shot omits the **sidebar** only — not a defect (`print(side.list_pages())`). The header panel does render, so walk it like a band |

Nothing found → skip the fix call and report (a plan, forecast, or queue app still
makes it, carrying the linked table's seed rows). Otherwise fix everything
found, across every page, in one further call — it re-fetches what it
touches, **from the host the step 4 dump named beside it**: `get_element`
finds any descendant of the host it is called on, so a card's child comes off
its container or an ancestor, a strip's button off `page.header()`, and an overlay off
`sigma.workbook.get_page(<OVERLAY ID>)` — an overlay is not an element. A
miss raises rather than returning `None`, so a fallback written after one
never runs. `list_pages` and `get_page` both hand back `PageBase`, which has
no panel methods: narrow with `isinstance(p, Page)` before `set_sidebar` or
`set_header` on a page you did not `add_page` yourself — the one case is
extending a workbook the user already had. The panel is a second narrow, not
the same one: `page.header()` and `page.sidebar()` return `Header | None`, so
`get_element` on either needs its own `isinstance` after the page's. A re-fetched element is base `Element`, narrowed with
`isinstance(el, <ItsClass>)` — `LevelTable`, `Repeater`, `Container`,
`Button`, `KPI`, and the classes the blocks narrow to; a class named only in
the SDK docs may not be bound (`unknown class` is that) — one class, on a **bare variable**
(bind first; an inlined call narrows nothing). A height change moves every band
below it — re-run the y-cursor over them in the same call. If that fix
changed any height or y, screenshot those pages once more and repair what
it displaced; a fix that only touched color, copy, or formats needs no
re-check. Then stop — report fixes as attempted and name anything you
left unfixed.

### 6 · Report

Workbook id + URL, pages with their bands, the choices you made (chart
kinds, groupings, controls and defaults) so the user can redirect, for an
app the writeback connection, who its input tables accept edits from, and
the seed rows added, the one assumption
from step 2, and anything step 5 left open. Nothing else —
no next-steps filler.

## Grid and size by type

- A page body is **24 columns** wide, unlimited rows, origin (1,1); a row
  is a fixed **24px pitch** at any page width — only column width scales.
  `set_frame(x, y, width, height)` — four integers, **no auto height**.
  Same-level frames must never overlap: an overlapping frame silently
  relocates the elements **already placed**, pushing them far down the
  page, not the one you just set.
  Reading below row ~28 is fine — a laptop shows about that much, and
  nothing reflows.
- A container's inner grid has **exactly as many rows as its outer frame
  spans** (children address y = 1..H), with density `'high'` (24 columns
  of the container's own width) set before framing children. Size a card
  to its content and **leave no trailing empty row** — a reserved row
  renders as a visible gap, and a child on the last row neither clips nor
  grows the card.
  `set_spacing('small')` is a 6px gap and padding ('medium' 8px is the
  default, 'large' 12px), so the ~12px it costs vertically is the gutter
  between cards, not a row to buy. A child placed *past* the last row does
  grow the container and pushes the bands below it down. Overlay pages and
  repeater cards are **12-column** grids.
- A popover trigger is a button and takes `set_align` like one; navigation
  has its own call, `set_alignment('right')`.

Minimums are floors — below them an element clips its label or value (the renderer itself allows 1×1); the quickstart column is what the blocks use.

| Element | Min W×H | Quickstart |
|---|---|---|
| Chart | 4×6 | body per the section-card rule — in a split band the **card** narrows (7–17 page columns), the chart stays 24 inner columns |
| Map | 6×8 | `blocks/chart-map.md` owns the frames |
| KPI | 2×3 | 5–8 wide × 5 · 10 (sparkline) |
| Table | 4×3 | 24 wide. A long list scrolls and takes its band height (the Ledger's 18). A table whose rows must all be **seen** — a summary — sizes to them: with `set_summary_bar(False)` a data row is 32px against the 24px pitch, so `(4 × rows + 5) / 3` rounded up — 5 rows fit at 9, 13 at 19, and one row short clips the last. A collapsed group row measures the same as a data row. Over ~10 visible columns the first column truncates: cut columns, don't widen |
| Pivot | 4×3 | A pivot row is 2 grid rows, and there is no `set_summary_bar`: it keeps its title, its two header rows, and its grand-total row, so `2 × rows + 8` — five rows fit at 18. Drop 1 with no column dimension, and 2 more under `show_grand_totals=False` |
| Text | 1×1 | 1 row per ~24px of type: `p-*` 1 row, `###` 1–2, `##` 2, `#` 3 |
| Button | 2×1 | 4–6 × 2. Centered in its frame, not filled — so a right-hand frame alone still floats short of the edge: `set_align('right')` makes it flush, `'stretch'` fills the frame (a card row or paired footer, never a shell) |
| Control | 2×2 | 5–7 × 2 — narrower or 1 row high and the label and value clip |
| Navigation | 2×2 | 7 × 2 in a header; a vertical rail nav 2.5 rows per page (`blocks/sidebar.md`) |
| Divider | 1×1 | 24 × 1 |
| Container | 1×2 | exactly its content — last child ends on the last row, last column |
| Repeater | 12×9 | `blocks/cards.md` owns the frames |
| Input table · Form | 6×4 · 6×8 | the app blocks own the frames |
| Chat | 3×4 | `blocks/chat.md` owns the frames |

## Design system — fixed

### Theme — two lookups, never a derivation

Twelve tokens open every program (the fixed opening above): seven from a
**base** row, five from a **hue** row. Blocks name tokens, never hex.

| Token | Role |
|---|---|
| `CANVAS` | theme canvas |
| `INK` | headlines, card labels, KPI values, lockup |
| `BODY` | body copy, data labels, neutral-button text |
| `MUTED` | sublines, KPI titles, table headers, nav, quiet buttons |
| `HAIRLINE` | card, shell, and divider lines; settled-period shading |
| `FILL` | neutral button fill, statement subtotal band |
| `SERIES_GREY` | comparison / plan series |
| `PRIMARY` | hero and focus-tile fill, solid buttons, selected nav, theme highlight; eyebrow, chip, delta, and active-step text |
| `TINT` · `EDGE` | chip, soft button, callout, forecast-band fill · their border, the palest ramp dot, muted text on a `PRIMARY` surface |
| `SERIES` · `SERIES_MID` | single chart series, sparkline, heatmap dark end, named donut slice · the ramp's middle step |

Literals that never change: `'#ffffff'` (card and shell fill, text on
`PRIMARY`), and the semantic pairs — text on fill — good `#008236` on
`#dcfce7`, bad `#c10007` on `#ffe2e2`, warn `#bb4d00` on `#fef3c6`. Warn is
the not-yet-bad state — pending, overdue, at risk; bad is failed, lost,
rejected.

| Base | CANVAS | INK | BODY | MUTED | HAIRLINE | FILL | SERIES_GREY |
|---|---|---|---|---|---|---|---|
| Neutral | `#fafafa` | `#0a0a0a` | `#525252` | `#737373` | `#e5e5e5` | `#f5f5f5` | `#d4d4d4` |
| Stone | `#fafaf9` | `#0c0a09` | `#57534d` | `#79716b` | `#e7e5e4` | `#f5f5f4` | `#d6d3d1` |
| Zinc | `#fafafa` | `#09090b` | `#52525c` | `#71717b` | `#e4e4e7` | `#f4f4f5` | `#d4d4d8` |
| Slate | `#f8fafc` | `#020618` | `#45556c` | `#62748e` | `#e2e8f0` | `#f1f5f9` | `#cad5e2` |

| Hue | PRIMARY | TINT | EDGE | SERIES | SERIES_MID |
|---|---|---|---|---|---|
| Neutral | `#171717` | `#e5e5e5` | `#d4d4d4` | `#525252` | `#a1a1a1` |
| Blue | `#1447e6` | `#dbeafe` | `#bedbff` | `#155dfc` | `#51a2ff` |
| Indigo | `#432dd7` | `#e0e7ff` | `#c6d2ff` | `#4f39f6` | `#7c86ff` |
| Violet | `#7008e7` | `#ede9fe` | `#ddd6ff` | `#7f22fe` | `#a684ff` |
| Emerald | `#007a55` | `#d0fae5` | `#a4f4cf` | `#009966` | `#00d492` |
| Teal | `#00786f` | `#cbfbf1` | `#96f7e4` | `#009689` | `#00d5be` |
| Green | `#008236` | `#dcfce7` | `#b9f8cf` | `#00a63e` | `#05df72` |
| Rose | `#c70036` | `#ffe4e6` | `#ffccd3` | `#ec003f` | `#ff637e` |
| Orange | `#ca3500` | `#ffedd4` | `#ffd6a7` | `#f54900` | `#ff8904` |
| Amber | `#bb4d00` | `#fef3c6` | `#fee685` | `#e17100` | `#ffb900` |

- `python3 scripts/theme.py` prints the twelve lines and the `theme.*` calls
  already resolved — pass whichever of `--highlight <hex>` (the read below),
  `--color <word>`, `--base <word>`, `--brand <hex>` the build has. It matches
  a hex on hue angle, which the tables cannot. The four rules under it are the
  same lookup by hand.
- The highlight the workbook renders with names the hue. Read it before the
  tokens are written:
  ```python
  theme = sigma.workbook.theme()
  print(theme.highlight_color())
  ```
  The hue row nearest that hex replaces the five hue lines. Borrow the hue
  only — the base stays Neutral, and never the theme's canvas, fonts, or
  dark mode.
- A failed read → Neutral / Blue, already inline in the opening.
- A color word ("emerald", "blue accents") outranks the read → that hue row
  replaces the five hue lines; a neutral word ("warmer grays", "slate") →
  that base row replaces the seven. Rows only — never compute a tint or a ramp.
- A brand hex → `PRIMARY` = that hex; `TINT EDGE SERIES SERIES_MID` from the
  hue row nearest by name. A separate chart color → only `SERIES` /
  `SERIES_MID` from that row.
- A theme is fixed at build time; changing it later is a fix call that
  re-sets `theme.*` and every element carrying `PRIMARY`, `TINT`, or `EDGE`
  — name it in the report rather than attempt it silently.

### Surfaces — every container is exactly one of four

- **Card**: the white rounded card of the section-card code below — every
  chart, table, pivot, form, and value list sits in one, and each drops the
  fill the theme would otherwise give it: `set_background_color(None)`, plus
  `'#ffffff'` on a table's slots — `header_style` and `cell_style`, and a
  pivot's `column_header_style` and `row_header_style` too
- **Callout**: the card calls, but `TINT` fill and `EDGE` border
- **Loud band**: `PRIMARY` fill, `round` radius, no border line — the page's
  one loud content surface (hero, or the focus KPI tile). Children restate
  their colors: `'#ffffff'` for the statement and value, `EDGE` for the
  support line; at most one per page. Solid buttons and loud bands are
  `PRIMARY`; text is `INK`
- **Structural**: `set_padding(False)` + `set_gap(False)` +
  `set_background_color(None)`, no border — grouping only: every title
  block (`blocks/title.md`). `set_gap(False)` is for lines meant to touch,
  so the KPI band and the shell's `hc` take `set_spacing('small')` and keep
  theirs (`blocks/kpi-row.md`, `blocks/header.md`) — without it the
  header's control and the button beside it collide

The shell (header, sidebar) is not a band: white, a `HAIRLINE` line, an
`INK` lockup naming what the workbook is, `MUTED` nav with the selected
page in `PRIMARY` (`blocks/header.md`, `blocks/sidebar.md`) — the hue shows
on the selection, never as a fill.

The **section-card rule** — label, optional muted subline, then the body:

```python
sec = page.add_container()       # page = whichever page handle (home, scenarios, …)
sec.set_frame(1, y, 24, 14)
sec.set_column_density('high')
sec.set_spacing('small')
sec.set_background_color('#ffffff')
sec.set_border(sigma.border.solid(width=1, color=HAIRLINE, radius='round'))
sl = sec.add_text('**<Section label>**')          # 16px bold ink — the card title
sl.set_frame(1, 1, 12, 1)
ss = sec.add_text('<p class="p-small"><span style="color: ' + MUTED + '"><What this section shows and why it matters, one line.></span></p>')
ss.set_frame(1, 2, 18, 1)
# body (1, 3, 24, H-2); no subline → (1, 2, 24, H-1); cards under 9 rows drop the subline
```

- The label row's right side (columns 13–24) takes a chip, a segmented
  control, or the tab-switch buttons (`blocks/tabs.md`).
- Never nest a decorative card inside another card — inner containers are
  structural.

### Text — the whole type system

Text content is markdown. These are the only sizes that exist; spans set
**color only**, always a token in the one shape the blocks use —
`'<span style="color: ' + MUTED + '">…</span>'` — never size a run with
`font-size`. Spans survive inside headings and around `**bold**` and
`{{placeholders}}`.

| Role | Markup | Renders |
|---|---|---|
| Hero statement (the one loud line) | `### <span style="color: #ffffff">$4.2M to close the year</span>` | 24px, white on `PRIMARY` |
| Page title | `### Plan workspace` | 24px, ink |
| Section statement | `<p class="p-large">**Where the quarter stands**</p>` | 20px |
| Card label / lockup | `**Revenue by month**` — plain bold, sentence case | 16px, ink |
| Body | `<p class="p-small">…</p>`, values bolded: `**{{Total revenue}}**` | 14px |
| Subhead / card subline | `'<p class="p-small"><span style="color: ' + MUTED + '">One line saying the job.</span></p>'` | 14px |
| Eyebrow | `'<p class="p-small"><span style="color: ' + PRIMARY + '">FY26 OPERATING VIEW</span></p>'` — the one CAPS line | 14px |
| Right-aligned | add `style="text-align: right"` to the `<p>` | |

Fourteen is the floor for text elements; a smaller label is an element's own
title via `set_font_size`. KPI values are 24 bold, 30 on a loud band.

Dynamic values: `add_text(md, formulas={'Total revenue': (sigma.formula.sum(col), fmt)})`
binds `{{Total revenue}}`, with `fmt = sigma.format.format('currency_si', 1, '$')`;
use the base table's columns. A placeholder takes **no format spec** —
`{{Rev | $,.0f}}` is not parsed, it renders that literal string — and a bare
aggregate renders raw, full-precision digits, so bind a `(formula, fmt)` pair
for every number or date in prose. A value-list field takes no pair:
pre-format it as text (`blocks/formulas.md`, "Pre-formatted text"). Elements
format their own columns with `set_format` instead.

**Color values, never words** — a number may take `PRIMARY`, good,
or bad; a sentence stays `INK`, `BODY`, or `MUTED`. Pages open with language,
not metrics — an imperative or noun phrase plus a subhead naming the job;
"Dashboard" is not a title.

### Charts

Element titles hidden — the card label does that job. Single measure =
`SERIES` — good `'#008236'` or bad `'#c10007'` instead when the
measure is itself a gain or a loss (retention, uptime / churn, attrition);
a comparison series = `SERIES_GREY`; a categorical split
only when the categories are the subject (≤6). Every date axis truncated
to a grain and formatted; x labels never rotated. A rate, ratio, or
threshold measure never forces a zero baseline. Every KPI carries context
(`blocks/kpi-row.md`).

The Dashboards row names each band's chart; when that chart does not fit
the band's data, take the row the data matches:

| The band's data | Chart |
|---|---|
| one measure over a date, 12–40 marks at a grain | line (`blocks/chart-trend.md`; a plan or prior column → two-series) |
| a measure by an entity, 4–25 values | ranked horizontal bar, top-10 (`blocks/chart-ranked.md`) — never a sorted table |
| two measures by a category ≤8 | grouped bars (`blocks/chart-compare.md`) |
| a measure over a date split by a category ≤6 | stacked bars (`blocks/chart-composition.md`) |
| a static split, ≤6 slices, no date on the band | donut (`blocks/chart-composition.md`) |
| tiers as separate measure columns | ribbon (`blocks/chart-composition.md`) |
| a measure by two categoricals — ≤6 across, ≤12 down | heatmap (`blocks/pivot.md` `color_scale`), 14+ columns wide; hours as columns need all 24, so bucket to dayparts or take the wider frame |
| an opening figure, signed steps, a closing figure — a bridge, variance walk, build-up | waterfall (`blocks/chart-waterfall.md`) |
| a measure by a lat/long pair, or by a named region — where, footprint, estate, by site | point or region map (`blocks/chart-map.md`) |

`set_series_color`, `set_category_color`, `set_value_color`, and
`color_scale` take `SERIES`, `SERIES_MID`, `SERIES_GREY`, or the ramp
`TINT → SERIES_MID → SERIES` (good/bad for a gain-or-loss measure,
`'#ffffff'` on a `PRIMARY` tile) — never `PRIMARY` or `INK` (the forecast
block's actual bars are the one `INK` series, and say so), and never
`theme.highlight_color()`; every chart block sets its own colors.

## Blocks

Blocks are plain SDK code — change columns, copy, spans, and counts
freely; the styling calls stay as written, token names included.

| Need | File |
|---|---|
| Header band, or shared header + nav, with the Assistant trigger | `blocks/header.md` |
| Sidebar rail — the app shell: nav, picker, Assistant, status | `blocks/sidebar.md` |
| Title block + chip + breadcrumb + progress rail | `blocks/title.md` |
| KPI row + variants | `blocks/kpi-row.md` |
| Insight callout | `blocks/insight.md` |
| AI-written insight (explicit ask only; read with `blocks/insight.md`) | `blocks/insight-ai.md` |
| Active-context strip (page follows one selection) | `blocks/context-strip.md` |
| Comparison strip (baseline · current · change) | `blocks/compare-strip.md` |
| Hero band | `blocks/hero.md` |
| Trend over time | `blocks/chart-trend.md` |
| Actuals vs projection (forecast band) | `blocks/chart-forecast.md` |
| Category comparison | `blocks/chart-compare.md` |
| Ranking (top-N) | `blocks/chart-ranked.md` |
| Composition (stacked · donut) | `blocks/chart-composition.md` |
| Waterfall — a bridge from an opening figure to a closing one | `blocks/chart-waterfall.md` |
| Map — points from coordinates · shaded named regions | `blocks/chart-map.md` |
| Detail table + conditional formats · goals card (targets, quotas, budgets with a bar) | `blocks/table.md` |
| Pivot (measure × two dimensions) | `blocks/pivot.md` |
| Financial statement — P&L: sections, computed subtotal lines, variance | `blocks/statement.md` |
| Filter toolbar · full-height rail, form, or record column | `blocks/filters.md` |
| Buttons + action wiring | `blocks/buttons.md` |
| Tab switcher on a card, or a tabbed main surface | `blocks/tabs.md` |
| Stepped wizard in a modal · one-step form modal | `blocks/wizard.md` |
| Record detail — a row click or picker into a modal, drawer, or popover · record card beside a list | `blocks/detail.md` |
| Assistant chat — a popover from the shell's top-right trigger | `blocks/chat.md` |
| Repeated cards — one design per row or group (rep, region, product, queue item) · list rows · card feed with a per-card action | `blocks/cards.md` |
| A calculation no block shows — average, conditional, share of total, prior period, rank, date window, text built from a number (value-list fields, joined columns) | `blocks/formulas.md` |
| Input table — empty or linked, columns, seed rows; read with any app block | `blocks/input-table.md` |
| Plan grid app — with `input-table` `sidebar` `title` `formulas`; then `hero` `kpi-row` `cards` `context-strip` `compare-strip` `buttons` `chat` as its bands call for them | `blocks/plan-grid.md` |
| Forecast grid app — date spine × entities; the plan-grid reads plus `plan-grid` `chart-trend` | `blocks/forecast.md` |
| Review queue app — with `input-table` `sidebar` `title` `formulas`; then `filters` `kpi-row` `buttons` `chat` | `blocks/queue.md` |
| Intake app — with `input-table` `sidebar` `title` `formulas` `wizard`; then `kpi-row` `chart-trend` `chart-composition` `table` `buttons` `chat` | `blocks/intake.md` |

## SDK docs — `read_resource`

For a need no block covers (for calculations, `blocks/formulas.md` comes
first) — and only then: the `build_workbook` description's README, module,
and connector-skill reads do not apply here. Compose a `<module>` URI from
the scheme below — module names are the feature: `barChart`, `levelTable`,
`inputTable`, `form`, `data/source`, `action/inputTableEffects`. The
`skills/` names are a **closed set**, listed in the row below and nowhere
else: a block is a block, never `sdk://skills/<block>/SKILL.md`. If a URI
errors, `list_resources` once and take the name from what it lists.

| Read | For |
|---|---|
| `sdk://sdk/reference/sigma/<module>.md` | every method on a class, typed signature, `Literal` variants — the read for any call the blocks do not show, and enough on its own |
| `sdk://skills/<name>/SKILL.md` | a feature no block covers, and only these five — `forms`, `survey`, `relationship-columns`, `balance-sheet`, `maps` (region-type edge cases only — `blocks/chart-map.md` has the rest) |

Take only mechanics from those skills — their theme, styling, and layout
advice loses to the design system above. If an example in one fails
because imports or `sigma.data.sql` are unavailable, do not retry it — take
the mechanics from the module docs instead. Their
`/sdk/...` and `/skills/...` cross-references need the `sdk://` prefix; no path, URI, or tool name ever
goes inside a program.

## Failure handling

- **Typecheck error** — nothing ran. Fix exactly what the error names and
  resubmit; do not restructure a working block around it.
- **Runtime error** — the edits before it are committed. Recover in one
  program (it opens with the token block too) against the returned id:
  bind `old = list_pages()` **first**,
  `add_page` the pages afresh, then `delete()` each page in `old` — a
  workbook cannot reach zero pages, so deleting before adding dies on the
  last one. A later call of a linked-table app keeps every page — its base
  must survive: resubmit that call alone, fixed, after `delete()`-ing what
  its failed run had built before the error.
- **Replacing an element others read from** — `delete()` raises nothing and
  strands every consumer with no source; only a repeater or single row
  container can be re-pointed (`set_source`). `el.describe_lineage()` lists
  what sits downstream, so edit in place when anything does. A stranded one
  shows in `sigma.workbook.describe_lineage()` with nothing above it:
  rebuild it on the new element and `delete()` it.
- **A rejected approach** — a runtime refusal naming the operation, not a
  type or syntax problem — one retry, then change approach or tell the
  user; never resubmit just to see.
