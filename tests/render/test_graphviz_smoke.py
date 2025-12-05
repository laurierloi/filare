from pathlib import Path

import graphviz
import pytest

from filare.models.dataclasses import Connector, Cable, WireClass, Loop
from filare.models.types import Side
from filare.models.colors import SingleColor
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


def test_node_cable_template_loads():
    cable = Cable(designator="W1", wirecount=2)
    rendered = gv.gv_node_cable(cable)
    assert "table" in rendered.lower()


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
    wire1 = WireClass(index=0)
    wire2 = WireClass(index=1)
    # Graphviz uses pin number for port naming; wire index maps to pin index
    wire1.pin = 1  # type: ignore[attr-defined]
    wire2.pin = 2  # type: ignore[attr-defined]
    c.loops = [Loop(first=wire1, second=wire2, side=Side.LEFT)]
    loops = gv.gv_connector_loops(c)
    assert loops and len(loops[0]) == 3


def test_connector_loops_right_and_missing_side():
    c = make_connector("X1", 2)
    c.ports_left = False
    c.ports_right = True
    wire1 = WireClass(index=0)
    wire2 = WireClass(index=1)
    wire1.pin = 1  # type: ignore[attr-defined]
    wire2.pin = 2  # type: ignore[attr-defined]
    c.loops = [Loop(first=wire1, second=wire2, side=Side.RIGHT)]
    loops = gv.gv_connector_loops(c)
    assert loops[0][1].endswith(":p1r:e")

    c.ports_right = False
    with pytest.raises(Exception):
        gv.gv_connector_loops(c)


def test_gv_edge_wire_builds_ports(monkeypatch):
    class DummyHarness:
        def __init__(self):
            self.connectors = {
                "X1": make_connector("X1", 1),
                "X2": make_connector("X2", 1),
            }

    harness = DummyHarness()
    cable = Cable(designator="W1", wirecount=1)
    wire = WireClass(parent=cable, index=0, color=SingleColor("RD"))
    conn_from = WireClass(parent="X1", index=0)
    conn_to = WireClass(parent="X2", index=0)

    class DummyConnection:
        from_ = conn_from
        to = conn_to
        via = wire

    color, left1, left2, right1, right2 = gv.gv_edge_wire(
        harness, cable, DummyConnection()
    )
    assert "#000000" in color
    assert "X1" in left1
    # wire parent is a Cable; the port includes cable designator implicitly
    assert "w1" in left2
    assert "X2" in right2


def test_gv_edge_wire_handles_missing_endpoints():
    class DummyHarness:
        connectors = {}

    cable = Cable(designator="W1", wirecount=1)
    wire = WireClass(parent=cable, index=0, color=None)

    class DummyConnection:
        from_ = None
        to = None
        via = wire

    color, left1, left2, right1, right2 = gv.gv_edge_wire(
        DummyHarness(), cable, DummyConnection()
    )
    assert color == "#000000"
    assert left1 is None and left2 is None and right1 is None and right2 is None


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

    options = type("Opts", (), {"bgcolor": SingleColor("WH"), "bgcolor_node": SingleColor("BK"), "fontname": "Arial"})
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
