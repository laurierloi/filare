import glob
from pathlib import Path

import pytest

import pytest

from filare.wv_cli import cli


def run_filare_cli(output_dir: Path, metadata: Path, inputs, formats="h"):
    # Use CLI callback directly to avoid subprocess; default html only to avoid heavy BOM rendering
    cli.callback(  # type: ignore[attr-defined]
        files=tuple(inputs),
        formats=formats,
        components=(),
        metadata=(metadata,) if metadata else (),
        output_dir=output_dir,
        output_name=None,
        version=False,
        use_qty_multipliers=False,
        multiplier_file_name="quantity_multipliers.txt",
    )


def test_examples_generate_outputs(tmp_path):
    examples_dir = Path("examples")
    metadata_file = examples_dir / "metadata.yml"
    yaml_inputs = sorted(Path(p) for p in glob.glob(str(examples_dir / "ex*.yml")))
    assert yaml_inputs, "No example YAMLs found"
    output_dir = Path("outputs") / "examples"
    output_dir.mkdir(parents=True, exist_ok=True)

    run_filare_cli(output_dir, metadata_file, yaml_inputs, formats="h")

    for inp in yaml_inputs:
        stem = inp.stem
        for ext in (".html",):
            assert (output_dir / f"{stem}{ext}").exists()


def test_tutorial_generates_outputs(tmp_path):
    tutorial_dir = Path("tutorial")
    metadata_file = tutorial_dir / "metadata.yml"
    yaml_inputs = sorted(Path(p) for p in glob.glob(str(tutorial_dir / "tutorial*.yml")))
    assert yaml_inputs, "No tutorial YAMLs found"
    output_dir = Path("outputs") / "tutorial"
    output_dir.mkdir(parents=True, exist_ok=True)

    run_filare_cli(output_dir, metadata_file, yaml_inputs, formats="h")

    for inp in yaml_inputs:
        stem = inp.stem
        for ext in (".html",):
            assert (output_dir / f"{stem}{ext}").exists()
