from pathlib import Path

from wireviz.models.metadata import Metadata, PageTemplateConfig
from wireviz.models.options import PageOptions
from wireviz.models.notes import Notes
from wireviz.render.output import generate_html_output
from wireviz.models.bom import BomRenderOptions, BomEntry, BomContent
from wireviz.models.numbers import NumberAndUnit
from wireviz.models.partnumber import PartNumberInfo
from wireviz.models.dataclasses import BomCategory


def test_generate_html_output_creates_file(tmp_path):
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
    options = PageOptions()
    notes = Notes()
    entry = BomEntry(
        qty=NumberAndUnit(1, None),
        partnumbers=PartNumberInfo(pn="PN"),
        id="1",
        description="Test",
        category=BomCategory.ADDITIONAL,
        designators=[],
    )
    bom_render = BomContent({hash(entry): entry}).get_bom_render(
        options=BomRenderOptions(no_per_harness=True)
    )
    options.bom_rows = bom_render.rows
    # precreate a placeholder svg expected by generate_html_output
    (tmp_path / "h.svg").write_text("<svg></svg>")
    generate_html_output(
        filename=tmp_path / "h",
        bom={hash(entry): entry},
        metadata=metadata,
        options=options,
        notes=notes,
        rendered={"bom": bom_render.render(options)},
        bom_render_options=BomRenderOptions(no_per_harness=True),
    )
    assert (tmp_path / "h.html").exists()
