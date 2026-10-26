# Tab switcher

Two depths of one section — the picture and the numbers behind it (chart ↔
table), a summary ↔ the rows it totals, a roll-up ↔ its breakdown. The tab
bar is hidden and quiet text buttons on the card's label row drive it, so
the card reads as one surface with a switch rather than as two bands.
Stepping a **flow** rather than swapping a view is the same container with
the steps as tabs (`blocks/wizard.md`).

```python
tc = sec.add_tabbed_container()
tc.set_frame(1, 2, 24, 13)     # row 2 = the card's subline row: drop the subline, or start at y=3 height 12
tc.set_column_density('high')
tabs = tc.list_tabs()                      # a new tabbed container has 3 tabs
chart_tab = tabs[0]
chart_tab.set_name('Chart')
table_tab = tabs[1]
table_tab.set_name('Table')
tabs[2].delete()                           # always account for all three
tc.set_tab_bar_visible(False)              # the buttons drive it
tc.set_padding(False)
tc.set_gap(False)

show_chart = sec.add_button('Chart')       # quiet switchers on the label row
show_chart.set_frame(19, 1, 3, 1)
show_chart.set_appearance('text')
show_chart.set_button_size('small')
show_chart.set_align('right')
show_chart.set_font_color(MUTED)
show_chart.set_bold(False)
show_table = sec.add_button('Table')
show_table.set_frame(22, 1, 3, 1)
show_table.set_appearance('text')
show_table.set_button_size('small')
show_table.set_align('right')
show_table.set_font_color(MUTED)
show_table.set_bold(False)
show_chart.on_click('show chart', [sigma.action.selectTabEffect.select_tab(chart_tab)])
show_table.on_click('show table', [sigma.action.selectTabEffect.select_tab(table_tab)])
```

Fill each tab like a page region (`chart_tab.add_line_chart(src)` …, frames on
its 24-column grid, height ≈ container − 2).

- Cheap variant — keep the bar, skip the buttons and the three hide calls:
  `tc.set_tab_style('button')`, `tc.set_tab_bar_size('small')`, `tc.set_tab_alignment('end')`.
- `select_tab` also takes a `(tc, 'next')` / `(tc, 'previous')` pair — clamped at the ends, no wraparound.
- Elements go into tabs, never the tabbed container itself.
- Switchers are buttons, never a segmented control — its chrome fights the quiet label row; the cheap variant above is the visible-strip route.

## Tabbed main — the page as two or more full views

Two or more whole views of one dataset (by region · by product · by stage):
the tabbed container is the page **body** — the wide column of a full-height
split, or full bleed where there is no rail. **It** is the card and carries
the surface; everything inside a tab is structural. Card the tab's contents
instead and the bar floats above a boxed inset, a card inside a card.

```python
tc = page.add_tabbed_container()
tc.set_frame(6, y, 19, 30)        # beside a 5-column rail; (1, y, 24, 30) with none
tc.set_column_density('high')
tc.set_tab_style('button')
tc.set_tab_bar_size('small')
tc.set_background_color('#ffffff')
tc.set_border(sigma.border.solid(width=1, color=HAIRLINE, radius='round'))
```

Fill each tab as above — first element at row 1, the bar sitting above the
tab's grid rather than in it, the last ending at `height − 2`. A section
card inside a tab keeps its frames and swaps its fill and border for
`set_padding(False)` + `set_gap(False)` — structural, like everything in a tab.
