from wireviz.models.component import ComponentModel
from wireviz.models.dataclasses import BomCategory, Component
from wireviz.models.numbers import NumberAndUnit


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
