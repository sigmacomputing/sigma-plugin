# Pivot card

A measure by two dimensions — the plan-grid / heatmap shape. A pivot renders
its name as a title by default — so let that title **be** the card label: set
it in sentence case and add no label text to the wrapper. Unlike a table, do **not**
`title_style().set_visible(False)` here; the title is the label.
(`set_name('')` blanks it if a design truly needs it gone.)

```python
piv = sec.add_pivot_table(src)
piv.set_frame(1, 1, 24, 14)                  # body (1, 1, 24, H), no label rows; a heatmap card is 14+ columns wide, H16 for five rows with the totals off (SKILL.md's pivot row)
piv.set_name('<Plan by line item and month>')
pm = piv.add_column('Pivot month', sigma.formula.date_trunc('month', piv.get_column_by_name('<DATE COL>')))
pm.set_format_pattern('%b')
piv.add_pivot_row(piv.get_column_by_name('<LINE ITEM>'))
piv.add_pivot_column(pm)
piv.add_pivot_value(piv.get_column_by_name('Amount'))   # auto-aggregated — and renamed 'Sum of Amount' from here on
pts = piv.table_style()
pts.set_preset('presentation')
for slot in [pts.header_style(), pts.column_header_style(), pts.row_header_style(), pts.cell_style()]:
    slot.set_background_color('#ffffff')
piv.set_background_color(None)
piv.set_padding(False)
```

- Two row dimensions nest broad→narrow (`add_pivot_row` twice, e.g.
  Section then Line Item).
- A source column used as a value is renamed `Sum of <name>` — look it up
  by that name afterwards (formats, conditional formats); a column the
  program added with `add_column` keeps its name.
- Value-driven cell color:
  `piv.add_conditional_format(piv.get_column_by_name('Sum of Amount'), sigma.conditionalFormat.color_scale([TINT, SERIES]))`
  turns it into a heatmap — the `TINT → SERIES` ramp only, never a rainbow;
  add `piv.set_totals_default_display(show_subtotals=False, show_grand_totals=False)`
  so the totals column does not crowd the cells.
- Column-dimension cardinality decides width: ~12 monthly columns fit;
  past that, truncate coarser or filter the range.
- "Limit it to five rows" (any number): `sigma.filter.top_n` ranks the column it is applied
  to, so on a row dimension it silently keeps the alphabetically last N.
  Query the N highest by value and filter the row column to them with
  `sigma.filter.values([...])`.

## Rollup grid — no column dimension

The plan-review shape: nested rows, many value columns, and subtotals you
get by collapsing. Skip `add_pivot_column` entirely.

```python
piv.add_pivot_row(piv.get_column_by_name('<SECTION>'))     # broad
piv.add_pivot_row(piv.get_column_by_name('<LINE ITEM>'))   # narrow
piv.set_totals_default_display(show_subtotals=True, show_grand_totals=True)
piv.set_frozen_column(piv.get_column_by_name('<SECTION>'))
piv.rename_total_label(piv.get_column_by_name('<SECTION>'), 'FY total')
piv.collapse_rows(piv.get_column_by_name('<SECTION>'))   # the outer column rolls up to its subtotals; collapsing the inner one left every row open
```

- **Semantics come from formula conditional formats**, not a color scale —
  see `blocks/table.md` for the call, which takes a `sigma.formula` object.
  They bold the subtotal rows the data already carries
  (`sigma.formula.in_(piv.get_column_by_name('<SECTION>'), sigma.formula.const_text('Total revenue'), sigma.formula.const_text('Gross profit'))`,
  no background), and they shade the settled half of a period grid (`closed`,
  defined below → background `HAIRLINE`) so the reader sees where the past
  ends. A subtotal the data does *not* carry — gross profit, EBITDA, anything
  computed across sections — no pivot can produce: that is
  `blocks/statement.md`.
- A period grid can carry **one blended measure** rather than two — actuals
  for closed periods, plan for open ones, in one column the shading already
  explains. Add it as the single pivot value:
  `closed = sigma.formula.lte(pm, sigma.formula.date_trunc('month', sigma.formula.today()))`
  then `piv.add_column('Plan or actual', sigma.formula.if_(closed, piv.get_column_by_name('Actual'), piv.get_column_by_name('Plan')))`.
