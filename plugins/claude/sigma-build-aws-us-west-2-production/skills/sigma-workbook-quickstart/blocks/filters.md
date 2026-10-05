# Filters

Controls target **base** columns so one filter re-scopes everything built
from the base. Pick the control from the column's shape: few distinct
values → segmented · many → list · date → `add_date_range_control` ·
number → `add_number_range_control` · a single threshold → `add_slider_control(bar, value=50000, target=..., range=(0, 250000, 5000), compare_op='>=')`
(`compare_op` is `'='`, `'<='`, or `'>='`) · boolean → `add_switch_control` —
all take `(host, value=, target=)` like the three below; a number-range
`value=` is a `(min, max)` tuple. A **type-to-find search box** over a name
column is `add_text_control` with a `match_mode` — required on any surface a
reader looks records up in (a table or card feed of deals, accounts,
tickets, transactions), and what a name or id column of more than ~25
distinct values takes instead of a list control:

```python
find = sigma.control.add_text_control(bar, target=base.get_column_by_name('<NAME>'),
    match_mode='contains', case_sensitive=False, placeholder='<Deal name>')
find.set_name('Search')               # 'Search' labels it, the placeholder names the column — never both
find.set_frame(4, 1, 10, 2)           # leads the bar, after the label; two filters follow at (14,1,5,2) and (19,1,6,2)
```

Target the **base** name column, so the search re-scopes the counts and the
KPI band under the table too — a child table only when that child is the
surface (a queue, a card feed's `lst`). `match_mode` is `'contains'
'starts_with' 'ends_with' 'exactly' 'like' 'regex'`; `'exactly'` pins a
surface to one record — the table under a detail card (`blocks/detail.md`),
the row an approval panel writes to (`blocks/plan-grid.md`) — not a search.
Both text controls also run variable-only with no `target=`.

## Toolbar — up to ~4 filters

One card strip above the content it governs. A search leads it and costs
two of the four slots — the frames under it shift as the snippet above says.

```python
bar = page.add_container()
bar.set_frame(1, y, 24, 2)
bar.set_column_density('high')
bar.set_spacing('small')
bar.set_background_color('#ffffff')
bar.set_border(sigma.border.solid(width=1, color=HAIRLINE, radius='round'))
bl = bar.add_text('<p class="p-small"><span style="color: ' + MUTED + '">Filters</span></p>')
bl.set_frame(1, 1, 3, 2)
bl.set_vertical_align('middle')
region = sigma.control.add_list_control(bar, target=base.get_column_by_name('Region'))
region.set_name('Region')
region.set_frame(4, 1, 5, 2)
dates = sigma.control.add_date_range_control(bar, target=base.get_column_by_name('<DATE COL>'))
dates.set_name('Period')
dates.set_frame(9, 1, 5, 2)
seg = sigma.control.add_segmented_control(bar, options=['<A>', '<B>', '<C>'], value='<A>', target=base.get_column_by_name('<STATUS>'))
seg.set_name('Status')
seg.set_frame(14, 1, 6, 2)
```

## Full-height columns — a rail, a form, or a record list beside the work

The rail is a card — white, hairline, padded — and the content column
beside it is structural. Both take the same `y` and the same height, and
the y-cursor resumes below them.

```python
rail = page.add_container()
rail.set_frame(1, y, 5, 30)
rail.set_column_density('low')          # 6 inner columns
rail.set_spacing('small')
rail.set_background_color('#ffffff')
rail.set_border(sigma.border.solid(width=1, color=HAIRLINE, radius='round'))
rl = rail.add_text('<p class="p-small"><span style="color: ' + MUTED + '">Filters</span></p>')
rl.set_frame(1, 1, 6, 1)
r1 = sigma.control.add_list_control(rail, target=base.get_column_by_name('Region'))
r1.set_name('Region')
r1.set_frame(1, 2, 6, 2)
# stack further controls at y 4, 6, 8 …
main = page.add_container()
main.set_frame(6, y, 19, 30)
main.set_column_density('high')
main.set_padding(False)                 # structural — cards go inside it
```

- The same two containers mirror and resize for the other page splits:
  `main (1,y,18,H)` + `rail (19,y,6,H)` for a running summary or approval
  panel the reader watches while working; `panel (1,y,8,H)` +
  `main (9,y,16,H)` when the left column is a form or a record list. That
  column is a card like the rail — the same fill, border, and padding
  calls; only `main` is structural.
- A control created with `add_*_control` has no label kwarg — always
  `set_name(...)` after, and give it a real short one. **`set_name('')` does
  not blank a label** — it falls back to the target column's name, so a
  picker meant to read bare renders `Opportunity Close Fiscal Quarter`
  instead. A label never moves beside the input, and hiding it buys no row
  back, so budget the row for it and name it in two words. A two-row
  control spends **row 1 on the label and row 2 on the input** — so
  anything that must read level with it lines up with row 2, not with the
  frame: a button is framed `(x, 2, w, 1)`, a text `(x, 1, w, 2)` with
  `set_vertical_align('bottom')`. Buttons have no vertical align of their
  own.
- Set `value=` defaults only when the first render still shows data; a
  filtered-to-empty opening page is a build failure.
- A date-range default is absolute datetimes —
  `value=(datetime(2026, 1, 1), datetime(2026, 6, 30))`; `datetime(y, m, d)`
  is available bare. A rolling window ("last 90 days") cannot be a control
  default — leave it unset, or flag rows with `sigma.formula.date_add`
  (`blocks/formulas.md`).
- `target=` accepts a list to filter several base tables' columns at once
  (`[orders.get_column_by_name('Region'), targets.get_column_by_name('Region')]`).
- The segmented control's `options` order is display order — pass a
  chronological/logical list, not whatever `query` returned.
