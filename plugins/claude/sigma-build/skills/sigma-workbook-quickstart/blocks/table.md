# Table card

Row-level detail — usually a page's last band, full width, inside a
section card. Keep tables for detail; a ranking belongs in
`blocks/chart-ranked.md`.

```python
tbl = sec.add_table(src)
tbl.set_frame(1, 2, 24, 12)      # H = 13; body per SKILL.md's section-card rule (an 18-row card → (1, 2, 24, 17))
cols = [
    tbl.get_column_by_name('<KEY>'),
    tbl.get_column_by_name('<STATUS>'),
    tbl.get_column_by_name('Revenue'),
    tbl.get_column_by_name('<DELTA>'),
]
tbl.set_visible_columns(cols)
tbl.set_sort([sigma.sort.descending(tbl.get_column_by_name('Revenue'))])
ts = tbl.table_style()
ts.set_preset('presentation')
ts.set_grid_lines('horizontal')
ts.set_cell_spacing('medium')
ts.header_style().set_color(MUTED)
for slot in [ts.header_style(), ts.cell_style()]:
    slot.set_background_color('#ffffff')
tbl.title_style().set_visible(False)
tbl.set_summary_bar(False)       # the row-count strip under the grid; SKILL.md's height rule assumes it off
tbl.set_background_color(None)
tbl.set_padding(False)

delta = tbl.get_column_by_name('<DELTA>')
tbl.add_conditional_format(delta, sigma.conditionalFormat.greater_than(0, background='#dcfce7', text_color='#008236', bold=True))
tbl.add_conditional_format(delta, sigma.conditionalFormat.less_than(0, background='#ffe2e2', text_color='#c10007', bold=True))
```

- Every judged column ships value-driven color in the good/bad tints —
  never raw green/red, and never color on a column nothing judges.
- **Whole-row verdict** — pass every column, and the rule paints the row:
  `tbl.add_conditional_format(tbl.list_columns(), sigma.conditionalFormat.formula(sigma.formula.eq(tbl.get_column_by_name('<STATUS>'), sigma.formula.const_text('At risk')), background='#fef3c6'))`
  — the warn fill for a state still open, the bad fill for one already lost.
  `conditionalFormat.formula` takes a **`sigma.formula` object**, never a
  formula string — a string fails the typecheck. It is the only rule that
  compares two columns:
  `sigma.formula.lt(tbl.get_column_by_name('Revenue'), tbl.get_column_by_name('Target'))`.
- Every single-color rule also carries `number_format=` / `format_decimals=` /
  `format_currency=`, so one rule can reformat the cells it matches — a percent
  row inside a currency column, without touching the column's own format.
- Grouped rollup: `g = tbl.set_groupings([tbl.get_column_by_name('<REGION>')])[0]`
  — derive a date grain with `add_column` + `sigma.formula.date_trunc`
  first; grouping keys always show. The rolled-up measure is
  `g.set_calculation('<Total revenue>', sigma.formula.sum(tbl.get_column_by_name('Revenue')))`.
  An aggregate in `add_column` instead returns the **row-level** value, not
  the group's — it renders numbers, so it reads plausible and is wrong.
  `set_visible_columns` takes base-level columns only — a grouping
  calculation in the list raises; one row per group with only its
  calculations is the pivot rollup (`blocks/pivot.md`).
- **Goals card** — a contained card, 8–12 columns, for targets, quotas, or
  budget lines: label + subline with a soft action button on the label row
  (`blocks/buttons.md`, `'New goal'` opening the form modal of
  `blocks/wizard.md`), then a one-row-per-goal table with a progress bar,
  then a one-line muted footer. The table:
  ```python
  gt = sec.add_table(src)
  gt.set_frame(1, 3, 24, T)                   # T from the table height rule in SKILL.md, on the goal count
  g = gt.set_groupings([gt.get_column_by_name('<GOAL>')])[0]
  g.set_calculation('Achieved', sigma.formula.sum(gt.get_column_by_name('Revenue')))
  g.set_calculation('Progress', sigma.formula.divide(sigma.formula.sum(gt.get_column_by_name('Revenue')), sigma.formula.sum(gt.get_column_by_name('Target'))))
  g.set_collapsed(True)                       # group rows only
  gt.set_visible_columns([])                  # an empty list hides every base column; keys and calculations stay
  gt.get_column_by_name('Achieved').set_format('currency_si', decimals=1, currency='$')
  gt.get_column_by_name('Progress').set_format('percent', decimals=0)
  gt.add_conditional_format(gt.get_column_by_name('Progress'), sigma.conditionalFormat.data_bars(SERIES_MID, '#c10007', show_values=True, min=0, max=1))   # mid tone — the percent prints over the bar
  ```
  plus the table-style calls above; the soft button `'New goal'` at
  `(17, 1, 8, 2)` with the label and subline 16 wide (a frame over them
  relocates the subline to the card's bottom); the footer at `(1, T + 3, 24, 2)` binds
  `sigma.formula.count_distinct(base.get_column_by_name('<GOAL>'))` —
  "{{n}} goals tracked" (a per-goal condition cannot be counted in prose).
  Card height H = T + 4 (13 goals → T 19, H 23). As a Briefing's 8-column
  side card, T = 10 → H 14 (6 goals, the rest scroll) and no button.
- Number formats per column:
  `col.set_format('currency_si', decimals=1, currency='$')` /
  `('percent', decimals=1)` / a date's `set_format_pattern('%b %d')` — a date column
  left unformatted renders as a raw timestamp.
- "And then what?" — a table of records on a work surface opens
  the record on a row click or a picker (`blocks/detail.md`), or is deliberately
  reference-only; a table nobody can open is the commonest thing missing
  from a finished page. A table of records a reader looks things up in also takes
  a `contains` search over its name column in the toolbar above
  (`blocks/filters.md`).
