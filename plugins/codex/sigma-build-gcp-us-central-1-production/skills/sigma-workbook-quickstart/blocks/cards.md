# Card list (repeater)

One card per row or group — a catalog, a feed, a work queue, or **a summary
card per entity** (per rep, per region, per product). The default way to show
a modest set of records: under ~200 rows a card list reads better than a
table, and any band that would otherwise be the same card design built three
or more times is one. Cards hold text, buttons, dividers, and plain
containers — no table, chart, KPI, control, tabbed container, nested
repeater, or **value list** (the SDK binds a card's value list to the whole
source, not to the card, whatever `layoutHost.py` says). The card's own grid
is a **fixed 12 columns**; every value on it is a text bound to a column of
the repeater's source.

One card per entity starts with a **one-row-per-entity table on the data
page**: grouped, with its facts as grouping calculations, text-typed and
pre-formatted (`blocks/formulas.md`, "Pre-format for prose"):

```python
lst = data_page.add_table(src)
lst.set_name('<Entity> list')
lst.set_frame(1, 13, 24, 8)
lg = lst.set_groupings([lst.get_column_by_name('<ENTITY>')])[0]
lg.set_calculation('Value text', sigma.formula.ampersand(sigma.formula.const_text('$'), sigma.formula.ampersand(sigma.formula.text(sigma.formula.round(sigma.formula.divide(sigma.formula.sum(lst.get_column_by_name('Revenue')), sigma.formula.const_num(1000000)), 1)), sigma.formula.const_text('M'))))
lg.set_calculation('Meta', sigma.formula.ampersand(sigma.formula.text(sigma.formula.count_distinct(lst.get_column_by_name('<KEY>'))), sigma.formula.const_text(' ORDERS')))
lg.set_calculation('Kind', sigma.formula.max(lst.get_column_by_name('<CATEGORY>')))
key = lg.keys()[0]
```

Then the repeater, on the page or inside a section card:

```python
cards = sec.add_repeater(lst.to_source())
cards.set_frame(1, 3, 24, 23)              # three rows of cards; 15 for two, 30 for four
cards.set_grouping(lg)                     # one card per group — omit over a row-grain source
cards.set_card_layout('grid')
cards.set_card_size('medium')
cards.set_scroll_type('vertical')          # the frame is fixed; the rest scrolls
cards.set_card_background_color('#ffffff')
cards.set_card_border(sigma.border.solid(width=1, color=HAIRLINE, radius='round'))
cards.set_background_color(None)           # the BOX the cards sit in
cards.set_padding(False)                   # ...and its padding
cards.set_spacing('small')                 # ...and the gap between cards
cards.set_card_padding(True)               # the CARDS' own padding — required
cards.set_card_spacing('small')            # element gap stays on — off, every card locks to a 5-row box
cn = cards.add_text('**{{Name}}**', formulas={'Name': key})
cn.set_frame(1, 1, 12, 1)
cm = cards.add_text('<p class="p-small"><span style="color: ' + MUTED + '">{{Meta}}</span></p>', formulas={'Meta': lst.get_column_by_name('Meta')})
cm.set_frame(1, 2, 12, 1)
rule = cards.add_divider()
rule.set_frame(1, 3, 12, 1)
rule.set_color(HAIRLINE)
ce = cards.add_text('<p class="p-small"><span style="color: ' + MUTED + '">Revenue</span></p>')
ce.set_frame(1, 4, 12, 1)
cv = cards.add_text('**{{Value}}**', formulas={'Value': lst.get_column_by_name('Value text')})
cv.set_frame(1, 5, 12, 1)                  # the last row of the 5-row card
```

- A card is a **5-row box** (30px rows) whatever its template — fewer rows
  leave dead space under the content, a sixth grows it — so every template
  ends on row 5. Frames: on `'grid'` 15 rows show two rows of cards, 23
  three, 30 four; on `'list'` 20 rows show three cards, +7 per extra card.
  Never `set_element_gap(False)` on a repeater.
- A repeater over a filtered queue opens empty sooner or later — give it
  `cards.set_no_data_label('NO PENDING ITEMS')` rather than a blank band.
- Filter through the **source table** (a control targeting `lst`). Sorting
  has **no SDK call yet** and the table's own sort does not reach the cards
  — they come in query order. Cards take no conditional formats or
  theme-token card colors (hex only).
- **Two styling surfaces, and mixing them is the classic bug**: the inherited
  `Element` methods style the **box the cards sit in**, `set_card_*` styles
  each card — without `set_card_padding(True)` every card renders flush to
  its edges.
- On `'grid'`, card size sets the width and so how many fit across —
  `'small'` 150–250px · `'medium'` 250–400 (≈5 across a full-width
  repeater) · `'large'` 400–600 (≈3); on `'list'` every card is a row.
- **A sentence per card is a column**, never prose written N times — a
  grouping calculation, or for a real per-card narrative a guarded
  `call_text('ai_complete', …)` calculation cleaned with `regexp_replace`
  (`blocks/insight-ai.md` carries the guard). Hand-building (the
  authored-copy exception in SKILL.md step 2) caps at three or four cards.
- A **chip** in a card is a button bound to a column —
  `cards.add_button('{{Kind}}', formulas={'Kind': lst.get_column_by_name('Kind')})`
  · solid · pill · small · `'#ffffff'` fill, `BODY` text on a `FILL` card.
  Its fill cannot vary *by* the value.

## On the page

A Portfolio dashboard's cards sit on the page under a label, not in a
section card — the calls above, framed for two rows of five:

```python
cl = page.add_text('**<Per-entity label>**')
cl.set_frame(1, y, 24, 1)
cards = page.add_repeater(src)
cards.set_frame(1, y + 1, 24, 9)          # one row of five; 15 for two rows — band 10 or 16
cards.set_scroll_type('vertical')          # the rest scroll
```

## List rows

A contained list — holdings, accounts, deals, queue items — as **one card
16 columns wide**: search and a segmented filter on the card's first two
rows, then one `FILL` row per record with a key tile, the name over a muted
meta line, a chip, and the value flush right under a `VALUE` eyebrow.
`lst` and `lg` as above, plus `Tile` =
`sigma.formula.upper(sigma.formula.left(key, sigma.formula.const_num(3)))`.

```python
sec = page.add_container()                 # the section card, no label — the search is the header
sec.set_frame(1, y, 16, 29)                # two control rows + the repeater's
sec.set_column_density('high')
sec.set_spacing('small')
sec.set_background_color('#ffffff')
sec.set_border(sigma.border.solid(width=1, color=HAIRLINE, radius='round'))
find = sigma.control.add_text_control(sec, target=lst.get_column_by_name('<ENTITY>'), match_mode='contains', case_sensitive=False, placeholder='<Entity> name')
find.set_name('Search')
find.set_frame(1, 1, 12, 2)
seg = sigma.control.add_segmented_control(sec, options=['<A>', '<B>', '<C>'], target=lst.get_column_by_name('<CATEGORY>'))   # up to 4 options at this width — more collapses to a dropdown; use a list control instead
seg.set_name('<Category>')
seg.set_frame(14, 1, 11, 2)
cards = sec.add_repeater(lst.to_source())  # the repeater calls above, with:
cards.set_frame(1, 3, 24, 27)              # four cards; 20 for three, +7 per extra card
cards.set_card_layout('list')
cards.set_card_background_color(FILL)
cards.set_card_border(None)
tile = cards.add_text('<p class="p-small" style="text-align: center">**{{Tile}}**</p>', formulas={'Tile': lst.get_column_by_name('Tile')})
tile.set_frame(1, 2, 1, 3)                 # rows 2–4: the row's content sits centered in the 5-row card
tile.set_vertical_align('middle')
tile.set_background_color('#ffffff')
tile.set_border(sigma.border.solid(width=1, color=HAIRLINE, radius='round'))
nm = cards.add_text('**{{Name}}**', formulas={'Name': key})
nm.set_frame(2, 2, 5, 1)
nm.set_vertical_align('bottom')
mt = cards.add_text('<p class="p-small"><span style="color: ' + MUTED + '">{{Meta}}</span></p>', formulas={'Meta': lst.get_column_by_name('Meta')})
mt.set_frame(2, 3, 5, 1)
mt.set_vertical_align('top')
chip = cards.add_button('{{Kind}}', formulas={'Kind': lst.get_column_by_name('Kind')})
chip.set_frame(7, 2, 3, 2)                 # 3 columns — a real category name truncates in 2
chip.set_appearance('solid')
chip.set_shape('pill')
chip.set_button_size('small')
chip.set_fill_color('#ffffff')
chip.set_font_color(BODY)
ve = cards.add_text('<p class="p-small" style="text-align: right"><span style="color: ' + MUTED + '">VALUE</span></p>')
ve.set_frame(10, 2, 3, 1)
ve.set_vertical_align('bottom')
vv = cards.add_text('<p class="p-small" style="text-align: right">**{{Value}}**</p>', formulas={'Value': lst.get_column_by_name('Value text')})
vv.set_frame(10, 3, 3, 1)
vv.set_vertical_align('top')
```

The controls target `lst`, so the list filters without re-scoping the
page; a control's label always renders — name it for the reader, never
`''`.

## Card feed

The list card at page width, each record carrying its own action — deals to
forecast, items to review, stores to open. No tile and no search card, so the
card re-frames across its 12 columns — the repeater calls above, with:

```python
cards = page.add_repeater(lst.to_source())
cards.set_frame(1, y, 24, 22)              # three cards; 20 without the third line
cards.set_card_layout('list')
cards.set_card_background_color('#ffffff')
cards.set_card_border(sigma.border.solid(width=1, color=HAIRLINE, radius='round'))
cards.set_no_data_label('NO <RECORDS> MATCH')
nm = cards.add_text('**{{Name}}**', formulas={'Name': key})
nm.set_frame(1, 2, 6, 1)
nm.set_vertical_align('bottom')
mt = cards.add_text('<p class="p-small"><span style="color: ' + MUTED + '">{{Meta}}</span></p>', formulas={'Meta': lst.get_column_by_name('Meta')})
mt.set_frame(1, 3, 6, 1)
mt.set_vertical_align('top')
sub = cards.add_text('<p class="p-small"><span style="color: ' + MUTED + '">{{Kind}}</span></p>', formulas={'Kind': lst.get_column_by_name('Kind')})
sub.set_frame(1, 4, 6, 1)                  # the third line — drop it and frame the repeater 20
sub.set_vertical_align('top')
ve = cards.add_text('<p class="p-small" style="text-align: right"><span style="color: ' + MUTED + '">VALUE</span></p>')
ve.set_frame(7, 2, 3, 1)
ve.set_vertical_align('bottom')
vv = cards.add_text('<p class="p-small" style="text-align: right">**{{Value}}**</p>', formulas={'Value': lst.get_column_by_name('Value text')})
vv.set_frame(7, 3, 3, 1)
vv.set_vertical_align('top')
go = cards.add_button('Review →')          # soft (blocks/buttons.md) — unstyled renders Sigma blue
go.set_frame(10, 3, 3, 2)
go.set_align('right')
go.set_appearance('solid')
go.set_shape('round')
go.set_button_size('small')
go.set_fill_color(TINT)
go.set_font_color(PRIMARY)
go.on_click('open', [sigma.action.navigateEffect.navigate_to(<PAGE>)])
```

- A **third content line grows the card**: the list rule's 20 rows for three
  cards becomes 22. The trailing row cannot be reclaimed.
- A card's button reaches a **page or an overlay, never a row** — an
  effect's value binds to the whole source, so a card cannot hand its own
  record to a picker or a detail panel (`blocks/detail.md`).
- The same repeater runs **inside a drawer or modal**, on a container in
  it — `set_card_border(None)` on a `FILL` card.
