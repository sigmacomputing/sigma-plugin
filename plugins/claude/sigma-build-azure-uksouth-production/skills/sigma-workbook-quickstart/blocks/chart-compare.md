# Chart: category comparison (bars)

Grouped bars answer "which categories differ, and by how much" — the default
two-measure shape for actual against plan, side by side so the gap shows per group.

```python
cmp = sec.add_bar_chart(src)
cmp.set_frame(1, 3, 24, 12)   # H = 14; a shorter card → SKILL.md's section-card rule
cmp.set_dimension(cmp.get_column_by_name('<CATEGORY>'))
cmp.set_series([
    (sigma.formula.sum(cmp.get_column_by_name('Target')), 'Plan'),
    (sigma.formula.sum(cmp.get_column_by_name('Revenue')), 'Actual'),
])
series = cmp.list_series()
cmp.set_series_color(series[0], SERIES_GREY)
cmp.set_series_color(series[1], SERIES)
cmp.set_stacking('none')
cmp.dimension_axis().set_marks('none')
cmp.dimension_axis().set_label_angle(0)
cmp.value_axis().set_marks('none')
cmp.legend().set_position('top-left')
cmp.title_style().set_visible(False)
cmp.set_background_color(None)
cmp.set_padding(False)
```

- Single measure: one series in `SERIES` — good `'#008236'` or bad `'#c10007'` when the measure is itself a gain or a loss (retention / churn), `cmp.legend().set_visible(False)`.
- Long category labels: `cmp.set_orientation('horizontal')` — the dimension moves
  to the y-axis and labels sit flat; never reach for a label angle instead.
