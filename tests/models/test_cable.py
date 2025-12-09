from filare.models.cable import Cable
from filare.models.colors import MultiColor
from filare.models.dataclasses import Connection, PinClass


def test_cable_creates_wire_objects(cable):
    assert len(cable.wire_objects) == 2
    assert list(cable.wire_objects.keys()) == [1, 2]
    assert str(cable.wire_objects[1].color).upper().startswith("RD")


def test_cable_connect_records_connections(cable, pin_pair):
    left_pin, right_pin = pin_pair
    cable._connect(left_pin, 1, right_pin)
    assert cable.wire_ins("1") == [str(left_pin)]
    assert cable.wire_outs("1") == [str(right_pin)]
    assert isinstance(cable._connections[0], Connection)


def test_cable_qty_multiplier_applies_length(cable):
    cable.compute_qty_multipliers()
    sleeve = cable.additional_components[0]
    assert sleeve._qty_multiplier_computed == cable.length.number
