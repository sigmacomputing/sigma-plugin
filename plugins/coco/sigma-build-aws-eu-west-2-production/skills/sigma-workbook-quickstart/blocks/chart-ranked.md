# Chart: ranking (horizontal top-N)

A ranking is a sorted horizontal bar — never a sorted table, never vertical
bars with rotated labels.

```python
rank = sec.add_bar_chart(src)
rank.set_frame(1, 3, 24, 12)   # H = 14; a shorter card → SKILL.md's section-card rule
rank.set_dimension(rank.get_column_by_name('<ENTITY>'))
rank.set_series([(sigma.formula.sum(rank.get_column_by_name('Revenue')), 'Total revenue')])
top = rank.list_series()[0]
top.set_format('currency_si', decimals=1, currency='$')
top.set_filter(sigma.filter.top_n(10))
rank.set_orientation('horizontal')
rank.set_sort_by_series('dimension', top, ascending=False)
rank.set_series_color(top, SERIES)
rank.dimension_axis().set_label_angle(0)
rank.dimension_axis().set_marks('none')
rank.value_axis().set_marks('none')
rank.value_axis().set_show_labels(True)      # the axis carries the values
rank.data_labels().set_visible(False)
rank.legend().set_visible(False)
rank.title_style().set_visible(False)
rank.set_background_color(None)
rank.set_padding(False)
```

- Adjust N in `sigma.filter.top_n(10)`; past ~12 bars give the card a taller
  frame rather than a smaller font.
- A blank in the entity column is its own `null` group, and a big one ranks
  first as an unlabeled bar. Name the entities to keep —
  `rank.get_column_by_name('<ENTITY>').set_filter(sigma.filter.values([...]))`
  from a query ranked by the measure, not an arbitrary distinct list — or rank by a label column with no blanks.
- Values read off the axis, not off the bars: a data label draws inside the
  longest bar, `BODY` on `SERIES`, which is unreadable. It failed in a 10-wide
  and a 14-wide card alike, so no width or value spread makes data labels safe.
