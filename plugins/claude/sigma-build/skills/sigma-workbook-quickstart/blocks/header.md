# Header

The identity strip — white, a hairline, the workbook's subject as the
lockup. **Band** for one page, **panel** for 2+ reading
pages (the shell table); three or more reading pages and every app take the
rail and strip of `blocks/sidebar.md` instead — what is never built is two
navs. Both variants here carry the `Assistant` popover trigger
(`blocks/chat.md`).

## Band — single-page

```python
band = home.add_container()
band.set_frame(1, 1, 24, 2)
band.set_column_density('high')
band.set_spacing('small')
band.set_background_color('#ffffff')
band.set_border(sigma.border.solid(width=1, color=HAIRLINE, radius='round'))
brand = band.add_text('**<What the workbook is>**<span style="color: ' + MUTED + '"> · <its scope></span>')   # **Revenue planning** · FY26
brand.set_frame(1, 1, 14, 2)
brand.set_vertical_align('middle')
marker = band.add_text('<p class="p-small" style="text-align: right"><span style="color: ' + MUTED + '">Overview</span></p>')
marker.set_frame(15, 1, 5, 2)
marker.set_vertical_align('middle')
ai = sigma.workbook.add_popover(band, 'Assistant')   # fill it per blocks/chat.md
trig = ai.trigger()
trig.set_text('Assistant')
trig.set_appearance('text')
trig.set_font_color(MUTED)
trig.set_frame(20, 1, 5, 2)
trig.set_align('right')
```

## Shared panel + nav — multi-page

Panel calls live on `Page`, which is what `add_page` returns — so every
page of the fixed opening hosts one directly. Controls and buttons never sit
on the panel itself — on a container in it.

```python
header = scenarios.add_header()              # scenarios came from add_page
header.set_background_color('#ffffff')
header.set_border_style('line')
header.set_scroll_behavior('fixed')          # navigation requires a fixed header
lockup = header.add_text('**<What the workbook is>**<span style="color: ' + MUTED + '"> · <its scope></span>')
lockup.set_frame(1, 1, 8, 2)
lockup.set_vertical_align('middle')
nav = header.add_navigation()                # auto: follows visible pages
nav.set_frame(9, 1, 7, 2)
nav.set_alignment('right')
nav.set_style('pill')
nav.set_text_color(MUTED)
nav.set_selected_color(PRIMARY)
hc = header.add_container()                  # structural, but it keeps its gap — the picker and the trigger must not touch
hc.set_frame(16, 1, 9, 2)
hc.set_column_density('high')
hc.set_padding(False)
hc.set_spacing('small')
hc.set_background_color(None)
hc.set_border(None)
pick = sigma.control.add_list_control(hc, target=base.get_column_by_name('<PERIOD OR SCENARIO>'), allows_multi=False)
pick.set_name('<Period>')                    # two words — a blank name renders the raw column name; only when describe returned such a column, else drop it
pick.set_frame(1, 1, 16, 2)
ai = sigma.workbook.add_popover(hc, 'Assistant')   # fill it per blocks/chat.md
trig = ai.trigger()
trig.set_text('Assistant')
trig.set_appearance('text')
trig.set_font_color(MUTED)
trig.set_frame(17, 2, 8, 1)                  # row 2 — level with the picker's input, not its label (blocks/filters.md)
trig.set_align('right')

home.set_header(header)                      # every page the nav covers, one for one
sigma.workbook.set_page_tabs_hidden_in_view_mode(True)
```

- The lockup is what the workbook is and for whom — `**Revenue planning** ·
  FY26`, `**Pipeline review** · Sales` — never an invented product name and
  never "Dashboard". A logo goes in front of it only when the user gives a
  URL: `mark = band.add_image('<URL>')` at `(1, 1, 1, 2)` (`(1, 1, 1, 1)` on
  the panel), the lockup one column right and one narrower; no styling calls, never
  the `'placeholder'` preset, a stock photo.
- The header grid is 24 columns and grows to its content, hard cap 8 rows
  — keep it to the two rows above, which is what a labelled control needs.
  The band's marker names the current page.
- Hide tabs **only** after the nav reaches every visible page (auto mode
  does; the hidden data page needs no link).
