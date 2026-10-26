# AI-written insight

Only when the user asks for an AI summary AND the warehouse exposes an AI
function (`ai_complete` or an org UDF; ask the user rather than probing
blind). The card is `blocks/insight.md`'s — only the body binding changes.
Aggregate to a small row set first — a grouped helper table on the data
page, ≤ ~50 rows, grouped as `blocks/cards.md` shows — then bind:

```python
prompt = sigma.formula.const_text('One executive sentence: revenue vs target, name the biggest driver. Data: ')
rows = sigma.formula.array_agg(sigma.formula.ampersand(
    sigma.formula.text(base.get_column_by_name('<CATEGORY>')),
    sigma.formula.ampersand(sigma.formula.const_text(': '), sigma.formula.text(base.get_column_by_name('Revenue')))))
summary = sigma.formula.call_text('ai_complete', sigma.formula.const_text('<MODEL>'),
    sigma.formula.ampersand(prompt, sigma.formula.text(rows)))
```

and use `formulas={'Summary': summary}` with body `{{Summary}}`. An
error string where the sentence should be means the function name or
model isn't available on this warehouse — fall back to the hand-written
body rather than retrying blind.

The prompt decides whether the sentence reads like the page or like a
chatbot. Order it: **length cap first** ("Return your response as 1–2
sentences."), the role, one `Ex:` sentence showing the register wanted, the
data as `#KEY: ` sections joined with `ampersand`, then an explicit "no
markdown, no asterisks". Serialize a column with
`sigma.formula.list_agg(sigma.formula.text(col), ', ')`, and strip the
reply's quote artifacts with `sigma.formula.replace(summary,
sigma.formula.const_text('"'), sigma.formula.const_text(''))`.

Frame the output as ordinary insight — the card keeps a human-authored
label ("WHAT MOVED", "RECOMMENDED OVERRIDES") with a small `PRIMARY` glyph
(`⍟`) opening it. Never label a card "AI".
