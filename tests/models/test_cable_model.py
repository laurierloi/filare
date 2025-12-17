from filare.models.cable import CableModel
from filare.models.colors import MultiColor
from filare.models.numbers import NumberAndUnit


def test_cable_model_to_cable_with_colors(cable_config_data):
    model = CableModel(**cable_config_data)
    cable = model.to_cable()
    assert cable.designator == "C1"
    assert cable.wirecount == 2
    assert len(cable.colors) == 2
    assert cable.length is not None and cable.length.number == 2


def test_cable_model_with_color_code():
    model = CableModel(designator="C2", wirecount=3, color_code="DIN")
    cable = model.to_cable()
    assert cable.wirecount == 3
    assert len(cable.colors) == 3
    assert cable.colors[0]  # not empty


def test_cable_model_coercions_and_defaults():
    model = CableModel(
        designator="C3",
        colors=["RD"],
        wirelabels=[],
        shield=False,
        gauge=NumberAndUnit.to_number_and_unit("1 mm"),
        length=NumberAndUnit.to_number_and_unit("2 m"),
    )
    assert model.colors == ["RD"]
    assert model.wirelabels == []
    assert model.shield is False
    assert str(model.gauge) == "1 mm"
    assert str(model.length) == "2 m"


def test_cable_model_multicolor_repeats_for_wirecount():
    model = CableModel(designator="C4", wirecount=3, color=MultiColor("RDBU"))
    assert [str(color) for color in model.colors] == ["RD", "BU", "RD"]


def test_cable_model_shield_string_preserved():
    model = CableModel(designator="C5", wirecount=1, shield="foil")
    assert model.shield == "foil"
