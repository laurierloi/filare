from wireviz.models.connector import ConnectorModel
from wireviz.models.types import BomCategory


def test_connector_model_to_dataclass(connector_config_data):
    connector_model = ConnectorModel(**connector_config_data, category=BomCategory.CONNECTOR)
    assert connector_model.pincount == 2
    connector = connector_model.to_connector()
    assert connector.designator == "J1"
    assert connector.pincount == 2
    assert connector.loops


def test_connector_model_defaults():
    model = ConnectorModel(designator="X1", pinlabels=["1", "2"], pincolors=["RD", "GN"])
    connector = model.to_connector()
    assert connector.pinlabels == ["1", "2"]
    assert connector.pincount == 2
    assert connector.pincolors[0] == "RD"
