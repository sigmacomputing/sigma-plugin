# Chart: trend line

The default shape for any measure over time: the time scale spaces marks by
real elapsed time, so gaps and pacing read true. The line row of SKILL.md's
chart table; the Dashboards row names the headline and window variants below.

```python
tr = sec.add_line_chart(src)
tr.set_frame(1, 3, 24, 12)   # H = 14; a shorter card → SKILL.md's section-card rule
month = tr.add_column('Order month', sigma.formula.date_trunc('month', tr.get_column_by_name('<DATE COL>')))
month.set_format_pattern('%b %Y')
tr.set_dimension(month)
tr.dimension_axis().set_scale_type('time')
tr.dimension_axis().set_marks('none')
tr.dimension_axis().set_label_angle(0)
tr.set_series([(sigma.formula.sum(tr.get_column_by_name('Revenue')), 'Total revenue')])
ser = tr.list_series()[0]
ser.set_format('currency_si', decimals=1, currency='$')
tr.set_series_color(ser, SERIES)
tr.value_axis().set_marks('none')
vs = tr.value_axis().scale()
if isinstance(vs, LinearScale):
    vs.set_show_zero(False)          # a trend reads slope — don't force a zero baseline
ls = tr.line_style()
ls.set_interpolation('monotone')
ls.set_show_points(False)
ls.set_stroke_width(2)
ls.set_missing('hide')
tr.title_style().set_visible(False)
tr.legend().set_visible(False)
tr.set_background_color(None)
tr.set_padding(False)
# Two-series variant (actual + plan or prior year): replace the block from
# tr.set_series(...) through tr.set_series_color(...) — and the legend line — with:
#   tr.set_series([
#       (sigma.formula.sum(tr.get_column_by_name('Target')), 'Plan'),
#       (sigma.formula.sum(tr.get_column_by_name('Revenue')), 'Total revenue'),
#   ])
#   pair = tr.list_series()
#   pair[0].set_format('currency_si', decimals=1, currency='$')
#   pair[1].set_format('currency_si', decimals=1, currency='$')
#   tr.set_series_color(pair[0], SERIES_GREY)   # context grey behind
#   tr.set_series_color(pair[1], SERIES)   # the measure in front
#   tr.legend().set_position('top-left')      # replaces legend().set_visible(False)
```

- Pick the grain from the queried date span — aim for 12–40 marks; a span
  inside one year takes `set_format_pattern('%b')`, a `'week'` grain `'%b %d'`.
- **Headline number over the chart** (same card): the card grows to 15,
  the chart moves to `(1, 6, 24, 10)`, and a title-less KPI sits between
  the subline and the chart —
  `hk = sec.add_kpi(src)` · `hk.set_frame(1, 3, 8, 3)` ·
  `hk.title().set_visible(False)` · `hk.set_value((sigma.formula.sum(hk.get_column_by_name('Revenue')), 'Headline'))`
  · value style 24, bold, ink · `hk.set_background_color(None)` ·
  `hk.set_padding(False)` — the number the line explains, read first.
- **Windowed trend** — the card carries its own date window, scoping this
  chart (and its headline KPI) without touching the page's filters:
  `win = sigma.control.add_date_range_control(sec, target=[tr.get_column_by_name('<DATE COL>'), hk.get_column_by_name('<DATE COL>')])`
  · `win.set_name('Window')` · `win.set_frame(17, 1, 8, 2)` — the control
  is two rows whatever its frame says, so the subline narrows to
  `(1, 2, 16, 1)`; no `value=` (a rolling window cannot be a default; the
  reader picks one from the control's presets). Drop the `hk` target when
  the card has no headline. Keep the month grain here — the window does
  the narrowing.
- Actuals + a projection in one frame is its own block:
  `blocks/chart-forecast.md`.
