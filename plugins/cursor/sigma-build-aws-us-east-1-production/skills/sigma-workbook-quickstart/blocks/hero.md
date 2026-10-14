# Hero band

The one loud surface — at most one per page, carrying the number that decides the meeting.

```python
hero = page.add_container()
hero.set_frame(1, y, 24, 5)
hero.set_column_density('high')
hero.set_spacing('small')
hero.set_background_color(PRIMARY)
hero.set_border(sigma.border.solid(radius='round'))   # radius alone rounds the corners — draws no line
gap = sigma.formula.subtract(sigma.formula.sum(base.get_column_by_name('Target')), sigma.formula.sum(base.get_column_by_name('Revenue')))
gap_text = sigma.formula.ampersand(sigma.formula.const_text('$'), sigma.formula.ampersand(sigma.formula.text(sigma.formula.round(sigma.formula.divide(gap, sigma.formula.const_num(1000000)), 1)), sigma.formula.const_text('M')))   # pre-formatted (blocks/formulas.md) — bound bare, a raw float in 24px type
copy = hero.add_container()          # structural: statement + support line read as one unit
copy.set_frame(1, 1, 15, 5)
copy.set_column_density('high')
copy.set_padding(False)
copy.set_gap(False)
copy.set_background_color(None)
copy.set_border(None)
hs = copy.add_text('### <span style="color: #ffffff">{{Gap}} to close the year</span>', formulas={'Gap': gap_text})
hs.set_frame(1, 1, 24, 3)
hs.set_vertical_align('middle')
hsub = copy.add_text('<p class="p-small"><span style="color: ' + EDGE + '">Plan says <what closing it takes, one line>.</span></p>')
hsub.set_frame(1, 4, 24, 2)          # the copy fills the band — no trailing empty row
hk = hero.add_kpi(src)
hk.set_frame(17, 1, 8, 5)
hk.set_name('Committed pipeline')
hk.set_value((sigma.formula.sum(hk.get_column_by_name('<MEASURE>')), 'Committed'))
hk.get_column_by_name('Committed').set_format('currency_si', decimals=1, currency='$')
hk.title().set_color(EDGE)
hk.title().set_font_size(14)
hk.value_style().set_color('#ffffff')
hk.value_style().set_font_size(30)
hk.value_style().set_bold(True)
hk.layout().set_anchor('left')
hk.set_background_color(None)
hk.set_padding(False)
```

- **Statement + next action** is the band's other shape: the copy container
  widens to 17 columns and one button takes `(18, 1, 7, 5)` with `set_button_size('large')`
  and `set_align('right')` — never `'stretch'`, which inflates the pill to a
  quarter of the page. Name the step ("Begin the variance review →"), and use
  it in place of the KPI when the page's job is to send the reader onward.
- A Briefing dashboard takes the statement + KPI shape above; statement +
  next action when the workbook has a page to send the reader to.
- Pair it with a next-action — 2–3 named records (the deals, the line items that close the gap) or a button (`blocks/buttons.md`); the loud number alone is a poster, not a page.
- Every element on the band restates its colors — anything left at a default renders ink-on-ink and disappears.
- The statement is `###` — the page-title size, white on `PRIMARY`; the
  support line is never white.
