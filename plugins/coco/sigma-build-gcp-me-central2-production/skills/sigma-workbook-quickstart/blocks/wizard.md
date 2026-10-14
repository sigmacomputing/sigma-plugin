# Wizard — a modal stepping through tabs

A stepped flow (name it, set parameters, review) in a modal: a hidden-bar
tabbed container holds the steps, marker buttons walk them.

```python
wiz = sigma.workbook.add_modal('New scenario')
wiz.set_width('large')
wiz.set_header(title='', show_close_icon=True)   # the body carries the title
wiz.set_footer_buttons(show_primary=False, show_secondary=False)  # per-tab nav instead
wt = wiz.add_text('<p class="p-large">**<New scenario>**</p>')
wt.set_frame(1, 1, 12, 2)
ws = wiz.add_text('<p class="p-small"><span style="color: ' + MUTED + '">Three steps, then it shows up in the library.</span></p>')
ws.set_frame(1, 3, 12, 1)

wtc = wiz.add_tabbed_container()
wtc.set_frame(1, 5, 12, 12)
wtc.set_column_density('medium')           # keep the modal's 12-column rhythm
steps = wtc.list_tabs()                    # a new tabbed container has 3 tabs — account for all three
step_basics = steps[0]
step_basics.set_name('Basics')
step_params = steps[1]
step_params.set_name('Parameters')
step_review = steps[2]
step_review.set_name('Review')
wtc.set_tab_bar_visible(False)
wtc.set_background_color(None)
wtc.set_padding(False)
wtc.set_gap(False)

s1 = wiz.add_button('① Basics')            # step markers: centered strip with
s1.set_frame(3, 4, 2, 1)                   # hairline separators
s1.set_appearance('text')
s1.set_align('stretch')
s1.set_font_color(BODY)
sd1 = wiz.add_divider('vertical')
sd1.set_frame(5, 4, 1, 1)
sd1.set_color(HAIRLINE)
s2 = wiz.add_button('② Parameters')
s2.set_frame(6, 4, 2, 1)
s2.set_appearance('text')
s2.set_align('stretch')
s2.set_font_color(BODY)
sd2 = wiz.add_divider('vertical')
sd2.set_frame(8, 4, 1, 1)
sd2.set_color(HAIRLINE)
s3 = wiz.add_button('③ Review')
s3.set_frame(9, 4, 2, 1)
s3.set_appearance('text')
s3.set_align('stretch')
s3.set_font_color(BODY)
s1.on_click('step 1', [sigma.action.selectTabEffect.select_tab(step_basics)])
s2.on_click('step 2', [sigma.action.selectTabEffect.select_tab(step_params)])
s3.on_click('step 3', [sigma.action.selectTabEffect.select_tab(step_review)])

h1 = step_basics.add_text('**Name the scenario**')     # step content sits in a
h1.set_frame(3, 1, 8, 1)                               # centered 8-of-12 column
nm = sigma.control.add_text_control(step_basics, placeholder='<Something a reviewer will recognise>')
nm.set_name('Scenario name')               # no target: variable-only, filters nothing
nm.set_frame(3, 2, 8, 2)
go1 = step_basics.add_button('Continue →')
go1.set_frame(8, 9, 3, 2)
go1.set_appearance('solid')
go1.set_shape('round')
go1.set_fill_color(PRIMARY)
go1.set_font_color('#ffffff')
go1.on_click('to parameters', [sigma.action.selectTabEffect.select_tab(step_params)])

h2 = step_params.add_text('**Set the parameters**')
h2.set_frame(3, 1, 8, 1)
case = sigma.control.add_segmented_control(step_params, options=['Conservative', 'Base', 'Stretch'], value='Base')
case.set_name('Growth case')               # options are manual — no target to derive from
case.set_frame(3, 2, 8, 2)
back2 = step_params.add_button('← Back')   # neutral fill, left
back2.set_frame(3, 9, 3, 2)
back2.set_appearance('solid')
back2.set_shape('round')
back2.set_fill_color(FILL)
back2.set_font_color(BODY)
back2.on_click('to basics', [sigma.action.selectTabEffect.select_tab(step_basics)])
go2 = step_params.add_button('Continue →')
go2.set_frame(8, 9, 3, 2)
go2.set_appearance('solid')
go2.set_shape('round')
go2.set_fill_color(PRIMARY)
go2.set_font_color('#ffffff')
go2.on_click('to review', [sigma.action.selectTabEffect.select_tab(step_review)])

h3 = step_review.add_text('**Review the setup**')
h3.set_frame(3, 1, 8, 1)
back3 = step_review.add_button('← Back')
back3.set_frame(3, 9, 3, 2)
back3.set_appearance('solid')
back3.set_shape('round')
back3.set_fill_color(FILL)
back3.set_font_color(BODY)
back3.on_click('to parameters', [sigma.action.selectTabEffect.select_tab(step_params)])
done = step_review.add_button('Done')
done.set_frame(8, 9, 3, 2)
done.set_appearance('solid')
done.set_shape('round')
done.set_fill_color(PRIMARY)
done.set_font_color('#ffffff')
done.on_click('close', [sigma.action.overlayEffects.close_overlay()])

opener = page.add_button('+ New scenario')
opener.set_frame(19, 2, 6, 2)              # title rows 1–4; under a single-page header band the title is rows 3–6: (19, 4, 6, 2)
opener.set_align('right')
opener.set_appearance('solid')
opener.set_shape('round')
opener.set_fill_color(PRIMARY)
opener.set_font_color('#ffffff')
opener.on_click('new scenario', [sigma.action.selectTabEffect.select_tab(step_basics), sigma.action.overlayEffects.open_overlay(wiz)])
```

- The opener selects step 1 before opening, so the wizard never resumes mid-flow.

## Form modal — one step, one record

Create a record from a `+ New …` button without leaving the page: a modal
holding a form over the input table (`it` from `blocks/input-table.md`,
built first — on the hidden data page, `data_page.add_input_table(...)`,
when no band shows it, with two seed rows), the form's own submit doing
the insert.

```python
m = sigma.workbook.add_modal('New goal')
m.set_width('small')
m.set_header(title='Set a new milestone', show_close_icon=True)
m.set_footer_buttons(show_primary=False, show_secondary=False)   # the form's submit is the footer
form = m.add_form(it)
form.set_frame(1, 1, 12, 16)                 # 3 rows per field + 4
form.set_title('')
form.set_description('<One line on what the record is for.>')
form.set_submit_label('Create goal')         # the outcome, never "Submit"
form.set_reset_visible(False)
form.set_submit_button_alignment('stretch')
form.set_spacing('medium')
form.set_background_color(None)
saved = form.on_submit('saved', [sigma.action.refreshElementEffect.refresh_element(it), sigma.action.overlayEffects.close_overlay()])
saved.set_success_toast(title='Goal created')
cancel = m.add_button('Cancel')            # quiet secondary under the stretched submit
cancel.set_frame(1, 17, 12, 2)
cancel.set_appearance('text')
cancel.set_align('stretch')
cancel.set_font_color(MUTED)
cancel.set_bold(False)
cancel.on_click('cancel', [sigma.action.overlayEffects.close_overlay()])
m.on_close('reset', [sigma.action.clearControlEffect.clear_control(m)])
opener.on_click('new', [sigma.action.overlayEffects.open_overlay(m)])   # opener: blocks/buttons.md — a title-row action, or a card's soft button
```

Field defaults and dropdown presentation as `blocks/intake.md` shows.
- A formula **cannot reference a control's live value** — a review step
  cannot echo the chosen inputs. Keep step 3 to a static summary and the
  actions; live *data* state comes from the context-strip's
  filtered-aggregate trick, not from controls.
- Replace the `done.on_click('close', …)` line to commit the controls as a
  row — controls are action values:
  `done.on_click('save', [sigma.action.inputTableEffects.insert_row(it, {i_name: nm, i_case: case}), sigma.action.refreshElementEffect.refresh_element(it), sigma.action.overlayEffects.close_overlay()])`
  (`it` from `blocks/input-table.md`; `i_case` a single-select column added
  for the case), then a toast on the sequence. Close resets the inputs:
  `wiz.on_close('reset', [sigma.action.clearControlEffect.clear_control(wiz)])`.
