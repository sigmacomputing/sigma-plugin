# Chart: sankey (flow between steps)

How a measure splits as it moves across two or three categorical steps —
channel → plan → outcome, region → product. Use it only when the path is the
question. Shares of a whole are `blocks/chart-composition.md`; a ranking is
`blocks/chart-ranked.md`.

The source is **one row per record carrying every stage column and the
measure** — no helper table.

```python
sk = sec.add_sankey_chart(src)
sk.set_frame(1, 3, 24, 12)   # H = 14; a shorter card → SKILL.md's section-card rule
sk.set_stages([sk.get_column_by_name('<STAGE 1>'), sk.get_column_by_name('<STAGE 2>')])
sk.set_value((sigma.formula.sum(sk.get_column_by_name('<AMOUNT>')), '<Measure>'))
sk.get_column_by_name('<STAGE 1>').set_filter(sigma.filter.values(['<NODE A>', '<NODE B>']))
sk.get_column_by_name('<STAGE 2>').set_filter(sigma.filter.values(['<NODE 1>', '<NODE 2>', '<NODE 3>', '<NODE 4>', '<NODE 5>']))
sk.set_palette([SERIES, SERIES_MID, EDGE])
sk.set_label_style('stage_percent')
sk.data_labels().set_visible(True)
sk.data_labels().set_precision(0)
sk.title_style().set_visible(False)
sk.set_background_color(None)
sk.set_padding(False)
```

- Stages run left to right in the order given; two or three work, each with
  about six nodes (~20 overlap labels). Name the nodes to keep with
  `sigma.filter.values` on each stage column, ranked by step 3's `query`; that
  also drops a blank-stage flow, which draws an unlabeled node.
- A skewed measure hides small nodes (a 1% stage draws invisible): size the
  flows by a measure the nodes share more evenly, such as distinct users.
  Ranking nodes by the measure can drop a whole stage — the busiest sets may
  never reach the smallest one — so query stage × node and keep nodes that
  cover every stage.
- Never cap nodes with `top_n` on the measure: it keeps the top N flows
  **per first-stage node**, so `top_n(8)` keeps 8 flows per source node, not 8
  overall — and tied flows share a rank, so a tie at the cut keeps them all.
  It does fit "the top 5 destinations per source".
- There is no legend setter — the stage labels are the legend.
