import itertools
from pathlib import Path

import pytest

from filare.flows.build_harness import build_harness_from_files


def _write_harness_with_options(
    tmp_path: Path, options_block: str
) -> tuple[Path, Path]:
    harness_path = tmp_path / "h.yml"
    metadata_path = tmp_path / "m.yml"
    harness_path.write_text(
        "connectors:\n"
        "  J1:\n"
        "    pincount: 1\n"
        "cables:\n"
        "  C1:\n"
        "    wirecount: 1\n"
        "    length: 1\n"
        "connections:\n"
        "  -\n"
        "    - J1: [1]\n"
        "notes:\n"
        "  - SplitNote\n"
        + ("" if not options_block else "\noptions:\n" + options_block)
    )
    metadata_path.write_text(
        "metadata:\n"
        "  pn: T\n"
        "  title: Split Test\n"
        "  company: ACME\n"
        "  address: 1 Road\n"
        "  sheet_total: 1\n"
        "  sheet_current: 1\n"
        "  sheet_name: h\n"
        "  output_dir: .\n"
        "  titlepage: t\n"
        "  output_names: [h]\n"
        "  files: [h.yml]\n"
        "  use_qty_multipliers: false\n"
        "  multiplier_file_name: qty.txt\n"
        "  revisions:\n"
        "    a:\n"
        "      name: tester\n"
        "      date: 2024-01-01\n"
        "      changelog: init\n"
    )
    return harness_path, metadata_path


def _build_opts(split_bom: bool, split_notes: bool, split_index: bool) -> str:
    lines = []
    if split_bom:
        lines.append("  split_bom_page: true")
    if split_notes:
        lines.append("  split_notes_page: true")
    if split_index:
        lines.append("  split_index_page: true")
    return "\n".join(lines)


def _assert_contains(path: Path, needle: str) -> None:
    assert needle in path.read_text(encoding="utf-8")


def _assert_not_contains(path: Path, needle: str) -> None:
    assert needle not in path.read_text(encoding="utf-8")


def _run_harness(tmp_path: Path, options_block: str) -> Path:
    harness_path, metadata_path = _write_harness_with_options(tmp_path, options_block)
    build_harness_from_files(
        [harness_path],
        [metadata_path],
        output_formats=("html",),
        output_dir=tmp_path,
    )
    return tmp_path / "h"


def _assert_exists(path: Path) -> bool:
    assert path.exists()
    return True


def _assert_missing(path: Path) -> None:
    assert not path.exists()


def _verify_split_files(
    base: Path, split_bom: bool, split_notes: bool, split_index: bool
):
    bom_file = base.with_suffix(".bom.html")
    notes_file = base.with_suffix(".notes.html")
    index_file = base.with_suffix(".index.html")
    html = base.with_suffix(".html").read_text(encoding="utf-8")

    if split_bom:
        _assert_exists(bom_file)
        _assert_contains(bom_file, 'id="bom"')
        _assert_not_contains(bom_file, "SplitNote")
        assert 'id="bom"' not in html
    else:
        _assert_missing(bom_file)
        assert 'id="bom"' in html

    if split_notes:
        _assert_exists(notes_file)
        _assert_contains(notes_file, 'id="notes"')
        _assert_contains(notes_file, "SplitNote")
        _assert_not_contains(notes_file, 'id="bom"')
        assert 'id="notes"' not in html
    else:
        _assert_missing(notes_file)
        assert 'id="notes"' in html

    if split_index:
        _assert_exists(index_file)
        _assert_contains(index_file, "index_table")
        _assert_not_contains(index_file, "SplitNote")
        assert "index_table" not in html
    else:
        _assert_missing(index_file)


def _should_generate(split_bom: bool, split_notes: bool, split_index: bool) -> bool:
    return any((split_bom, split_notes, split_index))


def _ensure_base_output(base: Path) -> None:
    assert base.with_suffix(".html").exists()


def _assert_no_unexpected_sections(
    base: Path, split_bom: bool, split_notes: bool, split_index: bool
) -> None:
    html = base.with_suffix(".html").read_text(encoding="utf-8")
    if not split_notes:
        assert "SplitNote" in html


def _format_params(split_bom: bool, split_notes: bool, split_index: bool) -> str:
    return f"bom={split_bom}-notes={split_notes}-index={split_index}"


def _maybe_run_split_generation(
    tmp_path: Path, split_bom: bool, split_notes: bool, split_index: bool
):
    opts = _build_opts(split_bom, split_notes, split_index)
    base = _run_harness(tmp_path, opts)
    _ensure_base_output(base)
    _assert_no_unexpected_sections(base, split_bom, split_notes, split_index)
    _verify_split_files(base, split_bom, split_notes, split_index)


def pytest_generate_tests(metafunc):
    if {"split_bom", "split_notes", "split_index"} <= set(metafunc.fixturenames):
        params = list(itertools.product([False, True], repeat=3))
        metafunc.parametrize(
            "split_bom,split_notes,split_index",
            params,
            ids=[_format_params(*p) for p in params],
        )


def test_split_sections(tmp_path, split_bom, split_notes, split_index):
    _maybe_run_split_generation(tmp_path, split_bom, split_notes, split_index)
