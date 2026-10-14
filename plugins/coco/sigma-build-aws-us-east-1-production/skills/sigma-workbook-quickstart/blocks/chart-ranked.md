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
rank.value_axis().set_show_labels(False)     # the labels on the bars carry the values
dl = rank.data_labels()
dl.set_visible(True)
dl.set_color(BODY)
rank.legend().set_visible(False)
rank.title_style().set_visible(False)
rank.set_background_color(None)
rank.set_padding(False)
```

- Adjust N in `sigma.filter.top_n(10)`; past ~12 bars give the card a taller
  frame rather than a smaller font.
- The data labels sit outside the bars only while there is room: the longest
  bar's label falls inside it, `BODY` on `SERIES`, which is unreadable. Give a
  ranking a card of 14+ columns. Width is not enough when the values are close
  — a ratio, a rate, a cost-per, anything whose smallest bar is over ~80% of
  the largest puts every label inside — so for those, axis labels instead:
  `rank.value_axis().set_show_labels(True)` and `dl.set_visible(False)`.
