from pathlib import Path

import graphviz
import pytest

from filare.models.dataclasses import Connector, Cable, WireClass, Side, Loop
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
