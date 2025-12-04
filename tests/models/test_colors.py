import pytest

from filare.models.colors import (
    COLOR_CODES,
    ColorOutputMode,
    MultiColor,
    SingleColor,
    get_color_by_colorcode_index,
)


def test_single_color_known_and_html():
    c = SingleColor(inp="RD")
    assert c.code_en == "RD"
    assert c.html.startswith("#")
    assert str(c) == "RD"


def test_single_color_unknown_defaults_html():
    c = SingleColor(inp="magenta")
    assert c.code_en.lower() == "magenta"
    assert c.html.lower() == "magenta"

def test_single_color_direct_values_and_copy(monkeypatch):
    # direct values triggers early init branch
    c = SingleColor(code_en="RD", html="#ff0000")
    assert str(c) == "RD"
    copy = SingleColor(c)
    assert copy.code_en == "RD"
    # reset mode to something non-standard to hit default convert_case branch
    monkeypatch.setattr("filare.models.colors.color_output_mode", type("X", (), {"name": "MISC"})())
    assert str(SingleColor(html=None)) == ""
    assert str(c) == "#ff0000"

def test_single_color_numeric_and_falsey():
    c = SingleColor(inp=0x123456)
    assert c.html == "#123456"
    assert bool(SingleColor(None)) is False

def test_single_color_german_mode(monkeypatch):
    monkeypatch.setattr("filare.models.colors.color_output_mode", ColorOutputMode.DE_LOWER)
    c = SingleColor(inp="GN")
    assert str(c) == "gn"
    assert c.code_de == "gn"


def test_multi_color_parses_colon_and_padding(monkeypatch):
    monkeypatch.setattr("filare.models.colors.padding_amount", 3)
    colors = MultiColor("RD:GN")
    assert len(colors) == 2
    padded = colors.html_padded_list
    assert len(padded) == 3
    assert all(p.startswith("#") or p for p in padded)
    # indexing wraps
    assert colors[3].code_en == colors[1].code_en
    assert colors.all_known


def test_get_color_by_colorcode_index_wraps():
    assert (
        get_color_by_colorcode_index("TEL", 60)
        == COLOR_CODES["TEL"][60 % len(COLOR_CODES["TEL"])]
    )

def test_multi_color_with_none_and_singlecolor():
    empty = MultiColor(None)
    assert len(empty) == 0
    assert bool(empty) is False
    assert not bool(empty[0])

    sc = SingleColor("RD")
    multi = MultiColor(sc)
    assert len(multi) == 1
    assert multi[0].code_en == "RD"

def test_multi_color_html_and_padding_defaults():
    multi = MultiColor(["RD", None, "BU"])
    # None entries are skipped
    assert [c.code_en for c in multi.colors] == ["RD", "BU"]
    assert multi.html.startswith("#")
    assert multi.html_padded.endswith("#0066ff") or ":" in multi.html_padded

def test_multi_color_unusual_cases(monkeypatch):
    # odd-length string falls back to treating as html color
    mc = MultiColor("ABC")
    assert mc[0].code_en == "ABC"
    # non-standard output mode hits fallback joiner
    monkeypatch.setattr("filare.models.colors.color_output_mode", type("X", (), {"name": "OTHER"})())
    assert str(mc) == "ABC"
    # length >3 raises padding exception
    with pytest.raises(Exception):
        _ = MultiColor(["RD", "BK", "GN", "YE"]).html_padded_list


@pytest.mark.parametrize(
    "mode",
    [ColorOutputMode.EN_UPPER, ColorOutputMode.EN_LOWER, ColorOutputMode.HTML_UPPER],
)
def test_color_output_mode_changes(monkeypatch, mode):
    monkeypatch.setattr("filare.models.colors.color_output_mode", mode)
    c = SingleColor(inp="RD")
    s = str(c)
    if "EN_" in mode.name:
        assert s.lower() == c.code_en.lower()
    elif "HTML_" in mode.name:
        assert s.lower().startswith("#") or s == c.html
