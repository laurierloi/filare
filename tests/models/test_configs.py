import yaml

from filare.models.configs import (
    CableConfig,
    ConnectionConfig,
    ConnectorConfig,
    MetadataConfig,
    PageOptionsConfig,
    PinConfig,
    WireConfig,
)


def _round_trip(model):
    if hasattr(model, "model_dump"):
        dumped = model.model_dump(exclude_none=True)
    else:
        dumped = model.dict(exclude_none=True)
    restored = yaml.safe_load(yaml.safe_dump(dumped))
    numeric_keys = (
        "pincount",
        "wirecount",
        "sheet_total",
        "sheet_current",
        "dpi",
    )
    for key in numeric_keys:
        val = restored.get(key)
        if isinstance(val, str) and val.isdigit():
            restored[key] = int(val)
    for key in ("width_mm", "margin_mm"):
        val = restored.get(key)
        if isinstance(val, str):
            try:
                restored[key] = float(val)
            except ValueError:
                pass
    assert restored == dumped


def test_connector_config_round_trip(connector_config_data):
    cfg = ConnectorConfig(**connector_config_data)
    assert cfg.pincount == 2
    assert cfg.loops and isinstance(cfg.loops, list)
    assert all(isinstance(pin, PinConfig) for pin in cfg.pins or [])
    _round_trip(cfg)


def test_connector_config_pincolors_and_loops_dict():
    cfg = ConnectorConfig(
        designator="JX",
        pinlabels=["A", "B"],
        pincolors=[["RD"], ["BK"]],
        loops={"first": "1", "last": "2"},
    )
    assert cfg.pincount == 2
    assert cfg.pincolors == [["RD"], ["BK"]]
    assert isinstance(cfg.loops, list)
    _round_trip(cfg)


def test_connector_config_pincolors_dict_and_pins_dict():
    cfg = ConnectorConfig(
        designator="JY",
        pins={"id": "1", "label": "L1"},
        pincolors={"1": "RD", "2": ["BK"]},
    )
    assert isinstance(cfg.pins, list)
    assert cfg.pincount == 1
    assert cfg.pincolors == {"1": "RD", "2": ["BK"]}
    _round_trip(cfg)


def test_connector_config_pinlabels_tuple_sets_pincount():
    cfg = ConnectorConfig(designator="JZ", pinlabels=("1", "2"))
    assert cfg.pincount == 2
    assert list(cfg.pinlabels) == ["1", "2"]
    _round_trip(cfg)


def test_cable_config_round_trip(cable_config_data):
    cfg = CableConfig(**cable_config_data)
    assert cfg.wirecount == 2
    assert cfg.colors == ["RD", "BK"]
    _round_trip(cfg)


def test_cable_config_colors_string_and_wirecount_derivation():
    cfg = CableConfig(designator="CX", colors="RD")
    assert cfg.colors == ["RD"]
    assert cfg.wirecount == 1
    _round_trip(cfg)


def test_cable_config_wirecount_preserved_when_set():
    cfg = CableConfig(designator="CY", wirecount=3, wires=[])
    assert cfg.wirecount == 3
    _round_trip(cfg)


def test_wire_config_round_trip(wire_config_data):
    cfg = WireConfig(**wire_config_data)
    assert cfg.color == "GN"
    _round_trip(cfg)


def test_connection_config_endpoint_coercion(connection_config_data):
    cfg = ConnectionConfig(**connection_config_data)
    assert cfg.endpoints == ["J1:1", "J2:1"]
    _round_trip(cfg)


def test_connection_config_accepts_tuple_and_set():
    cfg = ConnectionConfig(endpoints=("J1:1", "J2:2"), color=["RD"])
    assert cfg.endpoints == ["J1:1", "J2:2"]
    cfg2 = ConnectionConfig(endpoints={"J1:1", "J2:3"})
    assert set(cfg2.endpoints) == {"J1:1", "J2:3"}


def test_page_options_config_formats_none_and_list():
    cfg = PageOptionsConfig(formats=None)
    assert cfg.formats is None
    cfg2 = PageOptionsConfig(formats=["svg", "pdf"])
    assert cfg2.formats == ["svg", "pdf"]
    _round_trip(cfg2)


def test_metadata_config_round_trip(metadata_config_data):
    cfg = MetadataConfig(**metadata_config_data)
    assert cfg.authors["created"]["name"] == "Alice"
    assert cfg.files == ["doc.txt"]
    _round_trip(cfg)


def test_page_options_format_coercion(page_options_config_data):
    cfg = PageOptionsConfig(**page_options_config_data)
    assert cfg.formats == ["svg"]
    _round_trip(cfg)
