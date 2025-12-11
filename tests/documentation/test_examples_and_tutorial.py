import glob
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Iterable, List, Optional

import pytest
import yaml

pytestmark = pytest.mark.skipif(
    shutil.which("dot") is None, reason="Graphviz dot executable not found"
)


def _sanitize_inputs(
    inputs: Iterable[Path],
    scratch_dir: Path,
    strip_cut_and_term: bool = False,
) -> List[Path]:
    """Optionally strip cut/termination outputs from YAMLs to speed tests."""
    sanitized: List[Path] = []
    for inp in inputs:
        if not strip_cut_and_term:
            sanitized.append(inp)
            continue
        data = yaml.safe_load(inp.read_text(encoding="utf-8")) or {}
        for key, val in list(data.items()):
            if not isinstance(val, dict):
                continue
            if key == "options" or key.endswith("_options"):
                val.pop("include_cut_diagram", None)
                val.pop("include_termination_diagram", None)
        target = scratch_dir / inp.name
        target.write_text(yaml.safe_dump(data), encoding="utf-8")
        sanitized.append(target)
    return sanitized


def run_filare_cli(
    output_dir: Path,
    metadata: Optional[Path],
    inputs,
    formats="h",
    strip_cut_and_term: bool = False,
    scratch_dir: Optional[Path] = None,
):
    # Use CLI callback directly to avoid subprocess; default html only to avoid heavy BOM rendering
    if strip_cut_and_term and scratch_dir:
        scratch_dir.mkdir(parents=True, exist_ok=True)

    files = _sanitize_inputs(
        inputs, scratch_dir or output_dir, strip_cut_and_term=strip_cut_and_term
    )
    if strip_cut_and_term and scratch_dir:
        for resources_dir in (Path("examples/resources"), Path("tutorial/resources")):
            if resources_dir.exists():
                link_target = scratch_dir / resources_dir.name
                if not link_target.exists():
                    link_target.symlink_to(resources_dir.resolve())

    for file in files:
        cmd_parts = [
            "source scripts/agent-setup.sh >/dev/null &&",
            "uv run filare run",
            shlex.quote(str(file)),
            "--formats",
            shlex.quote(formats),
            "--output-dir",
            shlex.quote(str(output_dir)),
        ]
        if metadata:
            cmd_parts.extend(["--metadata", shlex.quote(str(metadata))])
        subprocess.run(
            ["bash", "-lc", " ".join(cmd_parts)],
            check=True,
            cwd=Path.cwd(),
        )


def test_examples_generate_outputs(tmp_path):
    examples_root = Path("examples")
    groups = []

    for meta in sorted(examples_root.glob("*/metadata.yml")):
        base = meta.parent
        inputs = sorted(
            p
            for p in base.glob("*.yml")
            if p.name != "metadata.yml" and not p.name.endswith(".document.yaml")
        )
        if inputs:
            groups.append((base.name, meta, inputs))

    assert groups, "No example YAMLs found"

    base_output = Path("outputs") / "examples"
    base_output.mkdir(parents=True, exist_ok=True)

    for name, metadata_file, yaml_inputs in groups:
        output_dir = base_output / name
        output_dir.mkdir(parents=True, exist_ok=True)
        run_filare_cli(
            output_dir,
            metadata_file,
            yaml_inputs,
            formats="h",
            strip_cut_and_term=True,
            scratch_dir=tmp_path / name,
        )

        for inp in yaml_inputs:
            stem = inp.stem
            for ext in (".html",):
                assert (output_dir / f"{stem}{ext}").exists()


def test_tutorial_generates_outputs(tmp_path):
    tutorial_dir = Path("tutorial")
    metadata_file = tutorial_dir / "metadata.yml"
    yaml_inputs = sorted(
        Path(p) for p in glob.glob(str(tutorial_dir / "tutorial*.yml"))
    )
    assert yaml_inputs, "No tutorial YAMLs found"
    output_dir = Path("outputs") / "tutorial"
    output_dir.mkdir(parents=True, exist_ok=True)

    run_filare_cli(
        output_dir,
        metadata_file,
        yaml_inputs,
        formats="h",
        strip_cut_and_term=True,
        scratch_dir=tmp_path,
    )

    for inp in yaml_inputs:
        stem = inp.stem
        for ext in (".html",):
            assert (output_dir / f"{stem}{ext}").exists()
