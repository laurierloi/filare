import yaml

from filare.models.interface.base import FilareInterfaceModel
from filare.models.interface.factories import (
    FakeCableInterfaceFactory,
    FakeConnectionInterfaceFactory,
    FakeConnectorInterfaceFactory,
    FakeMetadataInterfaceFactory,
    FakeOptionsInterfaceFactory,
)


def test_interface_model_to_yaml_round_trip():
    meta = FakeMetadataInterfaceFactory.build()
    dumped = meta.to_yaml()
    loaded = yaml.safe_load(dumped)
    rebuilt = type(meta)(**loaded)
    assert rebuilt.title == meta.title
    assert rebuilt.template.name


def test_factories_build_valid_models():
    connector = FakeConnectorInterfaceFactory.build()
    cable = FakeCableInterfaceFactory.build()
    options = FakeOptionsInterfaceFactory.build()
    assert connector.designator.startswith("J")
    assert cable.wirecount > 0
    assert options.include_bom is True


def test_connection_factory_allows_partial_endpoints():
    # Build several times to cover optional endpoints
    for _ in range(5):
        conn = FakeConnectionInterfaceFactory.build()
        assert conn.via.parent
        # At least one of from_/to may be present; via is mandatory.
        assert conn.from_ is not None or conn.to is not None


def test_json_schema_has_descriptions():
    schema = FilareInterfaceModel.model_json_schema()
    # schema_version description from base Field should be present
    assert "schema_version" in schema.get("properties", {})
    assert schema["properties"]["schema_version"].get("description")
