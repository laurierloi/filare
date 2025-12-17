from pathlib import Path
from typing import Any, cast

import filare.models.harness as harness_module
from filare.models.cable import CableModel
from filare.models.component import ComponentModel
from filare.models.connector import ConnectorModel
from filare.models.harness import Harness
from filare.models.hypertext import MultilineHypertext
from filare.models.notes import Notes
from filare.models.options import PageOptions
from filare.settings import settings


def test_harness_add_models_and_name(basic_metadata):
    harness = Harness(metadata=basic_metadata, options=PageOptions(), notes=Notes())

    harness.add_connector_model(ConnectorModel(designator="J1", pincount=1))
    harness.add_cable_model(CableModel(designator="C1", wirecount=1, colors=["RD"]))
    harness.add_additional_bom_item(
        ComponentModel(category="additional", type=MultilineHypertext.to("Label"))
    )

    assert harness.name == basic_metadata.name
    assert "J1" in harness.connectors
    assert "C1" in harness.cables
    assert harness.additional_bom_items and harness.additional_bom_items[0].category


def test_harness_output_and_tables(tmp_path, basic_metadata, monkeypatch):
    options = PageOptions(include_cut_diagram=True, include_termination_diagram=True)
    harness = Harness(metadata=basic_metadata, options=options, notes=Notes())

    harness.add_connector_model(
        {"designator": "J1", "pincount": 1, "pins": [1], "pinlabels": ["A"]}
    )
    harness.add_connector_model(
        ConnectorModel(designator="J2", pinlabels=["B"], pincount=1)
    )
    harness.add_cable_model({"designator": "C1", "wirecount": 1, "colors": ["RD"]})
    harness.add_additional_bom_item({"type": "Tag"})

    harness.connect("J1", "A", "C1", 1, "J2", "B")
    harness.orient_connectors_overview()
    assert harness.connectors["J1"].ports_right is True
    assert harness.connectors["J2"].ports_left is True

    harness.populate_bom()

    class FakeGraph:
        def __init__(self):
            self.format = None
            self.render_calls = []
            self.body = []

        def render(self, filename, view=False, cleanup=True):
            path = Path(filename)
            suffix = f".{self.format}" if self.format else ""
            target = path.with_suffix(suffix)
            target.write_text("x")
            self.render_calls.append((self.format, target))

        def save(self, filename):
            Path(filename).write_text("gv")

        def pipe(self, format="svg"):
            return b"<svg/>"

        def attr(self, *args, **kwargs):
            return None

    harness._graph = cast(Any, FakeGraph())

    monkeypatch.setattr(harness_module, "embed_svg_images_file", lambda path: None)
    template_calls = []

    class FakeTemplate:
        def render(self, ctx):
            template_calls.append(ctx)
            return "<table></table>"

    monkeypatch.setattr(
        harness_module, "get_template", lambda *args, **kwargs: FakeTemplate()
    )
    html_calls = []
    monkeypatch.setattr(
        harness_module,
        "generate_html_output",
        lambda *args, **kwargs: html_calls.append(args),
    )
    monkeypatch.setattr(
        harness_module, "generate_pdf_output", lambda *args, **kwargs: None
    )

    out = tmp_path / "out"
    harness.output(out, fmt=("html", "svg", "gv", "tsv", "csv"))

    assert (out.with_suffix(".svg")).exists()
    assert (out.with_suffix(".gv")).exists()
    assert (out.with_suffix(".tsv")).exists()
    assert template_calls  # cut/termination tables rendered
    assert html_calls  # html output invoked


def test_build_cut_table_handles_shield_id(basic_metadata, monkeypatch):
    options = PageOptions(include_cut_diagram=True)
    harness = Harness(metadata=basic_metadata, options=options, notes=Notes())
    harness.add_cable_model(
        {"designator": "C1", "wirecount": 1, "colors": ["RD"], "shield": True}
    )

    template_calls = []

    class FakeTemplate:
        def render(self, ctx):
            template_calls.append(ctx)
            return "<table></table>"

    monkeypatch.setattr(
        harness_module, "get_template", lambda *args, **kwargs: FakeTemplate()
    )

    rows, rendered = harness_module._build_cut_table(harness)

    assert rendered == "<table></table>"
    assert any(row["wire"].endswith("-s") for row in rows)
    assert template_calls  # template was rendered
