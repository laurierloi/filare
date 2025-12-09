from filare.flows.build_harness import build_harness_from_models
from filare.models.cable import CableModel
from filare.models.component import ComponentModel
from filare.models.connector import ConnectorModel


def test_build_harness_from_models(basic_metadata, basic_page_options):
    connectors = [ConnectorModel(designator="J1", pinlabels=["1", "2"])]
    cables = [
        CableModel(designator="C1", colors=["RD", "BK"], wirecount=2, length="1 m")
    ]
    harness = build_harness_from_models(
        connectors, cables, basic_metadata, basic_page_options
    )
    assert "J1" in harness.connectors
    assert "C1" in harness.cables
    assert harness.bom


def test_build_harness_from_models_with_additional_bom(
    basic_metadata, basic_page_options
):
    connectors = [ConnectorModel(designator="J1", pinlabels=["1"])]
    cables = [CableModel(designator="C1", colors=["RD"], wirecount=1)]
    additional = [ComponentModel(category="additional", type="Tape", qty=1)]
    harness = build_harness_from_models(
        connectors,
        cables,
        basic_metadata,
        basic_page_options,
        additional_bom=additional,
    )
    harness.populate_bom()
    assert any(entry.category for entry in harness.bom.values())
