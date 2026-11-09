# Chart: scatter

Two measures against each other across entities — where the relationship or the
outliers are the question (spend vs revenue per rep, price vs volume per
product). 15–200 points; fewer reads as a ranked or compare chart, more as
noise. One point per **row** of the chart's source, so the source is already at
the entity's grain: a rollup's own source, never the detail rows.

```python
pts = data_page.add_table(src)
pts.set_name('<Entity> points')
pts.set_frame(1, 13, 24, 12)             # stacked 12 rows under the last base
pg = pts.set_groupings([pts.get_column_by_name('<ENTITY>')])[0]
pg.set_calculation('Spend', sigma.formula.sum(pts.get_column_by_name('<SPEND>')))
pg.set_calculation('Revenue', sigma.formula.sum(pts.get_column_by_name('<REVENUE>')))

sc = sec.add_scatter_chart(pg.to_source())   # the grouping's source: one row per entity
sc.set_frame(1, 3, 24, 12)               # H = 14; a shorter card → SKILL.md's section-card rule
sc.set_dimension(sc.get_column_by_name('Spend'))        # x: a numeric column
sc.set_series([(sigma.formula.sum(sc.get_column_by_name('Revenue')), 'Total revenue')])   # y
ser = sc.list_series()[0]
ser.set_format('currency_si', decimals=1, currency='$')
sc.get_column_by_name('Spend').set_format('currency_si', decimals=1, currency='$')
sc.set_series_color(ser, SERIES)
sc.set_tooltips([sc.get_column_by_name('<ENTITY>')])    # the point's name, on hover
sc.dimension_axis().set_marks('none')
sc.value_axis().set_marks('none')
sc.dimension_axis().set_title('Spend')
sc.value_axis().set_title('Revenue')
sc.title_style().set_visible(False)
sc.legend().set_visible(False)
sc.set_background_color(None)
sc.set_padding(False)
```

- Both axes need a title — with no entity labels on the marks, the axis titles
  are how the reader knows which measure is which.
- A rate or ratio on either axis never forces a zero baseline:
  `s = sc.value_axis().scale()` · `if isinstance(s, LinearScale): s.set_show_zero(False)`.
- **Bubble**: `sc.set_size_column((sigma.formula.sum(sc.get_column_by_name('<THIRD MEASURE>')), '<Name>'))`
  — a bare column draws, but gets a default `Sum` and a warning.
- **Split by a category** (≤6, the categories are the subject):
  `sc.set_color_category(sc.get_column_by_name('<CATEGORY>'))` and one
  `sc.set_category_color('<CATEGORY VALUE>', SERIES)` per value, by size rank,
  largest first (`SERIES` `SERIES_GREY` `MUTED` `EDGE` `SERIES_MID` `TINT`); the legend moves to
  `'right'` instead of hiding. The category column joins the rollup the same way
  `Spend` does (`max` of it per entity).
- Never `set_color_scale` here: the ramp reads as a third measure that the page
  never explains. A highlighted outlier takes `add_conditional_color` on its own
  rule, named in the report.
- Look at the step 5 shot with the axes in mind: x is a number column, and a
  point count far from the entity count means the source is not at entity grain.
