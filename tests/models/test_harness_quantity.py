import json
import builtins

import pytest

from wireviz.models.harness_quantity import HarnessQuantity


def test_harness_quantity_reads_existing_file(tmp_path):
    qty_file = tmp_path / "quantity_multipliers.txt"
    qty_file.write_text(json.dumps({"H1": 2}))
    hq = HarnessQuantity([tmp_path / "H1.yml"], output_dir=tmp_path)
    hq.fetch_qty_multipliers_from_file()
    assert hq["H1"] == 2


def test_harness_quantity_prompts_when_missing(monkeypatch, tmp_path):
    inputs = iter(["3"])

    def fake_input(prompt):
        return next(inputs)

    monkeypatch.setattr(builtins, "input", fake_input)
    hq = HarnessQuantity([tmp_path / "H1.yml"], output_dir=tmp_path)
    hq.fetch_qty_multipliers_from_file()
    assert hq["H1"] == 3
    # file should be written
    assert json.loads((tmp_path / "quantity_multipliers.txt").read_text())["H1"] == 3


def test_harness_quantity_bad_json_raises(tmp_path):
    qty_file = tmp_path / "quantity_multipliers.txt"
    qty_file.write_text("not json")
    hq = HarnessQuantity([tmp_path / "H1.yml"], output_dir=tmp_path)
    with pytest.raises(ValueError):
        hq.fetch_qty_multipliers_from_file()


def test_harness_quantity_missing_multiplier_asserts(tmp_path):
    qty_file = tmp_path / "quantity_multipliers.txt"
    qty_file.write_text(json.dumps({"OTHER": 1}))
    hq = HarnessQuantity([tmp_path / "H1.yml"], output_dir=tmp_path)
    with pytest.raises(AssertionError):
        hq.fetch_qty_multipliers_from_file()
