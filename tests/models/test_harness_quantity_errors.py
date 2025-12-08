import json

import pytest

from filare.models.harness_quantity import HarnessQuantity
from filare.errors import FilareToolsException


def test_quantity_multiplier_bad_json_includes_path(tmp_path):
    qty_file = tmp_path / "quantity_multipliers.txt"
    qty_file.write_text("not json")
    hq = HarnessQuantity([tmp_path / "H1.yml"], output_dir=tmp_path)
    with pytest.raises(FilareToolsException) as excinfo:
        hq.fetch_qty_multipliers_from_file()
    assert str(qty_file) in str(excinfo.value)
    assert "Invalid format" in str(excinfo.value)
