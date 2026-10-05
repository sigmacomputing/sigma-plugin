# KPI row

Band of 3–5 KPIs — the scoreboard under the title. Widths by count — 3: `8/8/8` at x `1,9,17` · 4: `6×4` at `1,7,13,19` · 5: `5/5/5/5/4` at `1,6,11,16,21`.
All KPIs in a row share one height: 5 rows (with or without a comparison), 10 with a sparkline — and the band is exactly that tall. SKILL.md's Dashboards row names which variant below a page takes.

```python
kpis = page.add_container()
kpis.set_frame(1, y, 24, 5)
kpis.set_column_density('high')
kpis.set_spacing('small')
kpis.set_background_color(None)            # structural: the KPIs read straight on the canvas — the cards below carry the lines
kpis.set_border(None)
kpis.set_padding(False)                    # labels align with the page title's left edge

k1 = kpis.add_kpi(src)
k1.set_frame(1, 1, 8, 5)
k1.set_name('Revenue')                     # the KPI's own title — never a text element above it
k1.set_value((sigma.formula.sum(k1.get_column_by_name('Revenue')), 'Total revenue'))
k1.get_column_by_name('Total revenue').set_format('currency_si', decimals=1, currency='$')
k1.title().set_color(MUTED)
k1.title().set_font_size(14)
k1.title().set_bold(False)
k1.value_style().set_color(INK)
k1.value_style().set_font_size(24)
k1.value_style().set_bold(True)
k1.layout().set_anchor('left')
k1.layout().set_vertical_anchor('top')     # a KPI without a comparison otherwise floats to the middle
k1.set_background_color(None)
k1.set_padding(False)
k1.set_comparison((sigma.formula.sum(k1.get_column_by_name('Target')), 'plan'))   # renders "vs plan" — the vs is added for you; the name is a calc column, so never a source column's name in any case
k1.comparison_style().set_direction('higher')
k1.comparison_style().set_good_color('#008236')
k1.comparison_style().set_bad_color('#c10007')
k1.comparison_style().set_label_color(MUTED)
```

- Next KPIs: build each one the long way — `k2 = kpis.add_kpi(src)`, then the same `set_frame`, `set_name`, `set_value((formula, '<new unique name>'))`, format, and style calls. `k1.duplicate()` looks cheaper and is not: it drops the copy one row *below* the original, past the band's inner grid, and the container keeps the doubled height — re-asserting `kpis.set_frame(...)` afterwards does not shrink it back.
- **Percent**: format `('percent', decimals=1)`; a rate is `sigma.formula.divide(sigma.formula.sum_if(col, cond), sigma.formula.sum(col2))`.
- **Count**: `sigma.formula.count(col)` / `count_distinct(col)`, format `('number', decimals=0)`. A count with nothing to compare against still takes context — the prior-period timeline below, or the band's status sentence. Never `set_comparison(None)`: a label and a bare figure tell the reader nothing about whether it is good, and a KPI without context fills two rows of a five-row band, leaving a visible gap under it.
- **Prior-period comparison** (needs a date): the timeline is the date
  **truncated to the comparison grain** — `km = k1.add_column('Trend month', sigma.formula.date_trunc('month', k1.get_column_by_name('<DATE>')))`
  · `t = k1.trend()` · `t.set_timeline(km)` · `t.set_visible(False)` · then
  `k1.set_comparison('month')` and no `set_label` (the label writes itself:
  "Sep vs Aug, 2026"). The raw date column instead renders one day's value
  under a timestamp label. With a timeline the value **is the latest
  period's**, not the total — a partial current period reads as a drop, so
  when step 3's max date sits mid-period, compare to a column instead. A
  judged measure gets `set_comparison` + direction.
- **Sparkline** (10-row KPI): the same truncated timeline with the trend left
  visible — `t.set_shape('area')` · `t.set_area_style('gradient')` ·
  `t.set_value_color(SERIES)` — `SERIES`, not `PRIMARY`; the value reads the
  latest period, the line the history behind it.
- **Stat cards** — when each KPI carries its own one-line reading: one
  card per KPI instead of the shared band, `6` wide at x `1,7,13,19`,
  height 6 — the section-card calls, the KPI above at `(1, 1, 24, 4)`, and
  a `MUTED` `p-small` line at `(1, 5, 24, 2)` saying what the number means
  ("Trailing month against the one before."). Never mix the two shapes in
  one band. Each card repeats the `k1` calls under its own container
  handle — never `duplicate()` across cards.
- **Focus tile** (at most one per page) — a KPI reversed on `PRIMARY`
  so one metric carries the eye. It is its own element on
  the page beside a 17-wide band, at `(18, y, 7, 10)` with a sparkline, not
  inside the KPI band: `set_background_color(PRIMARY)`
  · `set_border(sigma.border.solid(radius='round'))` (no line — a loud surface)
  · value `#ffffff` at 30 · title `EDGE` (muted on the fill — ink and body
  go unreadable on it). A sparkline on the tile takes
  `t.set_value_color('#ffffff')`. Everything else is the KPI above, minus
  `set_padding(False)` — the tile is its own surface, so it keeps its padding.
  A subline under the title has to be a text element inside the same
  structural wrapper: `description()` exists on tables and charts, **not**
  on KPI.
- **Strip variant** — the white section card comes back (the dividers need a
  surface), so the padding does too: drop `kpis.set_padding(False)` and each
  KPI's, or the first value sits hard against the card's border. Hairline
  dividers instead of gaps: KPIs 6
  wide at x `1,8,15`, with `d = kpis.add_divider('vertical')` ·
  `d.set_frame(7, 1, 1, 5)` · `d.set_color(HAIRLINE)` between them (and at
  x 14). **With a status sentence**, the KPIs narrow to 4 at x `1,6,11`
  (dividers at x 5, 10, 15) and the sentence takes `(16, 1, 9, 5)` —
  `st = kpis.add_text(...)`, `set_vertical_align('middle')`, a `MUTED`
  `p-small` with its values bolded — plus, on an app only, a small action
  button in its last columns: a scoreboard that ends in the next step.
