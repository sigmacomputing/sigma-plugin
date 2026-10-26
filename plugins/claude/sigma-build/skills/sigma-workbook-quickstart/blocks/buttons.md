# Buttons

Three appearances, used beside the page title or under a card's content.

```python
go = page.add_button('Review plan →')
go.set_frame(19, 4, 6, 2)
go.set_align('right')                      # page actions end flush with the content's right edge
go.set_appearance('solid')                 # primary: PRIMARY, round
go.set_shape('round')
go.set_fill_color(PRIMARY)
go.set_font_color('#ffffff')

soft = page.add_button('+ New view')       # secondary: tint
soft.set_frame(14, 4, 5, 2)
soft.set_align('right')
soft.set_appearance('solid')
soft.set_shape('round')
soft.set_fill_color(TINT)
soft.set_font_color(PRIMARY)

quiet = page.add_button('Back to overview')  # tertiary: text only
quiet.set_frame(1, 1, 5, 2)                  # wherever it sits — frames never overlap
quiet.set_appearance('text')
quiet.set_font_color(MUTED)
quiet.set_bold(False)
```

Wire clicks with effects; `on_click` returns a sequence you can toast:

```python
target_page = sigma.workbook.get_page('<TARGET_PAGE_ID>')   # not the current page's id
seq = go.on_click('open review', [sigma.action.navigateEffect.navigate_to(target_page)])
# also: overlayEffects.open_overlay(drawer) / close_overlay(),
# selectTabEffect.select_tab(tab), openLinkEffect.open_link(url)
```

Decision panel — primary, soft, and a neutral third side by side in one
card row (`sec`), frames 8 wide at x `1/9/17`: the primary and soft take
the same calls as above plus `set_button_size('small')` and
`set_align('stretch')` (fill the 8-column frame); the neutral:

```python
changes = sec.add_button('Request changes')   # neutral: grey fill
changes.set_frame(17, 2, 8, 2)
changes.set_appearance('solid')
changes.set_shape('round')
changes.set_button_size('small')
changes.set_align('stretch')
changes.set_fill_color(FILL)
changes.set_font_color(BODY)
```

- A page-title action sits at columns 14–24 — rows 4–5 under an in-page
  band, rows 2–3 when the title rows are 1–4 (the title block shifts up;
  stay clear of its full-width rule).
- Confirm a click: `seq.set_success_toast(title='Opening review')` (optional `message=`, `{{name}}` via `formulas=`).
- A row click can branch on the clicked row's value:
  `tbl.on_select('open', [sigma.action.controlFlow.if_else([(sigma.action.condition.equals(tbl.get_column_by_name('<STATUS>'), 'Open'), [sigma.action.overlayEffects.open_overlay(drawer)])], [sigma.action.navigateEffect.navigate_to(done_page)])])`
  — conditions `equals greater_than less_than at_least at_most between is_null text_match` on a column; the else list may be empty.
- An effect's target must already exist, so wire each action after the page
  it points at — one program builds every page, so ordering is all it takes.
  Name any flow you could not wire.
- Decision buttons that write rows are wired in `blocks/queue.md` (a
  drawer) and `blocks/plan-grid.md` (a page button): effects run write →
  `refresh_element` → `close_overlay`, and the toast is set on the returned
  sequence. A status chip is a formula-labelled button with no action
  (`blocks/title.md`).
