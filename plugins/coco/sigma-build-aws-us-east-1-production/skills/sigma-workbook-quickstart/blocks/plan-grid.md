# Plan grid app — edit a plan against a baseline

The reader edits a forecast, budget, plan, headcount, quota, territory.
Pages **Overview · Plan · Review** under the sidebar rail
(`blocks/sidebar.md`). The grid is the page:
a linked table over the baseline at plan grain, editable overrides beside
the computed plan and delta.

| Page | Band | Block | Frame (the card) |
|---|---|---|---|
| Overview | title: greeting + eyebrow naming the period | `blocks/title.md` | rows 1–4 |
| Overview | next-action hero — statement + one button `Open the plan →` wired `navigate_to(plan_page)` | `blocks/hero.md` statement + CTA | `(1, 5, 24, 5)` |
| Overview | KPI row over `lt.to_source()` — calcs `'Total plan'` · `'Total baseline'` · `'Net delta'` | `blocks/kpi-row.md` | `(1, 10, 24, 5)` |
| Overview | pending changes: cards over `pend = data_page.add_table(lt.to_source())` with `ed = pend.add_column('Edited', sigma.formula.if_(sigma.formula.is_not_null(pend.get_column_by_name('Rationale')), sigma.formula.const_num(1), sigma.formula.const_num(0)))` · `ed.set_filter(sigma.filter.values([1]))` (a values filter rejects booleans); family, rationale, and pre-formatted Plan · Delta text; `set_no_data_label('NOTHING PENDING')` | `blocks/cards.md` | `(1, 15, 24, 10)`. Seed `Rationale` on ≤6 rows — this card is the rows a person touched, so a rationale on every row empties it of meaning. Quotas may be seeded on all of them |
| Plan | title + `Submit for review` primary button at cols 19–24 | `blocks/title.md` · `blocks/buttons.md` | rows 1–4 |
| Plan | context strip — edits count, net delta; drop its `sel` and `btn` (the sidebar strip's `pick` is the picker) | `blocks/context-strip.md` | `(1, 5, 24, 2)` |
| Plan | the grid, seeded | `blocks/input-table.md` linked | `(1, 7, 24, 18)` |
| Plan | compare strip Baseline · Plan · Change | `blocks/compare-strip.md` over `lt.to_source()` | `(1, 25, 24, 2)` |
| Review | title | `blocks/title.md` | rows 1–4 |
| Review | decision log `log` — Plan, Status pills, Note, system columns; 2 seed rows. **The decision is made inline**, in those editable columns — no approval panel beside it: `log`'s only row selector is its generated `i_id`, and nothing can hand a picker an id a reader would recognise (`blocks/detail.md`) | `blocks/input-table.md` empty | `(1, 5, 24, 12)` |
| Review | decisions by outcome, with the status sentence | `blocks/kpi-row.md` strip variant over `log.to_source()` | `(1, 17, 24, 5)` |

Build order: Plan page (`sec`, `lt`) → Overview → Review (`log`, columns
`g_plan` text · `g_status` single-select Submitted · Approved · Needs
changes · `g_note` text) → then the `submit` wiring, whose effect needs `log`:

```python
submit = plan_page.add_button('Submit for review')   # primary button (blocks/buttons.md), cols 19–24 of the title band
submit.set_frame(19, 2, 6, 2)
submit.set_align('right')
submit.set_appearance('solid')
submit.set_shape('round')
submit.set_fill_color(PRIMARY)
submit.set_font_color('#ffffff')
sent = submit.on_click('submit', [
    sigma.action.inputTableEffects.insert_row(log, {g_plan: '<PLAN NAME>', g_status: 'Submitted', g_note: 'Sent from the plan page'}),
    sigma.action.refreshElementEffect.refresh_element(log),
])
sent.set_success_toast(title='Submitted for review', message='{{n}} edits · net {{d}}', formulas={
    'n': sigma.formula.count_if(sigma.formula.is_not_null(lt.get_column_by_name('Rationale'))),
    'd': sigma.formula.sum(lt.get_column_by_name('Delta')),
})
```

- A period in the ask (by month, by quarter) is `blocks/forecast.md`.
- `Adjustment %` is per row, not compounding. A column whose name contains
  cost, expense, or spend: favorable delta is negative — swap the good/bad
  tints on its Delta format.
- `Status` values on `log`: Submitted · Approved · Needs changes.
