from filare.models.colors import SingleColor
from filare.models.connector import (
    ConnectorModel,
    FakeConnectorModelFactory,
    FakeGraphicalComponentModelFactory,
)
from filare.models.image import Image
from filare.models.types import BomCategory, Side


def test_connector_model_to_dataclass(connector_config_data):
    connector_model = FakeConnectorModelFactory.create(with_loops=True)
    assert connector_model.pincount and connector_model.pincount > 0
    connector = connector_model.to_connector()
    assert connector.designator.startswith("J")
    assert connector.pincount and connector.pincount > 0
    assert connector.loops


def test_connector_model_defaults():
    model = FakeConnectorModelFactory.create(designator="X1", pincount=2)
    connector = model.to_connector()
    assert connector.pinlabels and len(connector.pinlabels) == 2
    assert connector.pincount == 2
    assert connector.pincolors
    assert connector.pincolors[0][0]


def test_connector_model_coercions_and_category():
    model = FakeConnectorModelFactory.create(
        designator="X2",
        pincount=1,
        with_loops=True,
        with_color=True,
        loops=[{"first": "1", "second": "1", "side": Side.LEFT}],
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
    model = FakeConnectorModelFactory.create(
        designator="S1", pincount=1, simple=True, pinlabels=["A"], pincolors=[["RD"]]
    )
    conn = model.to_connector()
    assert conn.pincount == 1
    assert conn.style == "simple"
    assert conn.pinlabels == ["A"]
    assert conn.pincolors[0][0] is not None


def test_graphical_component_validators_and_images():
    base_gc = FakeGraphicalComponentModelFactory.create(
        designator="G1",
        category=BomCategory.CONNECTOR,
        with_color=False,
        with_bg=False,
    ).model_dump()
    base_gc.pop("bgcolor", None)
    base_gc.pop("bgcolor_title", None)
    base_gc.pop("image", None)
    model = ConnectorModel(
        **base_gc,
        pins=[{"label": "1"}],
        bgcolor=SingleColor("custom"),
        bgcolor_title=SingleColor("blue"),
        image=Image(src="example.png", height=1, width=1),
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
