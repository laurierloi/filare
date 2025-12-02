import textwrap

import pytest

from filare.fil_cli import cli


@pytest.mark.parametrize("formats", ["tb"])
def test_shared_bom_contains_both_harnesses(tmp_path, formats):
    pn = "TEST-DOC"

    metadata_path = tmp_path / "metadata.yml"
    metadata_path.write_text(
        textwrap.dedent(
            f"""\
            metadata:
              pn: {pn}
              company: Test Company
              address: 123 Test Street
              authors: {{}}
              revisions: {{}}
              template:
                name: din-6771
                sheetsize: A4
            """
        )
    )

    harness_a = tmp_path / "harness_a.yml"
    harness_a.write_text(
        textwrap.dedent(
            """\
            connectors:
              J1:
                pincount: 2
              J2:
                pincount: 2

            cables:
              W1:
                wirecount: 2

            connections:
              -
                - J1: [1, 2]
                - W1: [1, 2]
                - J2: [1, 2]
            """
        )
    )

    harness_b = tmp_path / "harness_b.yml"
    harness_b.write_text(
        textwrap.dedent(
            """\
            connectors:
              P1:
                pincount: 3
              P2:
                pincount: 3

            cables:
              W2:
                wirecount: 3

            connections:
              -
                - P1: [1-3]
                - W2: [1-3]
                - P2: [1-3]
            """
        )
    )

    cli.callback(  # type: ignore[attr-defined]
        files=(harness_a, harness_b),
        formats=formats,
        components=(),
        metadata=(metadata_path,),
        output_dir=tmp_path,
        output_name=None,
        version=False,
        use_qty_multipliers=False,
        multiplier_file_name="quantity_multipliers.txt",
    )

    harness_a_bom = tmp_path / f"{harness_a.stem}.tsv"
    harness_b_bom = tmp_path / f"{harness_b.stem}.tsv"
    shared_bom = tmp_path / "shared_bom.tsv"

    for output_file in (harness_a_bom, harness_b_bom, shared_bom):
        assert output_file.exists(), f"Missing {output_file}"

    shared_bom_text = shared_bom.read_text()
    expected_harness_names = [
        f"{pn}-{harness_a.stem}",
        f"{pn}-{harness_b.stem}",
    ]
    for harness_name in expected_harness_names:
        assert harness_name in shared_bom_text
