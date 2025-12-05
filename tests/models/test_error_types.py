from pathlib import Path

import pytest

from filare.errors import (
    ColorPaddingUnsupported,
    FileResolutionError,
    InvalidNumberFormat,
    UnsupportedLoopSide,
)
from filare.models.colors import MultiColor
from filare.models.numbers import NumberAndUnit
from filare.models.utils import smart_file_resolve
from filare.render.graphviz import gv_connector_loops


def test_invalid_number_format_raises_custom_error():
    with pytest.raises(InvalidNumberFormat):
        NumberAndUnit.to_number_and_unit("abc mm")


def test_file_resolution_error(tmp_path):
    with pytest.raises(FileResolutionError):
        smart_file_resolve(Path("missing.txt"), [tmp_path])


def test_color_padding_unsupported(monkeypatch):
    colors = MultiColor(["#111", "#222", "#333", "#444"])
    monkeypatch.setattr("filare.models.colors.padding_amount", 2)
    with pytest.raises(ColorPaddingUnsupported):
        _ = colors.html_padded_list


def test_unsupported_loop_side():
    dummy = type(
        "DummyConnector",
        (),
        {"ports_left": False, "ports_right": False, "loops": [], "designator": "X"},
    )()
    with pytest.raises(UnsupportedLoopSide):
        gv_connector_loops(dummy)
