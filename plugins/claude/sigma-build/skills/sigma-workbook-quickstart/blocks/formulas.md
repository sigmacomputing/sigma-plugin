# Formulas beyond the blocks

The calculations dashboards commonly need that no other block demonstrates —
signatures as the SDK defines them. Wrap literals in formula args:
`const_num(0.5)` · `const_int(3)` · `const_text('West')` · `const_bool(True)`;
comparisons are `gt / gte / lt / lte / between / eq / neq`.

**Nesting one formula inside another needs a wrap.** `lookup` `greatest`
`least` `lag` `lead` `coalesce` `if_` `grand_total` `max` `min` all return an
untyped `Formula`, and every typed argument — `divide` `subtract` `multiply`
`abs` `cumulative_sum` `zn` `ampersand` — rejects it: `expects
NumberFormulaResolvable but got Formula` (`TextFormulaResolvable` for
`ampersand`). Put `sigma.formula.number(<inner call>)` (or `text` / `date`)
around the inner call: `zn(number(<inner call>))`. `sum` and `avg` are already
typed and need no wrap.

```python
# Averages and distincts — same shape as sum / sum_if everywhere
aov = sigma.formula.avg(base.get_column_by_name('Revenue'))
west = sigma.formula.avg_if(base.get_column_by_name('Revenue'),
    sigma.formula.eq(base.get_column_by_name('Region'), sigma.formula.const_text('West')))
mid = sigma.formula.median(base.get_column_by_name('Revenue'))
buyers = sigma.formula.count_distinct(base.get_column_by_name('<CUSTOMER>'))

# Conditional value — status labels, bucketing
health = sigma.formula.if_(
    sigma.formula.gte(base.get_column_by_name('Revenue'), base.get_column_by_name('Target')),
    sigma.formula.const_text('On track'), sigma.formula.const_text('Behind'))
# 3+ branches: switch_(value, [(match, result), ...], default_value=...)

# Share of total — a percent that sums to 100% across the rows shown
share = sigma.formula.percent_of_total(sigma.formula.sum(base.get_column_by_name('Revenue')), 'grand_total')

# Prior row / period-over-period — lag shifts the column down by offset rows
# (a plain int), so sort the element by its date grain ascending first
prior = sigma.formula.lag(sigma.formula.sum(base.get_column_by_name('Revenue')), 1)

# Running total — sort the element by its date grain ascending first
ytd = sigma.formula.cumulative_sum(sigma.formula.sum(base.get_column_by_name('Revenue')))

# Pull a value across tables by key — targets, quotas, owners
quota = sigma.formula.lookup(targets.get_column_by_name('Quota'),
    base.get_column_by_name('Region'), targets.get_column_by_name('Region'))

# Nulls: zn -> 0 on a column or a typed number formula; coalesce wraps any formula
clean = sigma.formula.zn(base.get_column_by_name('<MEASURE>'))
safe = sigma.formula.coalesce(quota, sigma.formula.const_num(0))

# Date windows — a rolling flag to filter or sum_if by
recent = sigma.formula.gte(base.get_column_by_name('<DATE COL>'),
    sigma.formula.date_add('day', sigma.formula.const_int(-90), sigma.formula.today()))
age_days = sigma.formula.date_diff('day', base.get_column_by_name('<DATE COL>'), sigma.formula.today())
```

**Pre-formatted text** — prose binds `(formula, fmt)` (`SKILL.md`); a value-list
field, or a number joined into a text column, takes no format, and `text()` on
**any** number renders full float precision, aggregate or plain column
(`287243281.43`, `85.0000000000000000000`). Round in the formula there —
`text(round(x, n))`, never `text(x)`:

```python
# money
money = sigma.formula.ampersand(sigma.formula.const_text('$'), sigma.formula.ampersand(
    sigma.formula.text(sigma.formula.round(sigma.formula.divide(total, sigma.formula.const_num(1000000)), 1)),
    sigma.formula.const_text('M')))
# a rate
pct_txt = sigma.formula.ampersand(
    sigma.formula.text(sigma.formula.round(sigma.formula.multiply(rate, sigma.formula.const_num(100)), 1)),
    sigma.formula.const_text('%'))
```

Collapsing an append-only history to **one current row per entity** — the
step before `lookup` — is a rank filtered to 1 on a grouped helper table.
Without it every aggregate sums the whole history and reads plausibly wrong:

```python
latest = data_page.add_table(base.to_source())
latest.set_name('Latest submission')
latest.set_groupings([latest.get_column_by_name('<ENTITY KEY>')])
rk = latest.add_column('Submission rank',
    sigma.formula.row_number(latest.get_column_by_name('<DATE COL>'), 'desc'))
rk.set_filter(sigma.filter.values([1]))
```

- Every result binds like any block's formula: a `(formula, '<unique name>')`
  calc, a `formulas={}` placeholder, or a condition inside `sum_if`.
- `rank(column, 'desc')` numbers rows for a table column; a top-N **chart**
  stays `sigma.filter.top_n` (`blocks/chart-ranked.md`).
- Counting rows per category in a donut or bar: `count` a column other than
  the category itself — `count(<category>)` returns 1 per category. Use the key
  or id column.
- `date_add` / `date_diff` units: `'year' 'quarter' 'month' 'week' 'day'
  'hour' 'minute' 'second'`. `lag`/`lead` offsets are plain ints;
  `date_add` amounts are formulas (`const_int`).
- A grouped table sorts on the **grouping**, not the table:
  `g = tbl.list_groupings()[0]` · `g.set_sort([...])`. `tbl.set_sort` on a
  grouped table raises "not a base-level column".
- `set_groupings` returns one level per column and a calculation goes on the
  **last** one — `[0]` is right only for a single grouping, and on two it
  silently computes against the outer level and renders zeros.
- A date grain is `date_trunc` + `set_format_pattern`, never `date_format`:
  its pattern is strftime (`'%Y-%m'`, `'%b %Y'`), and a wrong token renders
  the pattern text itself on every row, collapsing the grouping to one value
  without erroring.
- Weekdays sort alphabetically unless told otherwise — add
  `wd = el.add_column('Weekday number', sigma.formula.weekday(<DATE>))`, then
  sort by it. `set_sort_by_calculation` takes the **column** on a pivot
  (`piv.set_sort_by_calculation(piv.get_column_by_name('<WEEKDAY>'), sigma.formula.min(wd), ascending=True)`)
  and a **channel** on a chart (`chart.set_sort_by_calculation('dimension', sigma.formula.min(wd), ascending=True)`).
- `set_format('currency', ...)` renders `USD28,412`; `'currency_si'` with
  `currency='$'` gives `$28.4K`, which is what the blocks use.
