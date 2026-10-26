# Compare strip

A white card holding a text grid — two states of the same measures side by side with the delta, read in one glance (baseline vs working plan, last vs this quarter). Header row of centered muted labels, one row per measure, delta column in `PRIMARY`.

```python
cs = page.add_container()
cs.set_frame(1, y, 24, 2)          # header row + one measure row; +1 per extra measure
cs.set_column_density('high')
cs.set_spacing('small')
cs.set_background_color('#ffffff')
cs.set_border(sigma.border.solid(width=1, color=HAIRLINE, radius='round'))
h1 = cs.add_text('<p class="p-small" style="text-align: center"><span style="color: ' + MUTED + '">**<Baseline>**</span></p>')
h1.set_frame(7, 1, 6, 1)
h2 = cs.add_text('<p class="p-small" style="text-align: center"><span style="color: ' + MUTED + '">**<Current>**</span></p>')
h2.set_frame(13, 1, 6, 1)
h3 = cs.add_text('<p class="p-small" style="text-align: center"><span style="color: ' + MUTED + '">**Change**</span></p>')
h3.set_frame(19, 1, 6, 1)
r1 = cs.add_text('<p class="p-small"><span style="color: ' + MUTED + '">**Revenue**</span></p>')
r1.set_frame(1, 2, 6, 1)
r1.set_vertical_align('middle')
money = sigma.format.format('currency_si', 1, '$')
tgt = sigma.formula.sum(base.get_column_by_name('Target'))
rev = sigma.formula.sum(base.get_column_by_name('Revenue'))
r1b = cs.add_text(                         # (formula, format) — bound bare, sum() renders 287243281.43
    '<p class="p-small" style="text-align: center"><span style="color: ' + INK + '">{{Baseline}}</span></p>',
    formulas={'Baseline': (tgt, money)})
r1b.set_frame(7, 2, 6, 1)
r1b.set_vertical_align('middle')
r1c = cs.add_text(
    '<p class="p-small" style="text-align: center"><span style="color: ' + INK + '">**{{Current}}**</span></p>',
    formulas={'Current': (rev, money)})
r1c.set_frame(13, 2, 6, 1)
r1c.set_vertical_align('middle')
r1d = cs.add_text(
    '<p class="p-small" style="text-align: center"><span style="color: ' + PRIMARY + '">**{{Change}}**</span></p>',
    formulas={'Change': (sigma.formula.subtract(rev, tgt), money)})
r1d.set_frame(19, 2, 6, 1)
r1d.set_vertical_align('middle')
```

- Derive the delta with `sigma.formula.subtract(current, baseline)`; its color stays `PRIMARY` — it is a value, not a verdict (good/bad ink belongs to conditional formats on tables).
- One measure per row, patterned exactly on the row shown; each extra measure adds one row and one row of card height (2 measures → height 3).
- The working state always reads heavier than the reference — current bold, baseline regular.
- Every `{{...}}` binds over **`base`'s** columns; placeholder keys are per-element, so every row reuses 'Baseline' / 'Current' / 'Change'.
- Past ~4 measures this stops being a glance — use a table card instead.
