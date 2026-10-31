import json
import sys

from dalang_dict import build_index, fetch, github_source, package_dictionary

GITHUB_REPO = "dariyooo/kanji-jlpt-levels-yomitan"
ASSET = "kanji-jlpt-levels-yomitan"
TITLE = "JLPT Kanji"

# Pinned for reproducible builds; bump the commit to pick up upstream fixes.
KANJI_DATA = github_source(
    "kanji-data.json", "davidluzgouveia/kanji-data", "00fd7079c3890f430759536f91aa5e854ec0ca4f", "kanji.json"
)

# KANJIDIC2 grades of the jōyō kanji: 1-6 kyōiku kanji, 8 remaining jōyō kanji
JOUYOU_GRADES = (1, 2, 3, 4, 5, 6, 8)
# Jōyō kanji not covered by Waller's lists (added to the jōyō list in 2010) get this level
UNLISTED_JOUYOU_LEVEL = 1
# KANJIDIC2 lists these 2010 jōyō kanji under their common form, the official jōyō form is added as well
JOUYOU_VARIANTS = {"叱": "𠮟", "剥": "剝"}

INDEX_FIELDS = {
    "sourceLanguage": "ja",
    "author": "Jonathan Waller (JLPT lists), David Gouveia (kanji-data)",
    "url": f"https://github.com/{GITHUB_REPO}",
    "description": "JLPT level (N5-N1) of kanji. Unofficial: the Japan Foundation does not publish kanji lists "
    "since 2010. Levels follow Jonathan Waller's JLPT resources, jōyō kanji added in 2010 are N1.",
    "attribution": "JLPT levels: Jonathan Waller, tanos.co.uk (CC BY). "
    "Jōyō grades: KANJIDIC2 by the EDRDG (CC BY-SA 4.0). Data: davidluzgouveia/kanji-data (MIT).",
}


def get_jlpt_level(info: dict) -> int | None:
    """Returns Waller's JLPT level, N1 for jōyō kanji missing from his lists, None if not in the JLPT."""
    if info.get("jlpt_new") in (1, 2, 3, 4, 5):
        return info["jlpt_new"]
    if info.get("grade") in JOUYOU_GRADES:
        return UNLISTED_JOUYOU_LEVEL
    return None


def build_kanji_meta_bank(kanji_data: dict) -> list:
    """Creates one `freq` entry per kanji with a JLPT level, e.g. ["日","freq",{"value":5,"displayValue":"N5"}].

    Sorted from N5 to N1 and by frequency within a level.
    """
    entries = []
    for kanji, info in kanji_data.items():
        level = get_jlpt_level(info)
        if level is None:
            continue
        freq = info.get("freq") or sys.maxsize
        entries.append((kanji, level, freq))
        variant = JOUYOU_VARIANTS.get(kanji)
        if variant and get_jlpt_level(kanji_data.get(variant, {})) is None:
            entries.append((variant, level, freq))
    entries.sort(key=lambda e: (-e[1], e[2]))

    return [[kanji, "freq", {"value": level, "displayValue": f"N{level}"}] for kanji, level, _ in entries]


def verify_kanji_meta_bank(kanji_meta_bank: list) -> None:
    """Fails on duplicate kanji and prints the per-level counts."""
    seen = set()
    counts = {f"N{level}": 0 for level in range(5, 0, -1)}

    for kanji, _, data in kanji_meta_bank:
        if kanji in seen:
            sys.exit(f"Duplicate kanji: {kanji}")
        seen.add(kanji)
        counts[data["displayValue"]] += 1

    print(f"Kanji meta bank verified: {len(seen)} kanji {counts}")


def main() -> None:
    kanji_data = json.loads(fetch(KANJI_DATA).read_text(encoding="utf-8"))

    kanji_meta_bank = build_kanji_meta_bank(kanji_data)
    verify_kanji_meta_bank(kanji_meta_bank)
    index = build_index(TITLE, GITHUB_REPO, ASSET, **INDEX_FIELDS)
    package_dictionary(ASSET, index, {"kanji_meta_bank": kanji_meta_bank})
