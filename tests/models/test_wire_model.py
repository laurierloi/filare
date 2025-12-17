from filare.models.colors import MultiColor
from filare.models.dataclasses import ShieldClass, WireClass
from filare.models.numbers import NumberAndUnit
from filare.models.wire import ShieldModel, WireModel


def test_wire_model_roundtrip():
    wire = WireClass(
        parent="W1",
        index=2,
        id="w2",
        label="SIG",
        color=MultiColor(["RD"]),
        gauge=NumberAndUnit.to_number_and_unit("20 AWG"),
        length=NumberAndUnit.to_number_and_unit("2 m"),
        ignore_in_bom=True,
        show_equiv=True,
    )
    model = WireModel.from_wireclass(wire)
    assert model.parent == "W1"
    assert model.gauge is not None
    assert model.gauge.unit is not None
    assert model.gauge.unit.lower() == "awg" or model.gauge.unit == "AWG"
    clone = model.to_wireclass()
    assert clone.label == "SIG"
    assert clone.ignore_in_bom is True
    assert clone.color is not None
    assert clone.color[0].code_en == "RD"


def test_shield_model_roundtrip_defaults():
    shield = ShieldClass(parent="C1", index=0, color=MultiColor(["BK"]))
    model = ShieldModel.from_wireclass(shield)
    assert model.label.lower() == "shield" or model.label == ""
    restored = model.to_wireclass()
    assert restored.label.lower() == "shield"
    assert restored.parent == "C1"
