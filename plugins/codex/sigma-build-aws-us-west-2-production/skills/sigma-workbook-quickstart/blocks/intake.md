# Intake app — form beside the log

The reader logs, submits, requests, tracks, enters. Pages **Log · Overview**
under the sidebar rail (`blocks/sidebar.md`).

| Page | Band | Block | Frame (the card) |
|---|---|---|---|
| Log | title + dynamic chip `{{n}} pending` | `blocks/title.md` | rows 1–4 |
| Log | left card: the form | fence below | `(1, 5, 8, H)` — H = 5 × fields + 3 |
| Log | right card: the input table, seeded | `blocks/input-table.md` empty table, `set_frame(1, 3, 24, H - 2)` inside the card | `(9, 5, 16, H)` |
| Overview | over `it.to_source()`: KPI row 24·5 (count, open, due this month) → Pair 14/10 14: trend by `Needed by` · stacked by status → table 24·14. A fresh log spans one or two periods, so the trend has no marks to draw: until it covers 3+, drop that band and take the composition full width. An ask naming on-time or outstanding filing also gets a roster band — the entity spine left-joined to `it.to_source()` with a `Filed` flag, never a typed cohort size | `blocks/kpi-row.md` · `blocks/chart-trend.md` · `blocks/chart-composition.md` · `blocks/table.md` | rows 5+ |

Build the input table (its card is the right column) before the form:

```python
card = log_page.add_container()                # left column, a card because it holds copy
card.set_frame(1, 5, 8, 28)                    # 5 x fields + 3, so 5 fields → 28
card.set_column_density('high')
card.set_spacing('small')
card.set_background_color('#ffffff')
card.set_border(sigma.border.solid(width=1, color=HAIRLINE, radius='round'))
form = card.add_form(it)                       # one field per editable column; submit appends the row
form.set_frame(1, 1, 24, 28)                   # the form is the card's only child: same H, no trailing row
form.set_title('New request')
form.set_description('Say what you need and when; approvals land on the right.')
form.set_submit_label('Save request')          # the outcome, never "Submit"
form.set_reset_visible(False)
form.set_submit_button_alignment('stretch')
form.set_spacing('medium')
form.set_title_font_size(20)
form.set_background_color(None)
form.get_field_by_name('Needed by').set_default(sigma.formula.today())
f_status = form.get_field_by_name('Status')
if isinstance(f_status, SelectFormField):      # a select column arrives as radio buttons
    f_status.set_presentation('dropdown')
    f_status.set_default('Pending')
saved = form.on_submit('saved', [sigma.action.refreshElementEffect.refresh_element(it)])   # the built-in insert stays
saved.set_success_toast(title='Request saved')
```

- **6 or more fields goes in a modal, no exceptions** — inline, the form
  outgrows the fold and the Save button falls off the card. It moves behind
  a `+ New <record>` button in the title row
  (`blocks/wizard.md`, Form modal), and the input-table card takes the full
  `(1, 5, 24, H)`.
- The input table **is** the base: no warehouse source, no base table on
  the data page (the opening's `base` and `src` lines drop out; `data_page`
  stays for helper tables) — unless the ask reconciles what people type against a
  source ("where it doesn't line up with what we shipped, flag the gap"), in
  which case that page is a **linked** table over the source
  (`blocks/input-table.md`, Linked) and the gap is a formula column, not a
  second thing to type — `src = it.to_source()` after the seed rows, and the
  Overview's KPIs, charts, and table are built on it exactly as a
  dashboard's are.
- A survey or questionnaire ask keeps this shape; take question wording from
  `sdk://skills/survey/SKILL.md` and nothing else from it.
