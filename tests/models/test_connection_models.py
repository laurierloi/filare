from filare.models.connections import ConnectionModel, LoopModel, PinModel
from filare.models.dataclasses import Connection, Loop, PinClass
from filare.models.types import Side


def test_pin_model_roundtrip():
    pin = PinClass(index=0, id="1", label="A", color="RD", parent="X1")
    model = PinModel.from_pinclass(pin)
    cloned = model.to_pinclass()
    assert cloned.id == pin.id
    assert cloned.color[0].html.startswith("#")
    assert cloned.parent == "X1"


def test_loop_model_roundtrip():
    first = PinClass(index=0, id="1", label="A", color="RD", parent="X1")
    second = PinClass(index=1, id="2", label="B", color="GN", parent="X1")
    loop = Loop(first=first, second=second, side="left")
    model = LoopModel.from_loop(loop)
    reconstructed = model.to_loop()
    assert reconstructed.first.id == "1"
    assert reconstructed.second.id == "2"
    assert reconstructed.side == Side.LEFT


def test_connection_model_roundtrip():
    left = PinClass(index=0, id="1", label="A", color="RD", parent="X1")
    wire = PinClass(index=1, id="w1", label="", color="BK", parent="W1")
    right = PinClass(index=2, id="2", label="B", color="BU", parent="X2")
    connection = Connection(from_=left, via=wire, to=right)
    model = ConnectionModel.from_connection(connection)
    reconstructed = model.to_connection()
    assert reconstructed.from_.id == "1"
    assert reconstructed.via.id == "w1"
    assert reconstructed.to.id == "2"
