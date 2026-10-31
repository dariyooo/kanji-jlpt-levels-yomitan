from kanji_jlpt_levels.build import build_kanji_meta_bank


def test_formats_level_as_n_level_display_value():
    bank = build_kanji_meta_bank({"日": {"jlpt_new": 5, "grade": 1, "freq": 1}})
    assert bank == [["日", "freq", {"value": 5, "displayValue": "N5"}]]


def test_uses_waller_level_over_jouyou_fallback():
    bank = build_kanji_meta_bank({"県": {"jlpt_new": 2, "grade": 3, "freq": 100}})
    assert bank[0][2]["value"] == 2


def test_jouyou_kanji_missing_from_waller_are_n1():
    bank = build_kanji_meta_bank({"俺": {"jlpt_new": None, "grade": 8, "freq": 1000}})
    assert bank == [["俺", "freq", {"value": 1, "displayValue": "N1"}]]


def test_adds_official_jouyou_form_of_variants():
    # kanji-data has an entry for 𠮟 but without grade
    bank = build_kanji_meta_bank(
        {
            "叱": {"jlpt_new": None, "grade": 8, "freq": 1500},
            "𠮟": {"jlpt_new": None, "grade": None, "freq": None},
        }
    )
    assert {entry[0] for entry in bank} == {"叱", "𠮟"}


def test_keeps_waller_name_kanji_and_skips_other_non_jouyou_kanji():
    bank = build_kanji_meta_bank(
        {
            "乃": {"jlpt_new": 1, "grade": 9, "freq": 1900},
            "鷲": {"jlpt_new": None, "grade": 9, "freq": 2000},
            "唖": {"jlpt_new": None, "grade": None, "freq": None},
        }
    )
    assert [entry[0] for entry in bank] == ["乃"]


def test_sorts_n5_to_n1_then_by_frequency():
    bank = build_kanji_meta_bank(
        {
            "政": {"jlpt_new": 2, "freq": 5},
            "人": {"jlpt_new": 5, "freq": 3},
            "一": {"jlpt_new": 5, "freq": 2},
            "氏": {"jlpt_new": 1, "freq": None},
        }
    )
    assert [entry[0] for entry in bank] == ["一", "人", "政", "氏"]
