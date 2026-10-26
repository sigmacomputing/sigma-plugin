# Insight callout

One `TINT` strip that says what moved, with live values woven into the sentence. Place it under the hero or the KPI row; write real synthesis, not a metric restated.

```python
note = page.add_container()
note.set_frame(1, y, 24, 3)
note.set_column_density('high')
note.set_spacing('small')
note.set_background_color(TINT)
note.set_border(sigma.border.solid(width=1, color=EDGE, radius='round'))
nl = note.add_text('<p class="p-small"><span style="color: ' + PRIMARY + '">What moved</span></p>')
nl.set_frame(1, 1, 24, 1)
rev = sigma.formula.sum(base.get_column_by_name('Revenue'))
tgt = sigma.formula.sum(base.get_column_by_name('Target'))
money = sigma.format.format('currency_si', 1, '$')
nb = note.add_text(
    '<p class="p-small"><span style="color: ' + INK + '">The quarter stands at **{{Total revenue}}** against a **{{Target}}** plan — a **{{Gap}}** gap, and <the driver, named> carries most of it. <One clause on what that means for the decision>; take it to <the action it informs — the override grid, the review page>.</span></p>',
    formulas={                                 # (formula, format) — bound bare, sum() renders 287243281.43
        'Total revenue': (rev, money),
        'Target': (tgt, money),
        'Gap': (sigma.formula.subtract(tgt, rev), money),
    })
nb.set_frame(1, 2, 24, 2)
nb.set_vertical_align('middle')
```

- All `formulas=` bind **`base`'s** columns; a placeholder name is free-form and may repeat a column name (only `(formula, name)` calcs must avoid collisions).
- A one-sentence body fits `nb.set_frame(1, 2, 24, 1)` with card height 2; the two-row body shown holds the full 2–4 sentence synthesis.
