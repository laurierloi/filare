from filare.models.configs import (
    CableConfig,
    ConnectionConfig,
    ConnectorConfig,
    FakeCableConfigFactory,
    FakeConnectionConfigFactory,
    FakeConnectorConfigFactory,
    FakeMetadataConfigFactory,
    FakePageOptionsConfigFactory,
    FakePinConfigFactory,
    FakeWireConfigFactory,
    MetadataConfig,
    PageOptionsConfig,
    PinConfig,
    WireConfig,
)


def test_fake_pin_and_connector_configs():
    pin = FakePinConfigFactory.create()
    assert isinstance(pin, PinConfig)
    assert pin.id
    connector = FakeConnectorConfigFactory.create()
    assert isinstance(connector, ConnectorConfig)
    assert connector.pins and connector.pinlabels
    assert connector.pincount == len(connector.pins)


def test_fake_wire_and_cable_configs():
    wire = FakeWireConfigFactory.create()
    assert isinstance(wire, WireConfig)
    assert wire.color
    cable = FakeCableConfigFactory.create()
    assert isinstance(cable, CableConfig)
    assert cable.wires and cable.wirecount == len(cable.wires)
    assert cable.colors


def test_fake_connection_metadata_page_options_configs():
    conn = FakeConnectionConfigFactory.create()
    assert isinstance(conn, ConnectionConfig)
    assert len(conn.endpoints) == 2
    meta = FakeMetadataConfigFactory.create()
    assert isinstance(meta, MetadataConfig)
    assert meta.title and meta.pn
    opts = FakePageOptionsConfigFactory.create()
    assert isinstance(opts, PageOptionsConfig)
    assert opts.formats and "svg" in opts.formats
