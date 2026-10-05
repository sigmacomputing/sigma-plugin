# Chart: waterfall (bridge)

Opening figure on the left, one signed step per driver, closing figure on the
right — how a variance is made up. There is no waterfall element: it is a
stacked bar with an invisible plinth holding each step at its running height.
Use for a bridge, a variance walk, a build-up, or "start here, end there".

The source is **one row per step, in order**: a small helper table on the data
page, never the fact table. It needs a `Step no` to sort by, a short `Step`
label, a signed `Impact`, and a `Kind` of `open` / `step` / `close`. The
`open` row's `Impact` is the opening figure; **the `close` row's is 0** — its
bar is the running total, which is the closing figure by construction, so
putting the figure there doubles it. The four bar columns are computed on
that table, not on the chart:

```python
wfd = data_page.add_table(<STEPS SOURCE>)
wfd.set_name('Bridge steps')
wfd.set_frame(1, 13, 24, 12)
wfd.set_sort([sigma.sort.ascending(wfd.get_column_by_name('Step no'))])
imp = wfd.get_column_by_name('Impact')
step = sigma.formula.eq(wfd.get_column_by_name('Kind'), sigma.formula.const_text('step'))
rise = sigma.formula.gt(imp, sigma.formula.const_num(0))
run = wfd.add_column('Running', sigma.formula.cumulative_sum(sigma.formula.sum(imp)))
# the plinth is the lower edge of this step's bar: running height less the part
# that rises above it. const_null, never 0 — a 0 segment still paints a hairline
# sliver on top of every bar. greatest() returns an untyped Formula, so it needs
# number() before subtract (blocks/formulas.md)
wfd.add_column('Plinth', sigma.formula.if_(step,
    sigma.formula.subtract(sigma.formula.number(run),
        sigma.formula.number(sigma.formula.greatest(imp, sigma.formula.const_num(0)))),
    sigma.formula.const_null()))
wfd.add_column('Rise', sigma.formula.if_(step,
    sigma.formula.if_(rise, sigma.formula.number(imp), sigma.formula.const_null()),
    sigma.formula.const_null()))
wfd.add_column('Fall', sigma.formula.if_(step,
    sigma.formula.if_(rise, sigma.formula.const_null(), sigma.formula.abs(imp)),
    sigma.formula.const_null()))
wfd.add_column('Anchor', sigma.formula.if_(step,
    sigma.formula.const_null(), sigma.formula.number(run)))
```

```python
wf = sec.add_bar_chart(wfd.to_source())
wf.set_frame(1, 3, 24, 12)   # H = 14; a shorter card → SKILL.md's section-card rule
wf.set_dimension(wf.get_column_by_name('Step'))
wf.set_sort_by_calculation('dimension', sigma.formula.min(wf.get_column_by_name('Step no')), ascending=True)
wf.set_series([                          # top of the stack first — the plinth goes last
    (sigma.formula.sum(wf.get_column_by_name('Rise')), 'Step up'),
    (sigma.formula.sum(wf.get_column_by_name('Fall')), 'Step down'),
    (sigma.formula.sum(wf.get_column_by_name('Anchor')), 'Opening and closing'),
    (sigma.formula.sum(wf.get_column_by_name('Plinth')), 'Plinth'),
])
bars = wf.list_series()
bars[0].set_format('currency_si', decimals=1, currency='$')
bars[1].set_format('currency_si', decimals=1, currency='$')
bars[2].set_format('currency_si', decimals=1, currency='$')
wf.set_stacking('stacked')
wf.set_series_color(bars[0], '#008236')      # a rise is good, a fall is bad — the one
wf.set_series_color(bars[1], '#c10007')      # chart that takes the semantic pair
wf.set_series_color(bars[2], SERIES_GREY)    # the anchors are not a driver
wf.set_series_color(bars[3], '#ffffff')      # the plinth, painted out against the card
wf.dimension_axis().set_label_angle(0)
wf.value_axis().set_marks('none')
wf.legend().set_visible(False)            # it would name the plinth
wf.title_style().set_visible(False)
wf.set_background_color(None)
wf.set_padding(False)
```

- **`set_series` paints the last series at the bottom of the stack**, so the
  plinth goes last and the order above is the order to keep.
- The plinth is `'#ffffff'` because it hides against the card, so a waterfall
  only ever sits on a white card — never a callout, a loud band, or the canvas.
- Labels are why bridges look broken: `SKILL.md` forbids rotating them and a
  waterfall cannot go horizontal, so keep `Step` to a word or two in the
  helper table — `sigma.formula.switch_` over the long driver names — rather
  than shrinking the type.
- 3–8 steps reads; past that the drivers stop being distinguishable and the
  small ones belong in one `Other` step.
- The closing anchor is the opening plus every step by construction, so if it
  does not foot, the helper table is wrong and no amount of rebuilding the
  chart will fix it — `query` the step rows and check the total first.
