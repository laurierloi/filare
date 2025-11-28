from wireviz.models.cable import CableModel


def test_cable_model_to_cable_with_colors(cable_config_data):
    model = CableModel(**cable_config_data)
    cable = model.to_cable()
    assert cable.designator == "C1"
    assert cable.wirecount == 2
    assert len(cable.colors) == 2
    assert cable.length.number == 2


def test_cable_model_with_color_code():
    model = CableModel(designator="C2", wirecount=3, color_code="DIN")
    cable = model.to_cable()
    assert cable.wirecount == 3
    assert len(cable.colors) == 3
    assert cable.colors[0]  # not empty
