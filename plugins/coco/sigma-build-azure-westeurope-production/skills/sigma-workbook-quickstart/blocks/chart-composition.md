# Chart: composition

How a total splits across categories, month by month. Earns its place only when
the categories are the subject and there are at most ~6 of them — verify the
count with `query` first; filter or group the tail.

```python
mix = sec.add_bar_chart(src)
mix.set_frame(1, 3, 24, 12)   # H = 14; a shorter card → SKILL.md's section-card rule
mo = mix.add_column('Mix month', sigma.formula.date_trunc('month', mix.get_column_by_name('<DATE COL>')))
mo.set_format_pattern('%b %Y')
mix.set_dimension(mo)                          # columns never cross elements
mix.set_series([(sigma.formula.sum(mix.get_column_by_name('Amount')), 'Total amount')])
mix.set_color_category(mix.get_column_by_name('<CATEGORY>'))
mix.set_category_color('<CATEGORY VALUE>', SERIES)   # one per value, largest first: SERIES SERIES_MID SERIES_GREY EDGE TINT — the donut's rule below
mix.set_stacking('stacked')
mix.dimension_axis().set_marks('none')
mix.dimension_axis().set_label_angle(0)
mix.value_axis().set_marks('none')
mix.legend().set_position('right')
mix.title_style().set_visible(False)
mix.set_background_color(None)
mix.set_padding(False)
```

- Share-of-total: `mix.set_stacking('percent')`.

Donut — static composition, the same ≤6 cap, on the user's ask or when the
Dashboards row or the Charts table names it:

```python
d = sec.add_donut_chart(src)
d.set_frame(1, 3, 24, 12)   # H = 14; a shorter card → SKILL.md's section-card rule
d.set_category(d.get_column_by_name('<CATEGORY>'))
d.set_values([(sigma.formula.sum(d.get_column_by_name('Revenue')), 'Total revenue')])
d.get_column_by_name('Total revenue').set_format('currency_si', decimals=1, currency='$')
d.set_hole_value((sigma.formula.sum(d.get_column_by_name('Revenue')), 'Total'))
d.get_column_by_name('Total').set_format('currency_si', decimals=1, currency='$')
d.hole().set_size(0.7)
d.legend().set_position('right')
d.title_style().set_visible(False)
d.set_background_color(None)
d.set_padding(False)
```

- `hole().set_size` takes 0.4–0.8; the hole shows `'Total'` — the figure the
  slices are shares of.
- Slice colors are set per category, as every chart sets its own:
  `d.set_category_color('<CATEGORY VALUE>', SERIES)` — one call per slice,
  every slice named, largest first: `SERIES` `SERIES_MID` `SERIES_GREY`
  `EDGE` `TINT`; none left to the workbook palette.

## Ribbon — tiers that live in separate columns

When the split is across **measures**, not a categorical column, drop the
dimension entirely: one horizontal bar at `percent` stacking reads as a
progress ribbon. This is the funnel/gauge shape — pipeline tiers, budget
committed/spent/remaining, capacity used/free, roles filled/offered/open.

**Difference nested tiers first** or the stack double-counts — if Commit
already contains Closed won, stack the increments, not the raw tiers:

```python
base.add_column('Commit (net)', sigma.formula.subtract(
    sigma.formula.zn(base.get_column_by_name('Commit')),
    sigma.formula.zn(base.get_column_by_name('Closed won'))))
# one per tier; the last is Total minus the tier before it

rib = sec.add_bar_chart(src)
rib.set_frame(1, 3, 24, 6)                 # no set_dimension — that is the trick
rib.set_series([                           # top of the stack first: set_series paints the LAST series at the bottom
    (sigma.formula.sum(rib.get_column_by_name('Remaining pipe')), 'Pipeline'),
    (sigma.formula.sum(rib.get_column_by_name('Commit (net)')), 'Commit'),
    (sigma.formula.sum(rib.get_column_by_name('Closed won')), 'Closed'),
])
rib.set_orientation('horizontal')
rib.set_stacking('percent')
t = rib.list_series()
rib.set_series_color(t[0], TINT)            # one hue stepped up — a certainty
rib.set_series_color(t[1], SERIES_MID)      # ramp, never unrelated colors
rib.set_series_color(t[2], SERIES)
dl = rib.data_labels()
dl.set_visible(True)
dl.set_as_percent(True)
dl.set_precision(0)
dl.set_color(BODY)
rib.dimension_axis().set_show_labels(False)
rib.dimension_axis().set_marks('none')
rib.value_axis().set_show_labels(False)
rib.value_axis().set_marks('none')
rib.legend().set_visible(False)
rib.title_style().set_visible(False)
rib.set_background_color(None)
rib.set_padding(False)
```

- **`series[0]` renders at the right end** of a horizontal percent stack, so
  list the tiers least-certain first and the ramp reads dark→pale left to
  right. Smoke-tested; getting this backwards inverts the whole chart.
- The bar carries percentages only, so give each tier a hand-built legend
  cell under it at row 9 — `● Tier` in its own color, the value as
  `<p class="p-large">**…**</p>`, a muted `p-small` count — three or four across the card at width 6. Use
  `EDGE` for the palest tier's **dot**: `TINT` reads as
  nothing on white.
- Card height 9 — label 1, subline 2, ribbon 3–8, legend 9. Leave no
  trailing row.
- One series alone is a **coverage meter** ("62% of quota"): same calls,
  a single ratio series.
