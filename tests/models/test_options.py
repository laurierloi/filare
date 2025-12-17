from filare.models.colors import SingleColor
from filare.models.options import PageOptions, get_page_options


def test_page_options_color_defaults_and_coercion():
    opts = PageOptions(
        bgcolor=SingleColor("RD"),
        bgcolor_node=SingleColor("RD"),
        bgcolor_connector=None,
        bgcolor_cable=None,
        bom_rows=2,
        bom_row_height=5.5,
    )
    # bgcolor_node None falls back to bgcolor
    assert opts.bgcolor_node.code_en == "RD"
    # missing colors inherit in order
    assert opts.bgcolor_connector == opts.bgcolor_node
    assert opts.bgcolor_bundle == opts.bgcolor_cable == opts.bgcolor_node
    assert opts.bom_rows == 2
    assert isinstance(opts.bom_row_height, float)


def test_get_page_options_prefers_page_specific():
    specific = {"page_options": {"bgcolor": "GN"}}
    general = {"options": {"bgcolor": "BU"}}
    opts = get_page_options(specific, "page")
    assert opts.bgcolor.code_en == "GN"
    opts2 = get_page_options(general, "page")
    assert opts2.bgcolor.code_en == "BU"
