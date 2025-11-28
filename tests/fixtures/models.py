import pytest

from wireviz.models.bom import BomEntry
from wireviz.models.cable import Cable
from wireviz.models.connector import Connector, Loop, PinClass
from wireviz.models.metadata import Metadata, PageTemplateConfig, PageTemplateTypes
from wireviz.models.options import PageOptions, get_page_options
from wireviz.models.numbers import NumberAndUnit
from wireviz.models.partnumber import PartNumberInfo
from wireviz.models.colors import MultiColor
from wireviz.models.dataclasses import (
    BomCategory,
    Component,
    QtyMultiplierCable,
    QtyMultiplierConnector,
)
from wireviz.models.configs import (
    CableConfig,
    ConnectionConfig,
    ConnectorConfig,
    MetadataConfig,
    PageOptionsConfig,
    PinConfig,
    WireConfig,
)


@pytest.fixture
def connector_args():
    return {
        "designator": "X1",
        "pincount": 3,
        "pinlabels": ["A", "B", "C"],
        "pincolors": ["RD", "GN", "BU"],
        "loops": [{"first": "A", "second": "B", "show_label": True}],
    }


@pytest.fixture
def connector(connector_args):
    return Connector(**connector_args)


@pytest.fixture
def cable_args():
    return {
        "designator": "C1",
        "wirecount": 2,
        "colors": ["RD", "BK"],
        "length": NumberAndUnit(2, "m"),
        "additional_components": [
            Component(
                type="Sleeve",
                category=BomCategory.ADDITIONAL,
                qty=NumberAndUnit(1, None),
                qty_multiplier=QtyMultiplierCable.LENGTH,
            )
        ],
    }


@pytest.fixture
def cable(cable_args):
    return Cable(**cable_args)


@pytest.fixture
def basic_metadata(tmp_path):
    return Metadata(
        title="Test Harness",
        pn="PN-1",
        company="Acme",
        address="123 Road",
        output_dir=tmp_path,
        output_name="out",
        sheet_total=1,
        sheet_current=1,
        sheet_name="SHEET",
        titlepage=tmp_path / "titlepage",
        output_names=["titlepage"],
        files=[],
        use_qty_multipliers=False,
        multiplier_file_name="qty.txt",
        template=PageTemplateConfig(name=PageTemplateTypes.din_6771, sheetsize="A4"),
        authors={"created": {"name": "Alice", "date": "2023-01-01"}},
        revisions={"a": {"name": "Bob", "date": "2023-01-02", "changelog": "init"}},
    )


@pytest.fixture
def basic_page_options():
    return PageOptions(bgcolor="0xFFFFFF", bgcolor_connector="0xCCCCCC")


@pytest.fixture
def bom_entry_sample():
    return BomEntry(
        qty=NumberAndUnit(2, None),
        partnumbers=PartNumberInfo(pn="PN-BOM"),
        id="1",
        description="Test Part",
        category=BomCategory.ADDITIONAL,
        designators=["X1"],
        per_harness={"H1": {"qty": NumberAndUnit(1, None)}},
    )


@pytest.fixture
def pin_pair():
    return (
        PinClass(index=0, id="1", label="L1", color=MultiColor("RD"), parent="X1"),
        PinClass(index=1, id="2", label="L2", color=MultiColor("BK"), parent="X2"),
    )


@pytest.fixture
def page_options_factory():
    def _factory(data):
        return get_page_options(data, "testpage")

    return _factory


@pytest.fixture
def connector_config_data():
    return {
        "designator": "J1",
        "pinlabels": ["1", "2"],
        "pincolors": ["RD", "GN", "BU"],
        "pins": [{"label": "A", "color": "RD"}, {"label": "B", "color": "GN"}],
        "loops": {"first": "1", "second": "2"},
        "images": ["front.png"],
        "style": "Header",
    }


@pytest.fixture
def cable_config_data():
    return {
        "designator": "C1",
        "wirecount": 2,
        "colors": ["RD", "BK"],
        "length": "2 m",
        "shields": [{"name": "S1"}],
        "wires": [{"label": "WA", "color": ["RD", "BK"]}],
    }


@pytest.fixture
def wire_config_data():
    return {"label": "SIG", "color": "GN", "gauge": "22 AWG", "length": "1 m"}


@pytest.fixture
def connection_config_data():
    return {
        "endpoints": ("J1:1", "J2:1"),
        "net": "SIG1",
        "color": "RD",
        "wire": "W1",
        "bundle": "B1",
    }


@pytest.fixture
def metadata_config_data(tmp_path):
    return {
        "title": "Harness Config",
        "pn": "PN-123",
        "company": "ACME",
        "output_dir": str(tmp_path),
        "output_name": "demo",
        "files": ["doc.txt"],
        "sheet_total": 1,
        "sheet_current": 1,
        "sheet_name": "SHEET",
        "titlepage": str(tmp_path / "titlepage"),
        "output_names": ["titlepage"],
        "authors": {"created": {"name": "Alice", "date": "2024-01-01"}},
        "revisions": {"a": {"name": "Bob", "date": "2024-01-02", "changelog": "init"}},
        "template": {"name": "din-6771", "sheetsize": "A4"},
        "use_qty_multipliers": True,
        "multiplier_file_name": "qty.txt",
    }


@pytest.fixture
def page_options_config_data():
    return {
        "bgcolor": "#ffffff",
        "bgcolor_connector": "#eeeeee",
        "connector_overview_style": "compressed",
        "font": "Arial",
        "dpi": 300,
        "width_mm": 210.0,
        "margin_mm": 10.0,
        "formats": "svg",
    }


@pytest.fixture
def config_models_factory():
    def _factory(model_class, data):
        return model_class(**data)

    return _factory
