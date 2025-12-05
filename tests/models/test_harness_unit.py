from filare.models.harness import Harness
from filare.models.connector import ConnectorModel
from filare.models.cable import CableModel
from filare.models.component import ComponentModel
from filare.models.notes import Notes
from filare.models.options import PageOptions


def test_harness_add_models_and_name(basic_metadata):
    harness = Harness(metadata=basic_metadata, options=PageOptions(), notes=Notes())

    harness.add_connector_model(ConnectorModel(designator="J1", pincount=1))
    harness.add_cable_model(CableModel(designator="C1", wirecount=1, colors=["RD"]))
    harness.add_additional_bom_item(ComponentModel(category="additional", type="Label"))

    assert harness.name == basic_metadata.name
    assert "J1" in harness.connectors
    assert "C1" in harness.cables
    assert harness.additional_bom_items and harness.additional_bom_items[0].category
