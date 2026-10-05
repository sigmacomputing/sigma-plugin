# Chart: actuals vs projection

History as solid bars, the projection as a `SERIES` line, and a tinted band
marking where the data stops being real. Use whenever the source carries a
flag separating actuals from forecast/plan/target rows.

```python
fc = sec.add_combo_chart(src)
fc.set_frame(1, 3, 24, 12)   # H = 14; a shorter card → SKILL.md's section-card rule
fm = fc.add_column('Forecast month', sigma.formula.date_trunc('month', fc.get_column_by_name('<DATE COL>')))
fm.set_format_pattern('%b %Y')
fc.set_dimension(fm)
fc.dimension_axis().set_scale_type('time')
fc.dimension_axis().set_marks('none')
fc.dimension_axis().set_label_angle(0)
actual = sigma.formula.eq(fc.get_column_by_name('<FLAG COL>'), sigma.formula.const_text('<ACTUAL VALUE>'))
projected = sigma.formula.neq(fc.get_column_by_name('<FLAG COL>'), sigma.formula.const_text('<ACTUAL VALUE>'))
fc.set_series([
    (sigma.formula.sum_if(fc.get_column_by_name('Revenue'), actual), 'Actual'),
    (sigma.formula.sum_if(fc.get_column_by_name('Revenue'), projected), 'Projected'),
])
pair = fc.list_series()
pair[0].set_format('currency_si', decimals=1, currency='$')
pair[1].set_format('currency_si', decimals=1, currency='$')
fc.set_series_shape(pair[0], 'bar')       # shapes before colors — reshaping
fc.set_series_shape(pair[1], 'line')      # can clear formatting
fc.set_series_color(pair[0], INK)        # ink bars — the one series that is not SERIES_*
fc.set_series_color(pair[1], SERIES)
fc.value_axis().set_marks('none')
fb = fc.add_ref_band(
    'dimension',
    sigma.refMarkValue.formula(sigma.formula.min_if(fm, projected)),
    sigma.refMarkValue.column(fm, 'max'))
fb.set_fill_color(TINT)
fb.set_line_visible(False)
fb.set_label_visible(True)
fb.set_label_text('FORECAST')
fb.set_label_color(MUTED)
fc.legend().set_position('top-left')
fc.title_style().set_visible(False)
fc.set_background_color(None)
fc.set_padding(False)
```

- Verify the flag column's distinct values with `query` first — the
  `'<ACTUAL VALUE>'` literal is the usual empty-chart culprit.
- Bars keep their zero baseline — never suppress zero on a bar series.
- A second measure (e.g. cost) rides along as two more `sum_if` series:
  actual as a `SERIES_GREY` bar, projected as a `SERIES_GREY` line.
- The band spans first projected month → last month; on a chart with no
  projected rows yet it collapses harmlessly to the right edge.
