from wireviz.models.connector import Connector
from wireviz.models.dataclasses import BomCategory


def test_connector_creates_pins_and_loops(connector):
    assert len(connector.pin_objects) == 3
    assert connector.loops[0].first.label == "A"
    assert connector.loops[0].second.label == "B"
    assert connector.category == BomCategory.CONNECTOR
    assert connector.has_pincolors is True


def test_connector_qty_multipliers_counts_connections(connector):
    # simulate a connection on first pin
    connector.activate_pin(1, side=None, is_connection=True)
    connector.activate_pin(2, side=None, is_connection=True)
    connector.compute_qty_multipliers()
    populated = connector.additional_components
    assert connector.pin_objects[1]._num_connections >= 1
    assert connector.pin_objects[2]._num_connections >= 1


def test_connector_str_includes_type_subtype(connector_args):
    c = Connector(**{**connector_args, "type": "D-Sub", "subtype": "male"})
    text = str(c)
    assert "D-Sub" in text and "male" in text
