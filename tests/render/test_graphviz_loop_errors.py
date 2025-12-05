import pytest

from filare.models.dataclasses import Connector, Loop, PinClass
from filare.models.colors import MultiColor
from filare.render.graphviz import gv_connector_loops


def test_gv_connector_loops_requires_side():
    connector = Connector(designator="X1", pincount=2)
    connector.ports_left = False
    connector.ports_right = False
    pin_a = PinClass(index=0, id="1", label="A", color=MultiColor("RD"), parent="X1")
    pin_b = PinClass(index=1, id="2", label="B", color=MultiColor("BK"), parent="X1")
    connector.loops = [Loop(first=pin_a, second=pin_b, side=None)]

    with pytest.raises(ValueError) as excinfo:
        gv_connector_loops(connector)

    assert "X1" in str(excinfo.value)
    assert "no side" in str(excinfo.value)
