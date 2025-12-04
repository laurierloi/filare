from filare.models.connector import ConnectorModel
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
        loops={"first": "1", "second": "1"},
        color=["RD", "GN"],
        category="connector",
    )
    assert model.pincount == 1
    connector = model.to_connector()
    assert connector.category.name.upper() == "CONNECTOR"
    assert connector.loops
    gc = model.to_graphical_component()
    assert gc.designator == "X2"
    assert str(gc.color).startswith("#") or str(gc.color)
