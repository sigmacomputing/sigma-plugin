# Record detail — pick a record, see the whole thing

Seeing one whole record is the move a reader reaches for first on any
table of records, so **every detail table on a work surface carries it**.
A **click cannot carry the row**: an effect's value is a literal, another
control's live value, or a formula over the *whole* element, and the SDK
has no Selection source — so a value read off the clicked row lands null
and the record renders blank. Trigger conditions do read the clicked row;
values never do. A **picker** sets the record instead. Three surfaces
hold it, and the reader's next move picks which:

| Surface | Reach for it when | Width |
|---|---|---|
| **Modal** — the default | reading one record, or a decision that must finish before the page is usable again | `'medium'`; `'x_small'` to confirm, `'large'` for a wizard (`blocks/wizard.md`) |
| **Drawer** | the list must stay readable beside it — scanning row after row, deciding down a queue (`blocks/queue.md`) | `'small' 'medium' 'large'` only |
| **Popover** | a few lines of "what am I looking at", opened from its own trigger — never from the picker | the bullets below |

The record is a **single-row container**: an element with its own frame
that is also a host, so text, value lists, KPIs, and buttons go inside it
and read the row it shows. `select_row` on the picker's `on_change` sets
that row; it opens on `initial_value` and holds the last row set, so
`initial_value` is a **real key from step 3** — the surface must read
correctly before anything is picked. The **key column is also what the
picker lists**, so key on the column a reader recognises — a name, a ref
— and fall back to an id only when nothing readable is unique. Controls
never sit on the overlay itself — on a container in it, and the picker on
the list's own card.

Its source is **one row per key**, the rule of `blocks/input-table.md`: a
grouped table, never a raw one. The container filters that source to the
key, so of its columns only the grouping key and the **calculations** hold
one value — the base columns trailing them render the literal text
`Multiple values`. Every attribute the card shows is a calculation too — a
label's is `sigma.formula.max`.

```python
one = data_page.add_table(src)             # the container's source
one.set_name('Record source')
one.set_frame(1, 49, 24, 8)                # a free data-page slot — the archetype's own bases take 13 through 37
g = one.set_groupings([one.get_column_by_name('<KEY>')])[0]
g.set_calculation('Total revenue', sigma.formula.sum(sigma.formula.multiply(one.get_column_by_name('<PRICE>'), one.get_column_by_name('<QTY>'))))
g.set_calculation('Orders', sigma.formula.count(one.get_column_by_name('<ORDER ID>')))
g.set_calculation('Owner', sigma.formula.max(one.get_column_by_name('<OWNER>')))

m = sigma.workbook.add_modal('Account detail')
m.set_width('medium')
m.set_header(title='Account detail', show_close_icon=True)
m.set_footer_buttons(primary_text='Done', show_primary=True, show_secondary=False)
body = m.add_container()
body.set_frame(1, 1, 12, 8)
body.set_column_density('medium')
body.set_padding(False)
body.set_gap(False)
card = body.add_single_row_container(one.to_source(), key_column=one.get_column_by_name('<KEY>'), initial_value='<FIRST KEY VALUE>')
card.set_frame(1, 1, 12, 8)
cols = card.list_columns()                 # its only column lookup: the key first, then the calculations in the order set above
key, rev, orders, owner = cols[0], cols[1], cols[2], cols[3]
name = card.add_text('<p class="p-large">**{{Name}}**</p>', formulas={'Name': key})
name.set_frame(1, 1, 12, 2)
facts = card.add_value_list(fields={       # a column binds bare — no aggregate, no text() wrapper; money and rates pre-format first (blocks/formulas.md)
    'Revenue': sigma.formula.ampersand(sigma.formula.const_text('$'), sigma.formula.ampersand(sigma.formula.text(sigma.formula.round(sigma.formula.divide(rev, sigma.formula.const_num(1000000)), 1)), sigma.formula.const_text('M'))),
    'Orders': orders,
    'Owner': owner,
})
facts.set_layout('separated')
facts.set_background_color(None)
facts.set_frame(1, 4, 12, 5)               # 2 rows per field, less one: 3 fields → 5, 4 → 7

m.on_primary_click('done', [sigma.action.overlayEffects.close_overlay()])

pick = sigma.control.add_list_control(sec, target=one.get_column_by_name('<KEY>'), allows_multi=False, allows_search=True)
pick.set_name('<Record>')                  # sec = the card holding the list; targeting `one` (the container's own source) leaves that list whole
pick.set_frame(17, 1, 8, 2)                # the card's label row, so its subline narrows to (1, 2, 16, 1)
pick.on_change('open detail', [
    sigma.action.setSingleRowViewEffect.select_row(card, pick),
    sigma.action.overlayEffects.open_overlay(m),
])
```

`pick`, `card`, and `m` are handles of the program that built them. From a
**later** call every one of them is re-fetched and narrowed first, because
`get_element` returns the base `Element` and `get_page` the base `PageBase`
— no `on_change`, and `open_overlay` rejects a page:

```python
page = sigma.workbook.get_page('<PAGE ID>')   # every id from the build's state dump
el = page.get_element('<CONTROL ID>')
ov = sigma.workbook.get_page('<MODAL ID>')
host = ov.get_element('<BODY ID>')
if not (isinstance(ov, Modal) and isinstance(host, Container)):
    raise RuntimeError('re-fetch')
card = host.get_element('<CARD ID>')
if not (isinstance(el, ListControl) and isinstance(card, SingleRowContainer)):
    raise RuntimeError('re-fetch')
el.on_change('open detail', [
    sigma.action.setSingleRowViewEffect.select_row(card, el),
    sigma.action.overlayEffects.open_overlay(ov),
])
```

- A button drives the same card with a constant:
  `b.on_click('<name>', [sigma.action.setSingleRowViewEffect.select_row(card, sigma.formula.const_text('<KEY VALUE>'))])`.
  Never open the overlay on `tbl.on_select`: the click cannot say which
  record, so it would open on whatever was last picked.
- The record's own **rows** under the card — its orders, its line items —
  need the room: `body.set_frame(1, 1, 12, 18)`, the card still `(1, 1, 12,
  8)`, that table at `(1, 9, 12, 10)`. Add its key column to the picker's
  `target` list (`target=[…, rows.get_column_by_name('<KEY>')]`) rather
  than adding a second control. Filter that table, never `base` — that
  would re-scope every page.
- A modal's footer styles itself — primary renders solid in the theme
  highlight (`PRIMARY`), secondary neutral — and **both CTAs show by
  default**, so a modal that supplies its own buttons hides them explicitly
  (`show_primary=False, show_secondary=False`, as the wizard does). A
  decision takes both: `set_footer_buttons(primary_text='Approve',
  show_primary=True, secondary_text='Cancel', show_secondary=True)` wired
  with `m.on_primary_click(...)` / `m.on_secondary_click(...)`.
- **Drawer** instead — the same body, swapping the three opening lines for
  `drawer = sigma.workbook.add_drawer('Account detail')` ·
  `drawer.set_width('medium')` ·
  `drawer.set_header(title='Account detail', show_close_icon=True)`, and
  `open_overlay(drawer)` on the picker. It has no footer, so its actions
  are buttons in the body (`blocks/queue.md`), and `set_width` takes only
  the three sizes above — a modal's `x_small`/`x_large` raise on one.
- **Info popover** — the "what am I looking at" affordance on a card's
  label row, quiet trigger included:
  ```python
  info = sigma.workbook.add_popover(sec, 'About this view')
  tip = info.add_text('<p class="p-small"><span style="color: ' + BODY + '"><What this shows, the filters in force, one caveat.></span></p>')
  tip.set_frame(1, 1, 12, 3)
  trig = info.trigger()
  trig.set_text('ⓘ')
  trig.set_appearance('text')
  trig.set_font_color(MUTED)
  trig.set_frame(23, 1, 2, 1)
  trig.set_align('right')
  ```
  A popover body caps near 40% of the viewport — a tip is a few lines; the
  one tall popover is the Assistant chat (`blocks/chat.md`).
- Decision buttons in the overlay write rows: `blocks/queue.md`.

## Record card — the picked row, on the page

The same container as an **8-column card beside the list** (pair 16/8)
instead of inside an overlay: pick a record and the card reads it, no
overlay to open — the shape a Ledger reaches for first, since the list
and the record then sit side by side. Only the wrapper changes — the
source, the `cols` unpack, and the bindings are the fence above, on those
same 12-wide frames: a
single-row container is 12 inner columns, and this one takes no density
call.

```python
g.set_calculation('Kind', sigma.formula.max(one.get_column_by_name('<CATEGORY>')))   # the fourth calculation on `one`, so index 4 below
card = page.add_single_row_container(one.to_source(), key_column=one.get_column_by_name('<KEY>'), initial_value='<FIRST KEY VALUE>')
card.set_frame(17, y, 8, 12)
card.set_background_color('#ffffff')
card.set_border(sigma.border.solid(width=1, color=HAIRLINE, radius='round'))
kind = card.list_columns()[4]
eye = card.add_text('<p class="p-small"><span style="color: ' + MUTED + '">{{Kind}}</span></p>', formulas={'Kind': sigma.formula.upper(sigma.formula.text(kind))})
eye.set_frame(1, 1, 12, 1)                 # the eyebrow takes row 1, so name moves to (1, 2, 12, 2) and facts to (1, 5, 12, 5)
go = card.add_button('<Next step> →')      # soft button, stretched (blocks/buttons.md)
go.set_frame(1, 11, 12, 2)
pick.on_change('pick', [sigma.action.setSingleRowViewEffect.select_row(card, pick)])   # the picker of the fence above, on the list's card
```

- Aligned label/value columns instead of the far-edge look:
  `facts.set_layout('grid')` + `facts.set_label_width(0.5)` — only `'grid'` layout draws label width.
