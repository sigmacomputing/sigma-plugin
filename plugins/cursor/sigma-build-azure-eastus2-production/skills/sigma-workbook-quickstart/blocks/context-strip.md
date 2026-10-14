# Context strip

One white strip announcing the page's active state — which scenario is live, how many overrides, the net effect — with the switcher and a quiet escape hatch in the same row. Earns its place on any page whose numbers depend on a selection.

```python
ctx = page.add_container()
ctx.set_frame(1, y, 24, 2)
ctx.set_column_density('high')
ctx.set_spacing('small')
ctx.set_background_color('#ffffff')
ctx.set_border(sigma.border.solid(width=1, color=HAIRLINE, radius='round'))
net = sigma.formula.sum_if(base.get_column_by_name('<IMPACT>'), sigma.formula.is_not_null(base.get_column_by_name('<OVERRIDE>')))
state = ctx.add_text(
    '<p class="p-small"><span style="color: ' + MUTED + '">Active scenario: </span><span style="color: ' + INK + '">**{{Scenario}}**</span><span style="color: ' + MUTED + '"> · {{Edits}} overrides · net </span><span style="color: ' + INK + '">**{{Impact}}**</span></p>',
    formulas={
        'Scenario': sigma.formula.max(base.get_column_by_name('<SCENARIO>')),
        'Edits': sigma.formula.count_if(sigma.formula.is_not_null(base.get_column_by_name('<OVERRIDE>'))),
        'Impact': sigma.formula.ampersand(sigma.formula.const_text('$'), sigma.formula.ampersand(sigma.formula.text(sigma.formula.round(sigma.formula.divide(net, sigma.formula.const_num(1000000)), 1)), sigma.formula.const_text('M'))),   # pre-formatted (blocks/formulas.md); a count binds bare
    })
state.set_frame(1, 1, 12, 2)
state.set_vertical_align('bottom')     # level with the control's input; the label takes row 1 (blocks/filters.md)
sel = sigma.control.add_list_control(ctx, target=base.get_column_by_name('<SCENARIO>'), allows_multi=False, value='<THE DEFAULT>')
sel.set_name('Active scenario')
sel.set_frame(13, 1, 6, 2)
# a list control can be cleared, and cleared it un-scopes the page. When the selection
# feeds a lookup or a model, use blocks/filters.md's segmented control instead (≤4
# values) — it has no clear affordance, so the page can never resolve against no scenario
btn = ctx.add_button('Switch scenario →')
btn.set_frame(19, 2, 6, 1)
btn.set_appearance('text')
btn.set_font_color(MUTED)
btn.set_bold(False)
btn.set_align('right')
btn.set_button_size('small')
```

- `{{Scenario}}` resolves to the active value because the control filters `base` — after the filter, `max` over the column returns the one selected name.
- Wire the button per `blocks/buttons.md` (usually navigate to the page where switching really happens); drop it when there is nowhere to go.
- The strip must never open empty — a `value=` default only when the first render still shows data.
- Everything inline in one `<p>` — it reads as a sentence, not a KPI row.
- Sits directly under the title rule, before the KPI row; the control spends row 1 on its label, so the sentence and the button settle onto row 2 with it.
