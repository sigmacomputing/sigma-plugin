# Chart: funnel (stage conversion)

Stages narrowing in size — leads to won, visits to purchases — where the
question is how many get through each step. Shares of a whole are
`blocks/chart-composition.md`; a ranking is `blocks/chart-ranked.md`.

Stages must be nested — everything in a stage also passed the one before. Counts
of distinct users per stage are not (a later stage can draw wider): use a bar chart.

The source is **one row per record with a stage column**; the chart sums the
measure per stage. Sort by a `Stage no` for business order — unsorted it runs
widest first, which only matches when every stage is smaller than the last.

```python
fn = sec.add_funnel_chart(src)
fn.set_frame(1, 3, 24, 12)   # H = 14; a shorter card → SKILL.md's section-card rule
fn.set_stage(fn.get_column_by_name('<STAGE>'))
fn.get_column_by_name('<STAGE>').set_filter(sigma.filter.values(['<STAGE 1>', '<STAGE 2>', '<STAGE 3>']))
fn.set_values([(sigma.formula.sum(fn.get_column_by_name('<AMOUNT>')), '<Measure>')])
fn.set_sort_by_calculation('stage', sigma.formula.min(fn.get_column_by_name('<STAGE NO>')), ascending=True)
fn.set_color_scale((sigma.formula.sum(fn.get_column_by_name('<AMOUNT>')), 'Shade'))
fn.color_scale_scheme().set_palette([EDGE, SERIES_MID])
vl = fn.value_labels()
vl.set_visible(True)
vl.set_color(INK)
fn.legend().set_visible(False)
fn.title_style().set_visible(False)
fn.set_background_color(None)
fn.set_padding(False)
```

- The `values` filter names the stages to keep; a blank stage otherwise draws
  an unlabeled bar at the top.
- `set_palette` takes exactly two colors for a sequential ramp — a third makes
  it diverging.
- The ramp is `EDGE → SERIES_MID`, not `TINT → SERIES`: labels sit inside the
  bar in one color, and `INK` is weak on the dark end of the full ramp. A bar
  too narrow for its figure draws unlabeled — usually the last stage — so put
  its number in the card's subline: a `p-small` `sec.add_text` framed
  `(1, 2, 18, 1)` whose `{{Last}}` binds
  `(sigma.formula.sum_if(<base AMOUNT>, sigma.formula.eq(<base STAGE>, sigma.formula.const_text('<LAST STAGE>'))), sigma.format.format('number', 0))`
  over `base`'s columns, not the chart's.

- **Conversion rates** ("what share moves on"): drop the two color-scale lines
  and `vl.set_color`, then `fn.conversion_labels().set_visible(True)` and
  `fn.set_conversion_basis('prior')`. Labels read `443.53M, 6.56%` at the bar's right. A color scale, color
  category or several values turns them off, so these bars take the default
  colors — say so in the report.
- Never `set_color_category` or `set_category_palette`: coloring by the stage
  column splits each stage and collapses the funnel into one stacked bar.
- Tiers stored as separate **measure columns** can feed `set_values` (one `sum`
  each, no `set_stage`), but each bar takes its own default color and there are
  no conversion labels, so it cannot meet the palette rule. Prefer a stage
  column; if the data forces this form, say so in the report.
- 3–7 stages; merge the tail past that.
