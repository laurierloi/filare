from wireviz.models.cable import CableModel
from wireviz.models.connector import ConnectorModel
from wireviz.models.harness import Harness
from wireviz.models.notes import Notes


def _build_harness(metadata, page_options):
    return Harness(metadata=metadata, options=page_options, notes=Notes([]))


def test_harness_accepts_connector_and_cable_models(basic_metadata, basic_page_options):
    harness = _build_harness(basic_metadata, basic_page_options)
    harness.add_connector_model(ConnectorModel(designator="J1", pinlabels=["1", "2"]))
    harness.add_cable_model(CableModel(designator="C1", wirecount=2, colors=["RD", "BK"], length="1 m"))
    assert "J1" in harness.connectors
    assert "C1" in harness.cables
    harness.populate_bom()
    assert harness.bom  # BOM entries created


def test_additional_bom_accepts_component_model(basic_metadata, basic_page_options):
    harness = _build_harness(basic_metadata, basic_page_options)
    harness.add_additional_bom_item({"type": "Sleeve", "qty": 1})
    harness.populate_bom()
    assert harness.additional_bom_items
