# Chart: waterfall (bridge)

Opening figure on the left, one signed step per driver, closing figure on the
right — how a variance is made up. Use for a bridge, a variance walk, a
build-up, or "start here, end there". The native `add_waterfall_chart` draws
it: increases green, decreases red, totals grey, and it works when the running
total crosses zero.

The source is **one row per step, in order**: a small helper table on the data
page, never the fact table. It needs a `Step no` to sort by, a short `Step`
label, and a signed `Impact`; the first row's `Impact` is the opening figure.
**No closing row** — the chart appends its own `End` total, the opening plus
every step, and a row for it draws a stray empty step.

```python
wfd = data_page.add_table(<STEPS SOURCE>)
wfd.set_name('Bridge steps')
wfd.set_frame(1, 13, 24, 12)
```

```python
wf = sec.add_waterfall_chart(wfd.to_source())
wf.set_frame(1, 3, 24, 12)   # H = 14; a shorter card → SKILL.md's section-card rule
wf.set_dimension(wf.get_column_by_name('Step'))
wf.set_series([(sigma.formula.sum(wf.get_column_by_name('Impact')), 'Impact')])
wf.set_sort_by_calculation('dimension', sigma.formula.min(wf.get_column_by_name('Step no')), ascending=True)
wf.set_name('')   # blanked, not hidden — the card's label and subline carry the title
wf.list_series()[0].set_format('currency_si', decimals=1, currency='$')
wf.set_background_color(None)
wf.set_padding(False)
```

- No legend, axis, title-style, stacking, series-color or data label
  setters — do not call them. The title cannot be hidden: blank it, and the
  card's label and subline are the title and subtitle. It leaves a short
  empty band above the bars.
- Step labels draw rotated and cannot be changed, and a long one is cut off
  with an ellipsis, so keep `Step` to a word or two in the helper table —
  `sigma.formula.switch_` over the long driver names.
- The value axis starts at zero, so steps that are small against the opening
  figure draw thin bars. Zoom it on a bar chart, then convert — the range
  carries over, and every call above then applies to `wf`:

```python
bc = sec.add_bar_chart(wfd.to_source())   # the dimension, series and sort calls above, on bc
sc = bc.value_axis().scale()
if isinstance(sc, LinearScale):
    sc.set_range(min=<FLOOR>)             # just under the lowest running total
wf = bc.convert_to('waterfall')
```
- Keep the default colors. `add_conditional_color` on the series recolors the
  opening bar too, so a rule would turn it green.
- 3–8 steps reads; past that the drivers stop being distinguishable and the
  small ones belong in one `Other` step.
- The `End` bar is the opening plus every step by construction, so if it does
  not foot to the real closing figure, the helper table is wrong and no amount
  of rebuilding the chart will fix it — `query` the step rows and check the
  total first.
