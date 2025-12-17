from filare.models.colors import MultiColor, SingleColor
from filare.models.connector import ConnectorModel
from filare.models.image import Image
from filare.models.types import BomCategory


def test_connector_model_to_dataclass(connector_config_data):
    connector_model = ConnectorModel(
        **connector_config_data, category=BomCategory.CONNECTOR
    )
    assert connector_model.pincount == 2
    connector = connector_model.to_connector()
    assert connector.designator == "J1"
    assert connector.pincount == 2
    assert connector.loops


def test_connector_model_defaults():
    model = ConnectorModel(
        designator="X1", pinlabels=["1", "2"], pincolors=["RD", "GN"]
    )
    connector = model.to_connector()
    assert connector.pinlabels == ["1", "2"]
    assert connector.pincount == 2
    assert connector.pincolors[0] == "RD"


def test_connector_model_coercions_and_category():
    model = ConnectorModel(
        designator="X2",
        pins=[{"id": "1"}],
        loops=[{"first": "1", "second": "1"}],
        color=MultiColor(["RD", "GN"]),
        category=BomCategory.CONNECTOR,
    )
    assert model.pincount == 1
    connector = model.to_connector()
    assert connector.category is not None
    if isinstance(connector.category, str):
        assert connector.category.upper() == "CONNECTOR"
    else:
        assert connector.category.name.upper() == "CONNECTOR"
    assert connector.loops
    gc = model.to_graphical_component()
    assert gc.designator == "X2"
    assert gc.color is not None
    assert str(gc.color).startswith("#") or str(gc.color)


def test_connector_model_simple_style_and_pinlabels_dict():
    model = ConnectorModel(
        designator="S1",
        style="simple",
        pinlabels=["A"],
        pincolors=["RD"],
    )
    conn = model.to_connector()
    assert conn.pincount == 1
    assert conn.style == "simple"
    assert conn.pinlabels == ["A"]
    assert conn.pincolors[0] == "RD"


def test_graphical_component_validators_and_images():
    model = ConnectorModel(
        designator="G1",
        type=None,
        notes=None,
        bgcolor=SingleColor("custom"),
        bgcolor_title=SingleColor("blue"),
        image=Image(src="example.png", height=1, width=1),
        category=BomCategory.CONNECTOR,
        pins=[{"label": "1"}],
    )
    assert isinstance(model.image, Image)
    assert model.bgcolor is not None
    assert model.bgcolor.html
    assert model.bgcolor_title is not None
    assert model.bgcolor_title.html
    gc = model.to_graphical_component()
    assert gc.designator == "G1"
    assert gc.category is not None
    if isinstance(gc.category, str):
        assert gc.category.upper() == "CONNECTOR"
    else:
        assert gc.category.name.upper() == "CONNECTOR"

    other = ConnectorModel(designator="G2", category="unknown", pins=[{"label": "1"}])
    assert other.category == "unknown"
