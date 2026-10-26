# Chart: map (points · regions)

Where the measure sits geographically — the answer to "which stores", "which
metros", "is it one site or the whole area" that a ranked bar cannot give.
Two elements, chosen by how the data locates a mark:

- `describe` shows a latitude **and** longitude pair → `add_point_map`
- it shows a named area (country, state, county, ZIP, province) → `add_region_map`
- it shows geometry (shapes, not points or names) → `add_geography_map(src)`; the setters are in the module docs (`## SDK docs`)

```python
mp = sec.add_point_map(src)
mp.set_frame(1, 3, 24, 14)   # H = 16; a shorter card → SKILL.md's section-card rule, 12 rows the floor — a cramped map blurs
mp.set_latitude(mp.get_column_by_name('<LATITUDE>'))
mp.set_longitude(mp.get_column_by_name('<LONGITUDE>'))
mp.set_point_size((sigma.formula.sum(mp.get_column_by_name('Revenue')), 'Total revenue'))
mp.set_color_scale((sigma.formula.sum(mp.get_column_by_name('Revenue')), 'Shaded revenue'))
mp.set_label([mp.get_column_by_name('<SITE NAME>')])
mp.get_column_by_name('Total revenue').set_format('currency_si', decimals=1, currency='$')
mp.set_padding(False)
```

A region map is the same shape with one different binding — the region column
and its type, which is required alongside it:

```python
rm = sec.add_region_map(src)
rm.set_region(rm.get_column_by_name('<STATE>'), 'us-state')
rm.set_color_scale((sigma.formula.sum(rm.get_column_by_name('Revenue')), 'Total revenue'))
```

- `region_type` is one of `'country'` `'us-state'` `'us-county'`
  `'us-zipcode'` `'us-cbsa'` `'us-postal-place'` `'ca-province'`. It must
  match what the column actually holds — `query` the distinct values first;
  two-letter codes and full names are both accepted, mixed ones are not.
- Never `set_background_color(None)` on a map: a transparent map renders its legend as a dark panel of dim, illegible text.
- `set_color_scale` binds the measure; the gradient takes the workbook palette. To pin it, `mp.color_scale_scheme().set_palette([TINT, SERIES])` after binding.
- Lat/long are **grouping keys**, so rows sharing a coordinate collapse into
  one mark and the measure aggregates across them — which is what you want
  per site, and wrong per transaction. If each row must be its own mark, the
  source needs a key that makes it unique.
- Size and color can carry the same measure — size for magnitude, shade for
  the same thing read at a glance. Two *different* measures on one map is one
  too many things to decode; put the second in the band beside it.
- A map answers "where", never "how much" — pair it with a ranking or a
  table in the same band, or the reader can see the shape and not the number.
- Only `set_label` renders text on the marks; a point map has no title on
  screen, so the card label does that job as usual.
