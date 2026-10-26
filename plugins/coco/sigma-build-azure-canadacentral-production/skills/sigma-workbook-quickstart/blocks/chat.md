# Assistant chat

An agent the reader types questions at, answering from the elements you
attach — it answers what no chart was built for. The shell table names the
placement, and it is a **popover** behind the shell's top-right `Assistant`
trigger in every one — the panel it opens under is where the reader's eye
already is. The chat itself:

```python
chat = host.add_chat('Answer questions about <SUBJECT> for <WHO IS ASKING>.')   # host: ai, the popover
chat.set_frame(1, 1, 12, 14)               # the popover body is 12 columns
chat.set_agent_name('<Revenue analyst>')
chat.set_agent_description('<Answers revenue questions from the orders table.>')
chat.set_instructions(
    'You answer questions about <SUBJECT> for <WHO>, from the attached data only. '
    + 'Answer in 2-3 sentences, naming the number that decides it. '
    + 'Say plainly when the data does not answer — never estimate. '
    + 'No tables, no bullet lists, no markdown. '
    + 'You can read and explain; you cannot change the workbook or the data, so never offer to.')
chat.add_source(base)
chat.set_background_color(None)
chat.set_padding(False)                    # flush — the popover's own padding insets it
```

- `ai = sigma.workbook.add_popover(host, 'Assistant')` — the host is the
  header band, the header panel's `hc`, or the sidebar strip's `hc` — then
  `ai.set_width('x_large')` · the chat above. `blocks/header.md` and
  `blocks/sidebar.md` style the trigger. It is the one tall popover.
- The popover **keeps its padding** — never `set_padding(False)` on it. It
  is the frame around the agent, not a structural container, and without
  the inset the messages and the input box run into its edge.
- A popover has no header and **cannot be opened by an action** —
  `open_overlay` on one raises. Its `trigger()` is the only way in, so it
  never takes a button beside it; style that trigger instead of adding one.
  A drawer is what an *action* opens (`blocks/queue.md`, `blocks/detail.md`).
- **Apps** attach the write table as well (`chat.add_source(it)` — `lt` for
  a grid or queue) so the agent reads the log or queue, and add to the
  instructions: 'You can read the plan, queue, or log; you cannot change
  it — say so if asked.'
- Sources are **column-bearing elements only** — the base table, an input
  table, a chart, a KPI, a pivot. A text element, container, or control
  fails at typecheck. `add_source` adds one, `set_sources([...])` replaces
  the set. Attach `base` for the whole grain and the page's main surface;
  never more than 3 sources.
- Instructions are **static text**: `{{...}}` stays literal, so scope the
  agent in words. There is no greeting or starter-question setting, and
  this block adds no agent actions (`chat.add_agent_action` can add them), so
  the agent has no tools — a brief that promises to file or update anything
  yields an agent that apologizes; state the limit instead.
- Always set both names — the default is a bare `Agent`, `Agent 2`, the way
  a page defaults to "Page 1".
