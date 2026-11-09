# Chart: area

A measure over time read as **volume** — what accumulated, or how a total
splits month by month. Use it over the trend line when the filled mass is the
point (a running total, a stacked split, a share of the whole); a plain rate or
price over time stays a line (`blocks/chart-trend.md`).

```python
ar = sec.add_area_chart(src)
ar.set_frame(1, 3, 24, 12)   # H = 14; a shorter card → SKILL.md's section-card rule
month = ar.add_column('Order month', sigma.formula.date_trunc('month', ar.get_column_by_name('<DATE COL>')))
month.set_format_pattern('%b %Y')
ar.set_dimension(month)
ar.dimension_axis().set_scale_type('time')
ar.dimension_axis().set_marks('none')
ar.dimension_axis().set_label_angle(0)
ar.set_series([(sigma.formula.sum(ar.get_column_by_name('Revenue')), 'Total revenue')])
ser = ar.list_series()[0]
ser.set_format('currency_si', decimals=1, currency='$')
ar.set_series_color(ser, SERIES)
ar.value_axis().set_marks('none')
st = ar.area_style()
st.set_interpolation('monotone')
st.set_show_line(True)
st.set_stroke_width(2)
st.set_missing('hide')
ar.title_style().set_visible(False)
ar.legend().set_visible(False)
ar.set_background_color(None)
ar.set_padding(False)
```

- An area encodes magnitude by its height, so the baseline stays at zero —
  never `set_show_zero(False)` here, unlike the trend line.
- Pick the grain from the queried date span, as `blocks/chart-trend.md` does:
  12–40 marks, `'%b'` inside one year.
- **Stacked split** (≤6 categories — verify the count with `query`): add
  `ar.set_color_category(ar.get_column_by_name('<CATEGORY>'))`, one
  `ar.set_category_color('<CATEGORY VALUE>', SERIES)` per value, by size rank,
  largest first (`SERIES` `SERIES_GREY` `MUTED` `EDGE` `SERIES_MID` `TINT`),
  `ar.set_sort_by_series('color_category', ar.list_series()[0], True)` so the
  stack runs in that order with the largest on the baseline,
  `ar.set_stacking('stacked')`, and `ar.legend().set_position('right')` in place
  of hiding it; `'percent'` stacking for a share of total.
- Two series (actual and plan): no stacking, so the areas overlay; the plan
  takes `SERIES_GREY` behind, the actual `SERIES` in front, as the trend block's
  two-series variant.
- The same measure at the same grain never also gets a trend line on the page
  (SKILL.md's "nothing is said twice").
