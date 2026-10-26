# Input table

The write surface. **Empty**: rows arrive from a form or a button — an intake
log, a decision log. **Linked**: mirrors a source row-for-row and adds
editable columns beside it — a plan grid, a review queue. Both open with seed
rows so the app demonstrates itself. Order is load-bearing: table → editable
and select columns → formula columns → system columns → style → seed rows →
form. A form built before a column lacks that field; a seed row naming a
column not yet added fails.

## Empty table

```python
it = sec.add_input_table('<CONNECTION_ID>')    # the base source's connection (describe prints it)
it.set_name('Requests')
it.set_edit_mode('published-all-users')        # viewers can write once the workbook is published; the default 'draft' is workbook editors only, 'published-explore' explorers and editors
it.set_frame(1, 3, 24, 14)                     # 2 x rows + 2: a pill row is two grid rows, and so is the header
i_name = it.add_editable_column('Request', 'text')
i_amt = it.add_editable_column('Amount', 'number')
i_date = it.add_editable_column('Needed by', 'datetime')
i_status = it.add_single_select_column('Status', ['Pending', 'Approved', 'Rejected', 'Needs changes'])   # pills, coloured by option index — so only for a status vocabulary in that order; a neutral one (scenario, tier, region) is a plain text column
i_urgent = it.add_editable_column('Urgent', 'boolean')
sys = it.add_system_columns(['row_id', 'created_at', 'created_by'])
i_id = sys[0]
if not isinstance(i_id, InputTableIDColumn):   # add_system_columns returns InputTableSystemColumn; update_rows' RowSelector rejects that
    raise RuntimeError('row id')
for s in sys:
    s.set_visible(False)                       # kept for actions and the audit trail, not for reading
its = it.table_style()
its.set_preset('presentation')
its.set_grid_lines('horizontal')
its.header_style().set_color(MUTED)
for slot in [its.header_style(), its.cell_style()]:
    slot.set_background_color('#ffffff')
it.title_style().set_visible(False)
it.set_summary_bar(False)                      # the totals row under the grid
it.set_background_color(None)
it.set_padding(False)
it.set_no_data_label('NO REQUESTS YET — ADD THE FIRST ONE ON THE LEFT')
it.add_conditional_format(it.list_columns(), sigma.conditionalFormat.formula(sigma.formula.eq(i_status, sigma.formula.const_text('Rejected')), background='#ffe2e2'))
it.add_conditional_format(it.list_columns(), sigma.conditionalFormat.formula(sigma.formula.eq(i_status, sigma.formula.const_text('Approved')), background='#dcfce7'))
it.upsert_rows([                               # 6 seed rows, one call; values from step 3's query
    {i_name: '<Request 1>', i_amt: 12400, i_date: datetime(2026, 9, 12, 12), i_status: 'Pending', i_urgent: True},
    {i_name: '<Request 2>', i_amt: 48000, i_date: datetime(2026, 10, 3, 12), i_status: 'Approved', i_urgent: False},
    {i_name: '<Request 3>', i_amt: 9500, i_date: datetime(2026, 9, 30, 12), i_status: 'Needs changes', i_urgent: False},
    {i_name: '<Request 4>', i_amt: 3100, i_date: datetime(2026, 9, 20, 12), i_status: 'Rejected', i_urgent: False},
    {i_name: '<Request 5>', i_amt: 22000, i_date: datetime(2026, 11, 1, 12), i_status: 'Pending', i_urgent: True},
    {i_name: '<Request 6>', i_amt: 15800, i_date: datetime(2026, 10, 17, 12), i_status: 'Pending', i_urgent: False},
])
```

## Linked table — editable columns beside a governed source

The source must have **one row per key**: a grouped table on the data page
(below), or step 3's `query` showed `COUNT(*) = COUNT(DISTINCT key)`. Never a
coarser join. A person edits this grid, so keep it under ~2,000 rows — more
keys than that means aggregating first — and inside the table column budget
(`SKILL.md`) show the key, the editables, and the two numbers that justify an
edit. Anything else pushes the editable a reader came for off-screen.
Three calls: the opening (call 1) commits the base; this fence
is call 2 against the returned id — the grid's source chain must hold an
element from an earlier call: the base (grouped or filtered tables over it
are fine in the same call), or for a `join` the joined table itself
(`blocks/forecast.md`, call 1) — opening with the re-fetch below; the seed
`update_rows` at the end is the step 5 call, after `lt = plan_page.get_element('<LT ID>')`
narrowed with `isinstance(lt, LinkedInputTable)` and its columns narrowed as
the bullets say.

```python
# the token block from SKILL.md goes above this — every call opens with it
data_page = sigma.workbook.get_page('<DATA PAGE ID>')   # ids from call 1's state dump
plan_page = sigma.workbook.get_page('<PLAN PAGE ID>')
base = data_page.get_element('<BASE ID>')
if not (isinstance(base, LevelTable) and isinstance(plan_page, Page)):
    raise RuntimeError('re-fetch')            # get_page/get_element return base types
src = base.to_source()
plan_base = data_page.add_table(src)           # one row per Product Name
plan_base.set_name('Plan baseline')
plan_base.set_frame(1, 13, 24, 12)
g = plan_base.set_groupings([plan_base.get_column_by_name('<KEY>')])[0]
g.set_calculation('Baseline revenue', sigma.formula.sum(sigma.formula.multiply(plan_base.get_column_by_name('Price'), plan_base.get_column_by_name('Quantity'))))

lt = sec.add_linked_input_table(plan_base.to_source(), lookup_columns={'<KEY>': 'Product'}, source_columns={'Baseline revenue': 'Baseline'})
lt.set_name('Plan grid')
lt.set_edit_mode('published-all-users')
lt.set_frame(1, 3, 24, 16)
l_adj = lt.add_editable_column('Adjustment %', 'number')
l_ovr = lt.add_editable_column('Override', 'number')
l_why = lt.add_editable_column('Rationale', 'text')
l_base = lt.get_column_by_name('Baseline')
l_plan = lt.add_formula_column('Plan', sigma.formula.coalesce(l_ovr, sigma.formula.multiply(l_base,
    sigma.formula.add(sigma.formula.const_num(1), sigma.formula.divide(sigma.formula.number(sigma.formula.coalesce(l_adj, sigma.formula.const_num(0))), sigma.formula.const_num(100))))))
l_delta = lt.add_formula_column('Delta', sigma.formula.subtract(l_plan, l_base))
pk = lt.list_primary_key_columns()[0]          # the key every action targets — a linked table is keyed on it, so it needs no row_id
lt.set_frozen_column(lt.get_column_by_name('Product'))
lt.set_summary_bar(False)
lts = lt.table_style()                         # then the style calls of the empty table
l_base.set_format('currency_si', decimals=1, currency='$')   # and Plan, Delta the same
lt.add_conditional_format(l_delta, sigma.conditionalFormat.greater_than(0, background='#dcfce7', text_color='#008236', bold=True))
lt.add_conditional_format(l_delta, sigma.conditionalFormat.less_than(0, background='#ffe2e2', text_color='#c10007', bold=True))
# step 5 is its own call
lt.update_rows([                               # step 5 call: seed 3 keys so Plan and Delta read
    ({lt.get_column_by_name('Product'): '<KEY VALUE 1>'}, {l_adj: 5, l_why: 'Demand up in Q3'}),
    ({lt.get_column_by_name('Product'): '<KEY VALUE 2>'}, {l_adj: -3, l_why: 'Supplier constraint'}),
    ({lt.get_column_by_name('Product'): '<KEY VALUE 3>'}, {l_ovr: 60000, l_why: 'New channel'}),
])
```

- If either `add_input_table` or `add_linked_input_table` names several
  writeback schemas, both take `writeback_schema_id='<ID>'`: ask the user which
  and resubmit. If it raises `no writeback connection`, a schema cannot fix it —
  ask which connection to use and resubmit with that id (a linked table writes
  through its source's connection); when none can write, say the app has no
  write surface here — never build around it. A **linked** table cannot be
  built on a `sigma.data.source.join` directly: add the join as a table first
  (`blocks/forecast.md`), then link that table.
- Format a date column as in `blocks/table.md`.
- Handles from `add_*_column` are what seed dicts and action effects take. A
  column fetched later with `get_column_by_name` is a plain `Column` — narrow
  it first: `if isinstance(c, LiteralEditableColumn)` / `SingleSelectEditableColumn`.
- One `upsert_rows` / `update_rows` per table, every seed row in it (≤ 2,000).
  Seed dates at noon — `datetime(2026, 9, 12, 12)` — or they render a day
  early. `to_source()` feeds KPIs, strips, charts, and the chat, without
  hidden or system columns. A control on base columns does not reach an input
  table: to filter one, target its own columns (`blocks/queue.md`'s toolbar)
  or build a second table off `it.to_source()` on the data page.
- A form takes an empty table only (`blocks/intake.md`); actions write to
  both kinds (`blocks/queue.md`).
