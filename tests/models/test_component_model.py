from filare.models.component import ComponentModel
from filare.models.dataclasses import Component
from filare.models.numbers import NumberAndUnit
from filare.models.types import BomCategory


def test_component_model_to_from_dataclass():
    comp = Component(
        category=BomCategory.ADDITIONAL,
        type="Label",
        pn="PN-1",
        qty=NumberAndUnit(2, None),
        additional_components=[{"type": "Tape", "qty": 1}],
    )
    model = ComponentModel.from_component(comp)
    assert model.category == BomCategory.ADDITIONAL
    assert model.qty.number == 2
    roundtrip = model.to_component()
    assert roundtrip.category == comp.category
    assert roundtrip.qty.number == comp.qty.number
    assert roundtrip.additional_components[0].type.raw == "Tape"
    # parent gets cleared when not a primitive
    comp.parent = {"invalid": True}
    model_with_parent = ComponentModel.from_component(comp)
    assert model_with_parent.parent is None


def test_component_model_validates_fields():
    model = ComponentModel(
        category=BomCategory.CONNECTOR,
        type=["Line1", "Line2"],
        bgcolor="0xFFFFFF",
        qty="3",
    )
    assert model.type.raw == "Line1<br>Line2"
    assert model.qty.number == 3
    assert model.bgcolor.html.lower() in ("#ffffff", "0xffffff")


def test_component_model_additional_coercion_and_categories():
    raw_sub = {"type": "Sub", "category": BomCategory.ADDITIONAL}
    comp_sub = Component(category=BomCategory.ADDITIONAL, type="Inner")
    model_sub = ComponentModel(category="misc", type="text")

    model = ComponentModel(
        category="UnknownCategory",
        type=None,
        additional_components=[model_sub, comp_sub, raw_sub],
    )
    # category string not castable is returned as-is
    assert model.category == "UnknownCategory"
    assert model.type is None
    assert len(model.additional_components) == 3
    assert isinstance(model.additional_components[1], ComponentModel)
    comp = model.to_component()
    assert comp.additional_components[0].type.raw == "text"
