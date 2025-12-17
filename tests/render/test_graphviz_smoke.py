from pathlib import Path

import graphviz
import pytest

from filare.errors import UnsupportedLoopSide
from filare.models.cable import CableModel
from filare.models.colors import MultiColor, SingleColor
from filare.models.connections import ConnectionModel, LoopModel, PinModel
from filare.models.connector import ConnectorModel
from filare.models.dataclasses import Cable, Connector, Loop, PinClass, WireClass
from filare.models.types import Side
from filare.models.wire import WireModel
from filare.render import graphviz as gv


def make_connector(designator: str, pins: int, style: str = "default") -> Connector:
    conn = Connector(designator=designator, pincount=pins, style=style)
    conn.ports_left = True
    conn.ports_right = False
    return conn


def test_node_connector_simple_template_loads(tmp_path, monkeypatch):
    c = make_connector("X1", 1, style="simple")
    rendered = gv.gv_node_connector(c)
    assert "<table" in rendered.lower()


def test_node_connector_accepts_model(tmp_path, monkeypatch):
    model = ConnectorModel(designator="X1", pincount=1, style="simple")
    rendered = gv.gv_node_connector(model.to_connector())
    assert "<table" in rendered.lower()


def test_node_cable_template_loads():
    cable = Cable(designator="W1", wirecount=2)
    rendered = gv.gv_node_cable(cable)
    assert "table" in rendered.lower()


def test_node_cable_accepts_model():
    cable_model = CableModel(designator="W1", colors=["RD"], wirecount=1)
    rendered = gv.gv_node_cable(cable_model.to_cable())
    assert "table" in rendered.lower()


def test_connector_template_uses_pin_number_when_label_missing():
    conn = make_connector("X1", 2)
    rendered = gv.gv_node_connector(conn)
    normalized = " ".join(rendered.split())
    assert "None" not in normalized
    assert 'colspan="2"> 1 </td>' in normalized
    assert 'colspan="2"> 2 </td>' in normalized


def test_node_image_attrs_resolves_paths(tmp_path, monkeypatch):
    img_path = tmp_path / "pic.png"
    img_path.write_text("dummy")
    from filare.models.image import Image

    attrs = gv._node_image_attrs(Image(src=str(img_path)))
    assert attrs["image"] == str(img_path.resolve())
    assert attrs.get("imagescale") in (None, "false")


def test_node_image_attrs_relative_with_scale(monkeypatch, tmp_path):
    from filare.models.image import Image

    rel_image = "relpic.png"
    attrs = gv._node_image_attrs(Image(src=rel_image, scale="both", fixedsize=True))
    assert Path(attrs["image"]).is_absolute()
    assert attrs["imagescale"] == "both"
    assert attrs["fixedsize"] == "true"


def test_connector_loops_builds_edges():
    c = make_connector("X1", 2)
    wire1 = PinClass(index=0, id="1", parent="X1")
    wire2 = PinClass(index=1, id="2", parent="X1")
    c.loops = [Loop(first=wire1, second=wire2, side=Side.LEFT)]
    loops = gv.gv_connector_loops(c)
    assert loops and len(loops[0]) == 3


def test_connector_loops_right_and_missing_side():
    c = make_connector("X1", 2)
    c.ports_left = False
    c.ports_right = True
    wire1 = PinClass(index=0, id="1", parent="X1")
    wire2 = PinClass(index=1, id="2", parent="X1")
    c.loops = [Loop(first=wire1, second=wire2, side=Side.RIGHT)]
    loops = gv.gv_connector_loops(c)
    assert loops[0][1].endswith(":p1r:e")

    c.ports_right = False
    with pytest.raises(UnsupportedLoopSide):
        gv.gv_connector_loops(c)


def test_connector_loops_accepts_loop_model():
    c = make_connector("X1", 2)
    c.ports_left = True
    loop_model = LoopModel(
        first=PinModel(parent="X1", id="1", index=0),
        second=PinModel(parent="X1", id="2", index=1),
        side=Side.LEFT,
    )
    loops = gv.gv_connector_loops(c)
    # empty initially, so assign model and retry
    c.loops = [loop_model.to_loop()]
    loops = gv.gv_connector_loops(c)
    assert loops and loops[0][1].startswith("X1")


def test_gv_edge_wire_builds_ports(monkeypatch):
    class DummyHarness:
        def __init__(self):
            self.connectors = {
                "X1": make_connector("X1", 1),
                "X2": make_connector("X2", 1),
            }

    harness = DummyHarness()
    cable = Cable(designator="W1", wirecount=1)
    wire = WireClass(parent="W1", index=0, color=MultiColor(["RD"]))
    conn_from = PinClass(parent="X1", index=0, id="1")
    conn_to = PinClass(parent="X2", index=0, id="1")

    class DummyConnection:
        from_ = conn_from
        to = conn_to
        via = wire

    color, left1, left2, right1, right2 = gv.gv_edge_wire(
        harness, cable, DummyConnection()
    )
    assert "#000000" in color
    assert left1 is not None
    assert "X1" in left1
    # wire parent is a Cable; the port includes cable designator implicitly
    assert left2 is not None
    assert "w1" in left2
    assert right2 is not None
    assert "X2" in right2


def test_gv_edge_wire_handles_missing_endpoints():
    class DummyHarness:
        connectors = {}

    cable = Cable(designator="W1", wirecount=1)
    wire = WireClass(parent="W1", index=0, color=None)

    class DummyConnection:
        from_ = None
        to = None
        via = wire

    color, left1, left2, right1, right2 = gv.gv_edge_wire(
        DummyHarness(), cable, DummyConnection()
    )
    assert color == "#000000"
    assert left1 is None and left2 is None and right1 is None and right2 is None


def test_gv_edge_wire_accepts_connection_model():
    class DummyHarness:
        def __init__(self):
            self.connectors = {
                "X1": make_connector("X1", 1),
                "X2": make_connector("X2", 1),
            }

    harness = DummyHarness()
    cable = Cable(designator="W1", wirecount=1)
    connection_model = ConnectionModel(
        from_=PinModel(parent="X1", id="1", index=0, color=MultiColor(["RD"])),
        via=WireModel(parent="W1", id="1", index=0, color=MultiColor(["BK"])),
        to=PinModel(parent="X2", id="1", index=0, color=MultiColor(["GN"])),
    )
    color, left1, left2, right1, right2 = gv.gv_edge_wire(
        harness, cable, connection_model
    )
    assert "#000000" in color
    assert left1 and right2


def test_set_dot_basics_respects_engine(monkeypatch):
    class DummyDot:
        def __init__(self):
            self.body = []
            self.engine = None
            self.graph_attrs = []
            self.node_attrs = []
            self.edge_attrs = []

        def attr(self, section, **kwargs):
            if section == "graph":
                self.graph_attrs.append(kwargs)
            elif section == "node":
                self.node_attrs.append(kwargs)
            elif section == "edge":
                self.edge_attrs.append(kwargs)

    options = type(
        "Opts",
        (),
        {
            "bgcolor": SingleColor("WH"),
            "bgcolor_node": SingleColor("BK"),
            "fontname": "Arial",
        },
    )
    monkeypatch.setattr("filare.render.graphviz.settings.graphviz_engine", "neato")
    dot = DummyDot()
    gv.set_dot_basics(dot, options)
    assert dot.engine == "neato"
    assert dot.graph_attrs and dot.node_attrs and dot.edge_attrs


def test_set_dot_basics_accepts_dict_colors(monkeypatch):
    class DummyDot:
        def __init__(self):
            self.body = []
            self.engine = None
            self.graph_attrs = []
            self.node_attrs = []
            self.edge_attrs = []

        def attr(self, section, **kwargs):
            if section == "graph":
                self.graph_attrs.append(kwargs)
            elif section == "node":
                self.node_attrs.append(kwargs)
            elif section == "edge":
                self.edge_attrs.append(kwargs)

    opts = type(
        "Opts",
        (),
        {
            "bgcolor": {"html": "#ffffff"},
            "bgcolor_node": {"code_en": "BK"},
            "fontname": "Arial",
        },
    )
    dot = DummyDot()
    gv.set_dot_basics(dot, opts)
    assert dot.graph_attrs[0]["bgcolor"] == "#ffffff"
    assert dot.node_attrs[0]["fillcolor"] in ("#000000", "bk")
