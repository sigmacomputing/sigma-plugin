# Review queue app — decide record by record

The reader approves, rejects, triages, resolves, assigns. Pages **Queue ·
Done** under the sidebar rail (`blocks/sidebar.md`). The queue is the page: a linked input table over the records,
one row per key, with the decision editable inline and a drawer for the
focused decision.

| Page | Band | Block | Frame (the card) |
|---|---|---|---|
| Queue | title + dynamic chip `{{n}} to decide` — `sigma.formula.count_if(sigma.formula.is_null(l_dec))` | `blocks/title.md` | rows 1–4 |
| Queue | toolbar: decision segmented (no default) · owner list · search — targets the queue's own columns, ending at column 18 so the record picker takes 19–24 | `blocks/filters.md` toolbar | `(1, 5, 24, 2)` |
| Queue | the queue: linked table over a data-page table that keeps only open records — `qsrc.get_column_by_name('<STATUS>').set_filter(sigma.filter.values(['<OPEN>']))` and `qsrc.get_column_by_name('<DATE>').set_filter(sigma.filter.date_relative('last', 7, 'day'))` — keyed on the record id, `source_columns` = name, amount, date from `describe` (max 6), editable `Decision` pills · `Owner` · `Note`, formula `Age (days)`; step 5 seeds 2 rows with a Decision | `blocks/input-table.md` linked | `(1, 7, 24, 18)` |
| Queue | decision drawer, opened by a click on a queue row or by the record picker (`blocks/detail.md`) | fence below | overlay |
| Done | audit log `log` — Record, Decision, Note, `created_at`, `created_by` left visible; 2 seed rows | `blocks/input-table.md` empty | `(1, 5, 24, 6)` — `blocks/input-table.md`'s height arithmetic on its seed count, growing with the log, never a reserved 18 |
| Done | decisions by outcome, with the status sentence — the log has no comparison to offer | `blocks/kpi-row.md` strip variant over `log.to_source()` | `(1, 11, 24, 5)` |

Before the drawer, on the data page: `qsrc = data_page.add_table(src)` ·
`qsrc.set_name('Open records')` · `qsrc.set_frame(1, 13, 24, 12)` · the two
filters above · `qpick = data_page.add_table(qsrc.to_source())` ·
`qpick.set_name('Record picker')` · `qpick.set_frame(1, 26, 24, 6)` — the
picker's option source, nothing downstream of it; then `lt = sec.add_linked_input_table(qsrc.to_source(), lookup_columns={'<ID>': '<Record>'}, source_columns={...})`
with `l_dec = lt.add_single_select_column('Decision', ['Approved', 'Rejected', 'Needs changes'])`
(no decision = null = the queue; a decided row stays in the grid showing its decision, and the log on Done records it), `l_own = lt.add_editable_column('Owner', 'text')`,
`pk = lt.list_primary_key_columns()[0]` — `pk` is the card's key, the value the
row click sets, and the column the buttons write to; what the card shows and
the buttons send come from `card.list_columns()`, never `pk` or another `lt`
handle. It is also what the picker lists, so take `lookup_columns` from the
column a reader recognises wherever one is unique (`blocks/detail.md`);
on the Done page's card, `log = done_sec.add_input_table('<CONNECTION_ID>')` ·
`g_rec = log.add_editable_column('Record', 'text')` ·
`g_dec = log.add_single_select_column('Decision', ['Approved', 'Rejected', 'Needs changes'])` ·
`g_note = log.add_editable_column('Note', 'text')`, the rest as
`blocks/input-table.md`'s empty table. `money` = `blocks/formulas.md`'s money
over the card's amount column, `by['<Amount>']` below.

```python
drawer = sigma.workbook.add_drawer('Decide')
drawer.set_width('medium')
drawer.set_header(title='Decide', show_close_icon=True)
card = drawer.add_single_row_container(lt.to_source(), key_column=pk, initial_value='<FIRST KEY VALUE>')
card.set_frame(1, 1, 12, 10)                    # the drawer's whole body — a single row container is a container, so the note sits in it
card.set_column_density('medium')
card.set_padding(False)
card.set_gap(False)
by = {}                                         # list_columns() is in display order and the key is not always first — look each column up by name
for c in card.list_columns():
    by[c.name()] = c
name = card.add_text('<p class="p-large">**{{Name}}**</p>', formulas={'Name': by['<Record>']})
name.set_frame(1, 1, 12, 2)
facts = card.add_value_list(fields={            # lt is already one row per key, so the card's columns bind bare — no grouped helper, no aggregate
    'Amount': money,                            # over by['<Amount>']; a bare number column would bind unformatted
    'Owner': by['Owner'],
})
facts.set_layout('separated')
facts.set_background_color(None)
facts.set_frame(1, 3, 12, 3)
note = sigma.control.add_text_area_control(card, placeholder='Why?')
note.set_name('Note')
note.set_frame(1, 6, 12, 3)
approve = card.add_button('Approve')            # primary: PRIMARY (blocks/buttons.md)
approve.set_frame(1, 9, 4, 2)
approve.set_appearance('solid')
approve.set_shape('round')
approve.set_fill_color(PRIMARY)
approve.set_font_color('#ffffff')
reject = card.add_button('Reject')              # neutral fill
reject.set_frame(5, 9, 4, 2)
reject.set_appearance('solid')
reject.set_shape('round')
reject.set_fill_color(FILL)
reject.set_font_color(BODY)
ok = approve.on_click('approve', [              # write → log → refresh → close
    sigma.action.inputTableEffects.update_rows(lt, {pk: sigma.formula.text(by['<Record>'])}, {l_dec: 'Approved'}),
    sigma.action.inputTableEffects.insert_row(log, {g_rec: sigma.formula.text(by['<Record>']), g_dec: 'Approved', g_note: note}),
    sigma.action.refreshElementEffect.refresh_element(lt),
    sigma.action.overlayEffects.close_overlay(),
])
ok.set_success_toast(title='Approved', message='{{r}} approved', formulas={'r': by['<Record>']})
no = reject.on_click('reject', [
    sigma.action.inputTableEffects.update_rows(lt, {pk: sigma.formula.text(by['<Record>'])}, {l_dec: 'Rejected'}),
    sigma.action.inputTableEffects.insert_row(log, {g_rec: sigma.formula.text(by['<Record>']), g_dec: 'Rejected', g_note: note}),
    sigma.action.refreshElementEffect.refresh_element(lt),
    sigma.action.overlayEffects.close_overlay(),
])
no.set_success_toast(title='Rejected')
drawer.on_close('reset', [sigma.action.clearControlEffect.clear_control(note)])
pick = sigma.control.add_list_control(bar, target=qpick.get_column_by_name('<ID>'), allows_multi=False, allows_search=True)
pick.set_name('<Record>')                       # bar = the toolbar; qpick is a picker-only table, since a control listing the queue's own ids would narrow the queue
pick.set_frame(19, 1, 6, 2)                     # the toolbar's last slot
by_pick = pick.on_change('open from picker', [  # jump to a record the queue's filters hide; the same card and drawer as the click
    sigma.action.setSingleRowViewEffect.select_row(card, pick),
    sigma.action.overlayEffects.open_overlay(drawer),
])
by_pick.set_condition(sigma.formula.is_not_null(pick))   # clearing the picker also fires on_change — unguarded, the drawer opens empty
opens = lt.on_select('open', [                  # pk is lt's own column, so the click carries its row (blocks/detail.md)
    sigma.action.setControlValueEffect.set_control_value(pick, pk),   # the picker follows the click, and so does any table it filters
    sigma.action.setSingleRowViewEffect.select_row(card, pk),
    sigma.action.overlayEffects.open_overlay(drawer),
], column=pk)                                   # scoped to the key cell (blocks/detail.md)
```

- A drawer that also lists the record's own rows (calls, orders): add that
  table's key column to the picker's `target` (`blocks/detail.md`) — the click
  sets the picker, so the table follows it.
- `Age (days)` is `blocks/formulas.md`'s `age_days`, bound with
  `lt.add_formula_column('Age (days)', ...)` over `lt`'s date column.
- Cap the queue at the source, never on the linked table: the status and
  relative-date filters above; a date literal (`const_date`) fails at
  evaluation, a relative filter does not. Never key on a status or owner —
  those change. The status segmented control takes no `value=`: rows with
  no decision yet are the queue.
- The decision buttons go **inside** `card`, never beside it: a column
  reference resolves against the element hosting it, so `by['<Record>']` is the shown
  record's id in there. That is what the actions target — there is no control
  holding the record.
  Third decision (`Request changes`) = the neutral button again at
  `(9, 9, 4, 2)`, writing `'Needs changes'`.
