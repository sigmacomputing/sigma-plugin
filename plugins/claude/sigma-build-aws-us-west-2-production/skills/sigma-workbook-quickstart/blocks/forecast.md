# Forecast grid app — a value per entity per period

The reader forecasts by month or quarter per entity (family, product, rep,
region). Pages **Overview · Forecast · Review** — the bands of
`blocks/plan-grid.md` with the grid swapped: its rows are **entity × period**,
a seeded date spine cross-joined to the entities, last year's actuals beside
the editable forecast.

## Call 1 — opening, then the backbone on the data page

```python
spine = data_page.add_input_table('<CONNECTION_ID>')   # the source's own connection — a join needs both sides on one
spine.set_name('Date spine')
spine.set_frame(1, 13, 24, 6)
s_month = spine.add_editable_column('Month', 'datetime')
spine.upsert_rows([{s_month: datetime(2026, 10, 1, 12)}, {s_month: datetime(2026, 11, 1, 12)}, {s_month: datetime(2026, 12, 1, 12)}])   # 3 shown — seed every period of the horizon (12 months or 4–8 quarters), noon
entities = data_page.add_table(src)                    # one row per entity
entities.set_name('Families')
entities.set_frame(1, 19, 24, 6)
eg = entities.set_groupings([entities.get_column_by_name('<ENTITY>')])[0]
eg.set_calculation('Units', sigma.formula.sum(entities.get_column_by_name('Quantity')))
actuals = data_page.add_table(src)                     # entity × month history
actuals.set_name('Actuals by month')
actuals.set_frame(1, 25, 24, 6)
am = actuals.add_column('Actual month', sigma.formula.date_trunc('month', actuals.get_column_by_name('<DATE>')))
ag = actuals.set_groupings([actuals.get_column_by_name('<ENTITY>'), am])[1]   # [1] — the inner level carries the calc
ag.set_calculation('Actual revenue', sigma.formula.sum(sigma.formula.multiply(actuals.get_column_by_name('Price'), actuals.get_column_by_name('Quantity'))))
matrix = data_page.add_table(sigma.data.source.join(sigma.data.source.SourceInput(entities.to_source(), eg), sigma.data.source.SourceInput(spine.to_source()), 'left_outer', [], key_formulas=[('1', '1')]))   # the cross join
matrix.set_name('Entity x month')
matrix.set_frame(1, 31, 24, 6)
fsrc = data_page.add_table(sigma.data.source.join(sigma.data.source.SourceInput(matrix.to_source()), sigma.data.source.SourceInput(actuals.to_source(), ag), 'left_outer', [],
    key_formulas=[('[<ENTITY>]', '[<ENTITY>]'), ("DateTrunc('month', [Month])", "DateAdd('year', 1, [Actual month])")]))   # last year's same month
fsrc.set_name('Forecast source')
fsrc.set_frame(1, 37, 24, 6)
```

## Call 2 — the grid, in the Forecast page's section card

```python
fsrc = data_page.get_element('<FSRC ID>')     # re-fetch, with the pages as blocks/input-table.md's call 2 opens
if not isinstance(fsrc, LevelTable):
    raise RuntimeError('re-fetch')
ft = sec.add_linked_input_table(fsrc.to_source(), lookup_columns={'<ENTITY>': 'Family', 'Month': 'Month'}, source_columns={'Actual revenue': 'Last year'})
ft.set_name('Monthly forecast')
ft.set_frame(1, 3, 24, 16)
f_val = ft.add_editable_column('Forecast', 'number')
f_why = ft.add_editable_column('Note', 'text')
f_ly = ft.get_column_by_name('Last year')
f_delta = ft.add_formula_column('vs last year', sigma.formula.subtract(f_val, f_ly))
ft.set_frozen_column(ft.get_column_by_name('Family'))
ft.get_column_by_name('Month').set_format_pattern('%b %Y')
ft.set_sort([sigma.sort.ascending(ft.get_column_by_name('Family')), sigma.sort.ascending(ft.get_column_by_name('Month'))])
# then the style calls, currency formats, and Delta conditional formats of blocks/input-table.md
```

## Step 5 call — seeds, by the composite key

```python
ft.update_rows([                               # fam, mon from get_column_by_name; f_val, f_why narrowed
    ({fam: 'Audio', mon: datetime(2026, 10, 1, 12)}, {f_val: 8200000, f_why: 'Launch month'}),
    ({fam: 'Audio', mon: datetime(2026, 11, 1, 12)}, {f_val: 9100000, f_why: 'Holiday ramp'}),
    ({fam: 'Smart Phones', mon: datetime(2026, 10, 1, 12)}, {f_val: 7600000}),
])
```

- A quarter grid uses `date_trunc('quarter', …)` and quarter-start seeds.
- Everything else is `blocks/plan-grid.md` over `ft.to_source()` — KPI row,
  compare strip, submit and review wiring — except Overview's pending band,
  which is `blocks/chart-trend.md`'s two-series variant (Last year behind
  Forecast, by Month) at `(1, 15, 24, 14)`.
