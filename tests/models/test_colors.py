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
