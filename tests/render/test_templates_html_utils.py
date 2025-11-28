from pathlib import Path

from filare.render.html_utils import Br, Table, Td, Tr
from filare.render.templates import get_template


def test_get_template_loads_existing_template():
    tpl = get_template("titleblock", ".html")
    assert tpl is not None


def test_html_utils_render_basic_table():
    cell = Td("cell")
    row = Tr([cell])
    table = Table([row])
    html = str(table)
    assert "<table" in html and "</table>" in html
    assert "cell" in html


def test_html_utils_singleton_tag():
    br = Br()
    assert str(br).startswith("<br")
