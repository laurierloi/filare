from filare.models.component import Component, GraphicalComponent
from filare.models.numbers import NumberAndUnit
from filare.models.types import BomCategory, QtyMultiplierConnector


def test_component_additional_components_infer_category():
    sub = {"type": "Screw"}
    comp = Component(
        type="Shell", category=BomCategory.CONNECTOR, additional_components=[sub]
    )
    assert len(comp.additional_components) == 1
    assert comp.additional_components[0].category == BomCategory.ADDITIONAL


def test_component_qty_multiplier_accepts_str():
    comp = Component(
        type="Connector",
        category=BomCategory.CONNECTOR,
        qty=NumberAndUnit(1, None),
        qty_multiplier=QtyMultiplierConnector.PINCOUNT.name,
    )
    comp.compute_qty_multipliers()
    assert comp._qty_multiplier_computed == 1


def test_graphical_component_str_and_hash(connector):
    # Connector inherits GraphicalComponent; __hash__ falls back to Component hash
    assert "Connector" in str(connector)
    assert hash(connector)
