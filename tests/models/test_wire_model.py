from filare.models.colors import MultiColor
from filare.models.dataclasses import ShieldClass, WireClass
from filare.models.numbers import NumberAndUnit
from filare.models.wire import (
    FakeShieldModelFactory,
    FakeWireModelFactory,
    ShieldModel,
    WireModel,
)


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


def test_fake_wire_factory_variants():
    model = FakeWireModelFactory.create(
        with_additional=True, with_bg=True, with_colors=False, with_gauge=False
    )
    assert model.color is None
    assert model.bgcolor is not None and model.bgcolor_title is not None
    assert model.additional_components
    clone = model.to_wireclass()
    assert clone.designator.startswith("W")
    assert clone.category is not None
    assert clone.additional_components == model.additional_components


def test_fake_shield_factory_defaults_and_lengths():
    model = FakeShieldModelFactory.create(with_length=False, with_colors=True)
    assert model.label.lower() == "shield"
    assert model.length is None
    restored = model.to_wireclass()
    assert restored.label.lower() == "shield"
    assert restored.color is not None
