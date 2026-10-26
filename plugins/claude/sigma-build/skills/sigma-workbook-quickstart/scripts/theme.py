#!/usr/bin/env python3
"""Resolve the twelve theme tokens and print the block every program opens with.

Run it — do not read it. One call replaces the two lookup tables in SKILL.md's
`### Theme`, and picks the hue row by hue angle in OKLCH rather than by name,
which is what the tables cannot do for a brand hex.

    python3 scripts/theme.py                       # the default, Neutral / Blue
    python3 scripts/theme.py --highlight '#2f6bdd' # what theme.highlight_color() returned
    python3 scripts/theme.py --color emerald       # a color word in the ask
    python3 scripts/theme.py --base slate          # a neutral word in the ask
    python3 scripts/theme.py --brand '#ff5733'     # a brand hex: PRIMARY is it exactly

A color word outranks a highlight read; a brand hex outranks both. Anything
unrecognised falls back to the default rather than failing, so the program can
always be written.
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

DATA = Path(__file__).with_name("design-system.json")
HEX = re.compile(r"^#?([0-9a-fA-F]{6})$")
# Below this OKLCH chroma a colour has no hue worth matching — it is a grey.
ACHROMATIC = 0.03


def load():
    return json.loads(DATA.read_text())


def parse_hex(value):
    """'#1447E6' or '1447e6' -> (20, 71, 230). None when it is not a hex color."""
    if not value:
        return None
    match = HEX.match(value.strip())
    if not match:
        return None
    digits = match.group(1)
    return tuple(int(digits[i : i + 2], 16) for i in (0, 2, 4))


def to_oklch(rgb):
    """sRGB 0-255 -> OKLCH. Plain arithmetic, so the script stays stdlib-only.

    OKLCH is the space Tailwind publishes its ramps in, which is where every
    row in design-system.json comes from.
    """

    def linear(channel):
        c = channel / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (linear(c) for c in rgb)
    long = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    medium = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    short = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = long ** (1 / 3), medium ** (1 / 3), short ** (1 / 3)
    lightness = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b_axis = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    chroma = (a * a + b_axis * b_axis) ** 0.5
    hue = math.degrees(math.atan2(b_axis, a)) % 360
    return lightness, chroma, hue


def hue_gap(first, second):
    """Shortest angular distance between two hues, in degrees."""
    gap = abs(first - second) % 360
    return min(gap, 360 - gap)


def nearest_hue(data, rgb):
    """The hue row in the same family as rgb — matched on hue angle alone.

    Lightness and chroma come from the row's own shades, so letting them into
    the distance picks the wrong family: a dull purple scores closer to vivid
    Indigo than to vivid Violet on full dE, and then the charts run ~27 degrees
    off the PRIMARY they sit beside. Hue only, and a colour with too little
    chroma to have a hue is Neutral.
    """
    _, chroma, hue = to_oklch(rgb)
    if chroma < ACHROMATIC:
        return "Neutral"
    scored = [
        (hue_gap(hue, to_oklch(parse_hex(values[0]))[2]), name)
        for name, values in data["hues"].items()
        if name != "Neutral"  # its hue angle is noise; the chroma guard reaches it
    ]
    return min(scored)[1]


def match_name(table, word):
    """Case-insensitive exact row name, else None."""
    if not word:
        return None
    for name in table:
        if name.lower() == word.strip().lower():
            return name
    return None


def resolve(data, highlight=None, color=None, base=None, brand=None):
    """Returns (base_row, hue_row, primary_override, notes)."""
    notes = []
    base_row = match_name(data["bases"], base)
    if base and not base_row:
        notes.append(f"base {base!r} is not a row; kept the default")
    if not base_row:
        base_row = data["defaults"]["base"]

    hue_row = None
    primary = None

    brand_rgb = parse_hex(brand)
    if brand and not brand_rgb:
        notes.append(f"brand {brand!r} is not a hex color; ignored")
    if brand_rgb:
        hue_row = nearest_hue(data, brand_rgb)
        primary = "#" + "".join(f"{c:02x}" for c in brand_rgb)
        notes.append(f"PRIMARY is the brand hex; the rest of the hue row is {hue_row}")

    if hue_row is None:
        named = match_name(data["hues"], color)
        if color and not named:
            notes.append(f"color word {color!r} is not a hue row; fell through")
        if named:
            hue_row = named
            notes.append(f"the ask named {named}, which outranks any highlight read")

    if hue_row is None:
        rgb = parse_hex(highlight)
        if highlight and not rgb:
            notes.append(f"highlight {highlight!r} is not a hex color; used the default")
        if rgb:
            hue_row = nearest_hue(data, rgb)
            notes.append(f"hue row nearest the workbook highlight {highlight} is {hue_row}")

    if hue_row is None:
        hue_row = data["defaults"]["hue"]
        notes.append(f"no color named and no highlight read; used {hue_row}")

    return base_row, hue_row, primary, notes


def render(data, base_row, hue_row, primary):
    values = dict(zip(data["base_tokens"], data["bases"][base_row]))
    values.update(zip(data["hue_tokens"], data["hues"][hue_row]))
    if primary:
        values["PRIMARY"] = primary

    lines = [
        "# tokens — a base row, then a hue row (### Theme); every program opens with them"
    ]
    for token in data["base_tokens"]:
        lines.append(f"{token} = '{values[token]}'")
    for token in data["hue_tokens"]:
        lines.append(f"{token} = '{values[token]}'")

    lines.append("")
    lines.append("theme = sigma.workbook.theme()")
    for call, argument in data["theme_calls"]:
        token = argument if argument in values else None
        if token:
            lines.append(f"theme.{call}({token})")
        else:
            lines.append(f"theme.{call}('{argument}')")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Print the twelve-token opening block for a quickstart program."
    )
    parser.add_argument("--highlight", help="hex returned by theme.highlight_color()")
    parser.add_argument("--color", help="a color word in the ask (emerald, blue, ...)")
    parser.add_argument("--base", help="a neutral word in the ask (slate, stone, zinc)")
    parser.add_argument("--brand", help="a brand hex; PRIMARY becomes exactly this")
    parser.add_argument(
        "--list", action="store_true", help="print the available base and hue rows"
    )
    args = parser.parse_args(argv)

    try:
        data = load()
    except (OSError, ValueError) as error:
        print(f"error: cannot read {DATA.name}: {error}", file=sys.stderr)
        print("fall back to SKILL.md's `### Theme` tables.", file=sys.stderr)
        return 1

    if args.list:
        print("bases:", ", ".join(data["bases"]))
        print("hues: ", ", ".join(data["hues"]))
        return 0

    base_row, hue_row, primary, notes = resolve(
        data, args.highlight, args.color, args.base, args.brand
    )
    print(render(data, base_row, hue_row, primary))
    print()
    print(f"# chosen: base {base_row}, hue {hue_row}")
    for note in notes:
        print(f"#   {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
