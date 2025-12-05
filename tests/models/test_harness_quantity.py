import builtins
import json
import logging

import pytest

from filare.models.harness_quantity import HarnessQuantity


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


def test_harness_quantity_handles_missing_file_gracefully(tmp_path):
    hq = HarnessQuantity([tmp_path / "H1.yml"], output_dir=tmp_path)
    # No file present; set multipliers and save
    hq.multipliers = {"H1": 0}
    hq.save_qty_multipliers_to_file()
    data = json.loads((tmp_path / "quantity_multipliers.txt").read_text())
    assert data["H1"] == 0


def test_harness_quantity_derives_paths(tmp_path):
    h1 = tmp_path / "H1.yml"
    h1.write_text("connectors: {}")
    hq = HarnessQuantity([h1], output_dir=tmp_path)
    assert hq.folder == tmp_path
    assert hq.qty_multipliers == tmp_path / "quantity_multipliers.txt"
    assert hq.harness_names == ["H1"]


def test_harness_quantity_retrieve_multiplier(tmp_path):
    h1 = tmp_path / "H1.yml"
    h1.write_text("connectors: {}")
    hq = HarnessQuantity([h1], output_dir=tmp_path, multipliers={"H1": 4})
    bom_path = tmp_path / "H1.bom.tsv"
    bom_path.write_text("")  # only stem used
    assert hq.retrieve_harness_qty_multiplier(bom_path) == 4


def test_harness_quantity_input_warning(monkeypatch, caplog, tmp_path):
    caplog.set_level(logging.WARNING)
    inputs = iter(["not-a-number"])

    def fake_input(prompt):
        return next(inputs)

    monkeypatch.setattr(builtins, "input", fake_input)
    h1 = tmp_path / "H1.yml"
    h1.write_text("connectors: {}")
    hq = HarnessQuantity([h1], output_dir=tmp_path)
    hq.get_qty_multipliers_from_user()
    assert any(
        "Quantity multiplier must be an integer" in rec.message
        for rec in caplog.records
    )


def test_harness_quantity_allows_empty_when_paths_provided(tmp_path):
    folder = tmp_path / "out"
    folder.mkdir()
    qty_path = folder / "quantity_multipliers.txt"
    hq = HarnessQuantity(
        harnesses=[],
        folder=folder,
        qty_multipliers=qty_path,
        multiplier_file_name="quantity_multipliers.txt",
    )
    assert hq.folder == folder
    assert hq.qty_multipliers == qty_path
