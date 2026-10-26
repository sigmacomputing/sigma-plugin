# Statement grid (P&L)

A P&L is not a table of the data — it is an **ordered list of lines**, some
read from accounts and some computed across them (gross profit, operating
income), each landing in a fixed place. No grouping or subtotal setting
produces that: gross profit is revenue *minus* cost of sales, arithmetic across
two sections, not a rollup inside one. So the statement is a **union of small
tables** — one for the detail lines, one per computed line — all sharing five
columns, stacked and then sorted by an ordinal. It is one band, sized to its
lines (SKILL.md's band rule carves it out).

## Two things step 3 must settle — a wrong answer here is silent

- **Section and ordinal per account.** The order comes from a number, so
  something must map account → section → sort position. A ledger fact table
  rarely carries it; the usual shape is a **join** to an account hierarchy on
  the account code, taking only its attributes — never a measure, or the
  aggregates fan out. With no hierarchy at all, map the sections yourself with
  `sigma.formula.switch_` and say so in the report: it is your reading, not the
  warehouse's.
- **The sign of costs.** `query` `SUM(amount)` grouped by section. Warehouses
  usually store costs **positive**, which is what `Signed` below normalises; if
  they are already negative, drop the `neg`. Getting this wrong doesn't error —
  it returns a plausible, wrong gross profit.

## Signed amounts — one rule, top to bottom

Sign every amount once, and every computed line becomes a plain sum. Because a
signed statement rises when things go well on *every* line, one variance rule
then reads correctly from revenue to net income. Without it you need
per-section polarity rules, and one missed section paints half the statement
backwards.

## Skeleton

Five shared columns — `Block` (section, `Subtotal`, or `Ratio`), `Label`,
`Ord`, `Actual`, `Plan`. Every table in the union exposes exactly these names;
`union_sources` matches by name and keeps only what every source has. Name the
calcs for the statement, not the warehouse: if the source itself has an
`Actual` or `Plan` column, the calc silently becomes `Actual (1)` — pick
`Actual $` or rename at the base.

```python
# 1 · detail lines — one row per statement line
det = data_page.add_table(base.to_source())
det.set_name('Statement lines')
det.set_frame(1, 14, 24, 12)
d_scn = det.get_column_by_name('<SCENARIO>')
d_sgn = det.add_column('Signed', sigma.formula.if_(
    sigma.formula.in_(det.get_column_by_name('<SECTION>'),
        sigma.formula.const_text('Cost of Goods Sold'), sigma.formula.const_text('Operating Expenses')),
    sigma.formula.neg(det.get_column_by_name('<AMOUNT>')), det.get_column_by_name('<AMOUNT>')))
d_blk = det.add_column('Block', sigma.formula.text(det.get_column_by_name('<SECTION>')))
d_lbl = det.add_column('Label', sigma.formula.text(det.get_column_by_name('<LINE ITEM>')))
dg = det.set_groupings([[d_blk, d_lbl]])[0]
dg.set_calculation('Ord', sigma.formula.min(det.get_column_by_name('<ACCOUNT CODE>')))
dg.set_calculation('Actual', sigma.formula.sum_if(d_sgn, sigma.formula.eq(d_scn, sigma.formula.const_text('Actual'))))
dg.set_calculation('Plan', sigma.formula.sum_if(d_sgn, sigma.formula.eq(d_scn, sigma.formula.const_text('Budget'))))

# 2 · one computed line per subtotal — repeat this whole block per the table
#     below, changing only the label, the ordinal, and the sections in scope,
#     each table 6 rows tall on a 7-row pitch: y = 27, 34, 41, 48, 55
gp = data_page.add_table(base.to_source())
gp.set_name('Gross profit')
gp.set_frame(1, 27, 24, 6)
g_scn = gp.get_column_by_name('<SCENARIO>')
g_sgn = gp.add_column('Signed', sigma.formula.if_(
    sigma.formula.in_(gp.get_column_by_name('<SECTION>'),
        sigma.formula.const_text('Cost of Goods Sold'), sigma.formula.const_text('Operating Expenses')),
    sigma.formula.neg(gp.get_column_by_name('<AMOUNT>')), gp.get_column_by_name('<AMOUNT>')))
g_scope = sigma.formula.in_(gp.get_column_by_name('<SECTION>'),
    sigma.formula.const_text('Revenue'), sigma.formula.const_text('Cost of Goods Sold'))
g_blk = gp.add_column('Block', sigma.formula.const_text('Subtotal'))
g_lbl = gp.add_column('Label', sigma.formula.const_text('Gross profit'))
gg = gp.set_groupings([[g_blk, g_lbl]])[0]
gg.set_calculation('Ord', sigma.formula.const_num(5350))
gg.set_calculation('Actual', sigma.formula.sum_if(g_sgn, g_scope, sigma.formula.eq(g_scn, sigma.formula.const_text('Actual'))))
gg.set_calculation('Plan', sigma.formula.sum_if(g_sgn, g_scope, sigma.formula.eq(g_scn, sigma.formula.const_text('Budget'))))

# 3 · the statement — detail source first; its names become the union's names
stmt_src = sigma.data.source.union_sources([
    sigma.data.source.SourceInput(det.to_source(), dg),
    sigma.data.source.SourceInput(gp.to_source(), gg),
])                                     # one SourceInput per computed line
st = sec.add_table(stmt_src)
st.set_frame(1, 3, 24, 21)             # statement lines + 2 — small spacing puts a line on the 24px pitch, not SKILL.md's 32; card height + 2
lbl = st.get_column_by_name('Label')
act = st.get_column_by_name('Actual')
pln = st.get_column_by_name('Plan')
blk = st.get_column_by_name('Block')
var = st.add_column('Var $', sigma.formula.subtract(act, pln))
pct = st.add_column('Var %', sigma.formula.divide(var, sigma.formula.abs(pln)))
st.set_visible_columns([lbl, act, pln, var, pct])
st.set_sort([sigma.sort.ascending(st.get_column_by_name('Ord'))])
act.set_format_pattern('(,.0f')        # accounting: negatives in parentheses
pln.set_format_pattern('(,.0f')
var.set_format_pattern('(,.0f')
pct.set_format('percent', decimals=1)
ts = st.table_style()
ts.set_preset('presentation')
ts.set_grid_lines('horizontal')
ts.set_cell_spacing('small')           # a statement is dense by convention
ts.header_style().set_color(MUTED)
for slot in [ts.header_style(), ts.cell_style()]:
    slot.set_background_color('#ffffff')
st.title_style().set_visible(False)
st.set_summary_bar(False)
st.set_background_color(None)
st.set_padding(False)

st.add_conditional_format(st.list_columns(), sigma.conditionalFormat.formula(
    sigma.formula.eq(blk, sigma.formula.const_text('Subtotal')), background=FILL, bold=True))
st.add_conditional_format([var, pct], sigma.conditionalFormat.less_than(0, text_color='#c10007', bold=True))
st.add_conditional_format([var, pct], sigma.conditionalFormat.greater_than(0, text_color='#008236'))
# a ratio line's cells reformat themselves — see Ratio lines below
st.add_conditional_format([act, pln], sigma.conditionalFormat.formula(
    sigma.formula.eq(blk, sigma.formula.const_text('Ratio')), number_format='percent', format_decimals=1))
```

The computed lines. Take the ordinals from the account ranges step 3 returned
and slot each one just past the block it closes — the numbers below suit a
4xxx revenue / 5xxx cost-of-sales / 6–7xxx operating chart of accounts:

| Label | `Ord` | Sections in `g_scope` |
|---|---|---|
| Total revenue | 4998 | Revenue |
| Total cost of sales | 5300 | Cost of Goods Sold |
| Gross profit | 5350 | Revenue · Cost of Goods Sold |
| Total operating expenses | 7350 | Operating Expenses |
| Operating income | 8001 | Revenue · Cost of Goods Sold · Operating Expenses |

## Notes

- Cost lines read **negative** on a signed statement, which is the accounting
  convention — parentheses, not a minus sign, and not red. Red is reserved for
  an unfavourable variance, which after signing is simply `Var $ < 0` on every
  line: no polarity column, no per-section rules.
- `Var %` divides by `abs(Plan)` so the percentage keeps the sign of the
  variance — over a negative cost plan, a plain divide flips it.
- `'(,.0f'` prints no currency symbol, as a statement should: name the units
  once in the card subline ("$000s", "USD"), not 90 times in the grid.
- Statement variance takes the good/bad color **as text**, not
  `blocks/table.md`'s tint backgrounds: 40 tinted cells reads as an alarm, and
  the subtotal band already carries the structure. That band deliberately
  borrows the neutral fill `FILL` — `TINT` would read
  as a callout, and the settled-period `HAIRLINE` is a step darker.
- **Ratio lines** — gross margin %, opex as a share of revenue — are ordinary
  union members whose calc is a quotient of two `sum_if`s, with
  `Block = 'Ratio'` and an ordinal just past the line they qualify (5355 after
  gross profit). The percent rendering comes from the conditional format
  above — a rule's own `number_format`, per `blocks/table.md`.
- A chart beside the statement keeps **statement order**, never value order:
  `chart.set_sort_by_calculation('dimension', sigma.formula.min(chart.get_column_by_name('Ord')), ascending=True)`.
- Blank spacer lines between sections are one more union member of constants,
  whited out on `Block = 'Spacer'` — a whole table per gap, so only when the
  subtotal bands alone do not break the page up.
- **A month-by-month statement**: reach for `blocks/pivot.md`'s rollup grid
  first — it spreads months for free. Come back here only when the grid needs
  computed lines across sections, and then twelve `sum_if` calcs replace
  `Actual`/`Plan` on **every** union member (the union keeps only columns all
  its sources have), each blending actuals for closed months with plan for open
  ones. Scope to one fiscal year first, since a month index does not know its
  year, and shade the settled months per `blocks/pivot.md`.

A balance sheet or cash-flow statement is this same skeleton with different
sections and ordinals; take their line semantics from
`sdk://skills/balance-sheet/SKILL.md`, and nothing else.
