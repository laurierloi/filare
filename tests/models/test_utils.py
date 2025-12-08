import pytest
from pathlib import Path

from filare.models import utils
from filare.errors import FileResolutionError


def test_expand_ranges_and_numbers():
    assert utils.expand("1-3") == [1, 2, 3]
    assert utils.expand("3-1") == [3, 2, 1]
    assert utils.expand(["1-2", 4, "x"]) == [1, 2, 4, "x"]
    assert utils.expand("5") == [5]


def test_clean_whitespace_and_links():
    assert utils.clean_whitespace("a   b  , c") == "a b, c"
    assert utils.html_line_breaks("line1\nline2") == "line1<br />line2"
    assert utils.remove_links('<a href="x">Text</a>') == "Text"


def test_flatten2d_and_int2tuple():
    assert utils.int2tuple(1) == (1,)
    assert utils.int2tuple((1, 2)) == (1, 2)
    rows = [["a", ["b", "c"]], [1, 2]]
    assert utils.flatten2d(rows) == [["a", "b, c"], ["1", "2"]]


def test_awg_mm2_equiv_tables():
    assert utils.awg_equiv("0.34") == "22"
    assert utils.mm2_equiv("22") == "0.34"
    assert utils.awg_equiv("999") == "Unknown"


def test_smart_file_resolve(tmp_path):
    base = tmp_path / "base"
    base.mkdir()
    target = base / "file.txt"
    target.write_text("ok")
    # relative search
    resolved = utils.smart_file_resolve(Path("file.txt"), [base])
    assert resolved == target
    # absolute that exists
    assert utils.smart_file_resolve(target, [base]) == target
    # missing file raises
    with pytest.raises(FileResolutionError):
        utils.smart_file_resolve(Path("missing.txt"), [base])
