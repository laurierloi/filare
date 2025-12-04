import pytest

from filare.models.configs import (
    CableConfig,
    ConnectorConfig,
    ConnectionConfig,
    WireConfig,
)
from filare.models.template_inputs import (
    TemplateCable,
    TemplateConnection,
    TemplateConnector,
    TemplatePin,
    TemplateWire,
)


def test_template_connector_from_config(connector_config_data):
    cfg = ConnectorConfig(**connector_config_data)
    connector = TemplateConnector.from_config(cfg)
    assert connector.designator == cfg.designator
    assert len(connector.pins) == 2
    assert all(isinstance(pin, TemplatePin) for pin in connector.pins)
    assert connector.loops and connector.loops[0]["first"] == "1"
    dumped = connector.model_dump(exclude_none=True)
    assert dumped["designator"] == "J1"


def test_template_cable_from_config(cable_config_data):
    cfg = CableConfig(**cable_config_data)
    cable = TemplateCable.from_config(cfg)
    assert cable.designator == cfg.designator
    assert len(cable.wires) == 1  # explicit wires preserved
    assert all(isinstance(w, TemplateWire) for w in cable.wires)
    assert cable.length and float(cable.length.number) == 2.0


def test_template_cable_from_wire_objects(wire_config_data):
    cfg = CableConfig(designator="C2", wires=[WireConfig(**wire_config_data)])
    cable = TemplateCable.from_config(cfg)
    assert cable.wires[0].label == "SIG"
    assert cable.wires[0].color == ["GN"]

def test_template_cable_from_colors_only():
    cfg = CableConfig(designator="C3", colors=["RD", "GN"], length="1 m")
    cable = TemplateCable.from_config(cfg)
    assert [w.color for w in cable.wires] == [["RD"], ["GN"]]
    assert str(cable.length) == "1 m"


def test_template_connection_from_config(connection_config_data):
    cfg = ConnectionConfig(**connection_config_data)
    conn = TemplateConnection.from_config(cfg)
    assert conn.endpoints == ["J1:1", "J2:1"]
    assert conn.color == ["RD"]
    assert conn.net == "SIG1"

def test_template_connection_validates_and_coerces():
    cfg = ConnectionConfig(endpoints=("J1:1", "J2:2"), color="BK", net=None)
    conn = TemplateConnection.from_config(cfg)
    assert conn.endpoints == ["J1:1", "J2:2"]
    assert conn.color == ["BK"]
    assert conn.net is None


def test_template_connector_from_pinlabels():
    cfg = ConnectorConfig(designator="J3", pinlabels=["1", "2"], pincolors=[["RD"], ["BK"]])
    connector = TemplateConnector.from_config(cfg)
    assert len(connector.pins) == 2
    assert connector.pins[0].label == "1"
    assert connector.pins[0].color == ["RD"]
    assert connector.pins[1].color == ["BK"]


def test_template_wire_validators():
    wire = TemplateWire(color="RD", length="2 m")
    assert wire.color == ["RD"]
    assert str(wire.length) == "2 m"


def test_template_models_forbid_extra():
    with pytest.raises(Exception):
        TemplateConnector(designator="JX", pins=[], extra="nope")
