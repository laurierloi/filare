from pathlib import Path

from filare.flows.render_outputs import render_harness_outputs
from filare.models.harness import Harness
from filare.models.metadata import Metadata, PageTemplateConfig
from filare.models.options import PageOptions
from filare.models.notes import Notes


def test_render_harness_outputs_generates_files(tmp_path):
    metadata = Metadata(
        title="t",
        pn="pn",
        company="c",
        address="a",
        output_dir=tmp_path,
        output_name="h",
        sheet_total=1,
        sheet_current=1,
        sheet_name="s",
        titlepage=tmp_path / "titlepage",
        output_names=[],
        files=[],
        use_qty_multipliers=False,
        multiplier_file_name="",
        authors={},
        revisions={"a": {"name": "r", "date": "2020-01-01", "changelog": "init"}},
        template=PageTemplateConfig(),
    )
    harness = Harness(metadata=metadata, options=PageOptions(), notes=Notes(), shared_bom={})
    # minimal connector/cable to allow output rendering
    harness.add_connector("X1", pincount=1)
    harness.add_connector("X2", pincount=1)
    harness.add_cable("C1", wirecount=1)
    harness.connect("X1", 1, "C1", 1, "X2", 1)
    harness.populate_bom()

    render_harness_outputs(harness, tmp_path, "h", ("tsv",))
    assert (tmp_path / "h.tsv").exists()
