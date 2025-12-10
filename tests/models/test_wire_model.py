from filare.models.dataclasses import ShieldClass, WireClass
from filare.models.wire import ShieldModel, WireModel


def test_wire_model_roundtrip():
    wire = WireClass(
        parent="W1",
        index=2,
        id="w2",
        label="SIG",
        color="RD",
        gauge="20 AWG",
        length="2 m",
        ignore_in_bom=True,
        show_equiv=True,
    )
    model = WireModel.from_wireclass(wire)
    assert model.parent == "W1"
    assert model.gauge.unit.lower() == "awg" or model.gauge.unit == "AWG"
    clone = model.to_wireclass()
    assert clone.label == "SIG"
    assert clone.ignore_in_bom is True
    assert clone.color[0].code_en == "RD"


def test_shield_model_roundtrip_defaults():
    shield = ShieldClass(parent="C1", index=0, color="BK")
    model = ShieldModel.from_wireclass(shield)
    assert model.label.lower() == "shield" or model.label == ""
    restored = model.to_wireclass()
    assert restored.label.lower() == "shield"
    assert restored.parent == "C1"
