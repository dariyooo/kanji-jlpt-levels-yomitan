# kanji-jlpt-levels-yomitan

JLPT level (N5-N1) of kanji for Yomitan and DaLang.

The dictionary only contains the JLPT level and is meant to be installed alongside a kanji dictionary like KANJIDIC.
Each kanji is stored as a `kanji_meta_bank` frequency entry with a display value, e.g. `["日","freq",{"value":5,"displayValue":"N5"}]`.

## Sources

There are no official kanji lists for the JLPT since 2010, so all levels are unofficial.
All data is read from [kanji-data](https://github.com/davidluzgouveia/kanji-data), locked to a commit in `sources.lock.json`.
The *Update* workflow checks it weekly, commits newer versions and releases the dictionary if it changed.

* **N5-N1 levels**: Jonathan Waller's [JLPT resources](http://www.tanos.co.uk/jlpt/) (`jlpt_new` in kanji-data).
  These are the de facto standard and used by e.g. jisho.org, JLPT Sensei, nihongo-pro and kanjiapi.dev.
  Waller's N1 list also contains 247 jinmeiyō (name) kanji like 丑, 乃 and 伊, these are kept.
* **Kanji added to the jōyō list in 2010** (172 kanji like 俺, 丼, 嫉 and 妬): Waller's lists predate the 2010 jōyō revision and do not contain them.
  Every jōyō kanji (KANJIDIC2 grades 1-6 and 8, `grade` in kanji-data) without a level from Waller is added as **N1**.
  This follows the general consensus, e.g. JLPT Sensei lists 79 of the 86 of these kanji it covers as N1 and Kanjium most of them.
  KANJIDIC2 stores 𠮟 and 剝 under their common forms 叱 and 剥, so both forms are added.

## Installation

Make sure [uv](https://github.com/astral-sh/uv) is installed on your system and run

``` bash
uv sync
```

## Usage

``` bash
uv run build.py
```

This creates the dictionary in `out/` (`kanji-jlpt-levels-yomitan.zip`, `kanji-jlpt-levels-yomitan.index.json` and `kanji-jlpt-levels-yomitan.manifest.json`).
Downloaded sources are cached in `tmp/sources/`, the uncompressed dictionary is kept in `tmp/kanji-jlpt-levels-yomitan/` for inspection.

## Development

``` bash
uv run ruff check .          # lint
uv run ruff format .         # format
uv run pyright               # type check
uv run pytest                # tests
```

The repo follows the [DaLang dictionary repo standard](https://github.com/dariyooo/dalang-dict-utils/blob/main/docs/repo-standard.md),
update the shared setup with `uvx copier update --trust`.

## Release

Push a tag with today's date:

``` bash
git tag 2026-11-01 && git push origin 2026-11-01
```

The *Release* workflow runs the checks, builds the dictionary with the tag as revision and publishes it as the GitHub release of the tag.
Installed dictionaries pick up new releases through "Check for updates".

## License

JLPT levels by Jonathan Waller (CC BY), jōyō grades from KANJIDIC2 by the [EDRDG](https://www.edrdg.org/edrdg/licence.html) (CC BY-SA 4.0), kanji-data (MIT).
