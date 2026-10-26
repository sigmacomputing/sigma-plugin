# Sidebar rail + strip

The app shell, shared by every page: a white fixed **rail** down the left —
lockup, vertical navigation, who is signed in — and a two-row **strip**
across the top carrying the one workbook-wide picker and the `Assistant`.
Use it when the shell table's row is *acts* or *reads across three or more
views*. The rail holds **destinations only**; anything that is not a page
goes on the strip. Pages under this shell skip `blocks/header.md` — the
strip carries no navigation, and two navs is the one thing never built.

## Rail — identity and destinations

```python
# panel calls live on Page, which add_page returns — create the rail on one
# page and attach it to each of the others (blocks/header.md)
side = plan_page.add_sidebar()
side.set_background_color('#ffffff')
side.set_border_style('line')
side.set_scroll_behavior('fixed')
side.set_width('medium')
lockup = side.add_text('**<What the app is>**')          # **Revenue planning** — the lockup rule in blocks/header.md
lockup.set_frame(1, 1, 6, 2)
lockup.set_vertical_align('middle')
tagline = side.add_text('<p class="p-small"><span style="color: ' + MUTED + '"><its scope — FY26 · Plugs Electronics></span></p>')
tagline.set_frame(1, 3, 6, 1)
group = side.add_text('<p class="p-small"><span style="color: ' + MUTED + '">Main</span></p>')
group.set_frame(1, 5, 6, 1)
nav = side.add_navigation()
nav.set_frame(1, 6, 6, 8)                    # 2.5 rows per visible page, rounded up — the bullets below
nav.set_orientation('vertical')
nav.set_style('pill')
nav.set_alignment('left')
nav.set_text_color(MUTED)
nav.set_selected_color(PRIMARY)
foot = side.add_divider()                    # who is signed in — the rail's last rows
foot.set_frame(1, 20, 6, 1)
foot.set_color(HAIRLINE)
who = side.add_text('<p class="p-small">**{{Who}}**<br><span style="color: ' + MUTED + '">{{Mail}}</span></p>', formulas={'Who': sigma.formula.current_user_full_name(), 'Mail': sigma.formula.current_user_email()})
who.set_frame(1, 21, 6, 2)

home.set_sidebar(side)                       # every page the rail covers
review_page.set_sidebar(side)
```

## Strip — scope and the Assistant

The rail's companion on the same pages, flush right. Controls and buttons
never sit on the panel itself — on the container `hc`.

```python
strip = plan_page.add_header()               # the page the rail was created on
strip.set_background_color('#ffffff')
strip.set_border_style('line')
strip.set_scroll_behavior('fixed')
hc = strip.add_container()                   # structural, but it keeps its gap — the picker and the trigger must not touch
hc.set_frame(13, 1, 12, 2)
hc.set_column_density('high')                # 24 inner columns
hc.set_padding(False)
hc.set_spacing('small')
hc.set_background_color(None)
hc.set_border(None)
pick = sigma.control.add_list_control(hc, target=base.get_column_by_name('<PERIOD OR SCENARIO>'), allows_multi=False)
pick.set_name('<Period>')                    # the control's own label names what it scopes — no text label beside it, and never a blank name (blocks/filters.md)
pick.set_frame(1, 1, 15, 2)                  # only when describe returned such a column; else drop it, shrink hc to (19, 1, 6, 2), and give ask (1, 2, 24, 1)
ai = sigma.workbook.add_popover(hc, 'Assistant')   # fill it per blocks/chat.md
ask = ai.trigger()                           # a popover has no action to open it — its trigger is the button
ask.set_text('Assistant')
ask.set_frame(16, 2, 9, 1)                   # row 2 — level with the picker's input, not its label (blocks/filters.md)
ask.set_appearance('solid')                  # the soft button of blocks/buttons.md — an action, never nav ink
ask.set_shape('round')
ask.set_button_size('small')
ask.set_align('right')
ask.set_fill_color(TINT)
ask.set_font_color(PRIMARY)

home.set_header(strip)                       # the rail's pages, one for one
review_page.set_header(strip)
sigma.workbook.set_page_tabs_hidden_in_view_mode(True)
```

- Rail and strip attach to the **same** pages — every `set_sidebar` gets a
  `set_header`. A page with one and not the other loses its nav or its scope.
- The sidebar grid is a **fixed 6 columns** whatever its pixel width;
  `set_width('small'|'medium'|'large')` changes pixels only — 200/260/400px.
  It grows as tall as its content — stack top-down, no bottom anchoring. The
  strip is 24 columns; keep it to the two rows above.
- A vertical nav option is ~52px, so the rail's nav takes **2.5 rows per
  visible page, rounded up** — 3 pages 8, 4 pages 10, 6 pages 15. Frame it
  short and the pages past the fold do not clip, they hide behind a scroll
  nobody goes looking for, so the app reads as though it had fewer pages —
  count the pages and take the number above, never the 6 that fits three.
  `set_option_size('small')` buys about one more page per 12 rows. The nav
  can grow to row 19 before `foot` and `who` move down with it.
- A panel must be **assigned to a page before elements go in** — creating it
  via `page.add_sidebar()` / `page.add_header()` (as above) satisfies that; a
  panel has no `set_padding`/`set_border`/`set_spacing` of its own, its inset
  is theme-fixed. Elements can be added to it at any point in the program.
- The rail's text is `INK` and `MUTED`; the nav marks the current page in
  `PRIMARY` via `set_selected_color`. `ask` is the shell's only tinted
  surface — nothing else on either panel carries the hue.
- Title blocks start at row 1, body `y` 5. Page filters stay on the page —
  the strip's picker re-scopes every page. Hide workbook tabs only once the
  nav reaches every visible page (auto nav does).
- Six or more pages: a second group label one row under the first nav and a
  `manual`-mode navigation below that for the pages that are not the work —
  `Resources` over README and Data, so `Main` lists only where the reader
  goes to work. Size each nav to its own page count and move `foot` and
  `who` below both. `manual` is **seed-and-prune**: it starts from the
  visible pages, and an option can only be `delete()`d — there is no call
  that adds, relabels, or retargets one.
