from filare.models.colors import MultiColor
from filare.models.connections import (
    ConnectionModel,
    FakeConnectionModelFactory,
    FakeLoopModelFactory,
    FakePinModelFactory,
    LoopModel,
    PinModel,
)
from filare.models.dataclasses import Connection, Loop, PinClass
from filare.models.types import Side
from filare.models.wire import WireModel


def test_pin_model_roundtrip():
    pin = PinClass(index=0, id="1", label="A", color=MultiColor("RD"), parent="X1")
    model = PinModel.from_pinclass(pin)
    cloned = model.to_pinclass()
    assert cloned.id == pin.id
    assert cloned.color is not None and len(cloned.color) > 0
    first_color = cloned.color[0]
    assert first_color is not None and first_color.html is not None
    assert first_color.html.startswith("#")
    assert cloned.parent == "X1"


def test_loop_model_roundtrip():
    first = PinClass(index=0, id="1", label="A", color=MultiColor("RD"), parent="X1")
    second = PinClass(index=1, id="2", label="B", color=MultiColor("GN"), parent="X1")
    loop = Loop(first=first, second=second, side=Side.LEFT)
    model = LoopModel.from_loop(loop)
    reconstructed = model.to_loop()
    assert reconstructed.first is not None and reconstructed.first.id == "1"
    assert reconstructed.second is not None and reconstructed.second.id == "2"
    assert reconstructed.side == Side.LEFT


def test_connection_model_roundtrip():
    left = PinClass(index=0, id="1", label="A", color=MultiColor("RD"), parent="X1")
    wire = PinClass(index=1, id="w1", label="", color=MultiColor("BK"), parent="W1")
    right = PinClass(index=2, id="2", label="B", color=MultiColor("BU"), parent="X2")
    connection = Connection(from_=left, via=wire, to=right)
    model = ConnectionModel.from_connection(connection)
    reconstructed = model.to_connection()
    assert reconstructed.from_ is not None and reconstructed.from_.id == "1"
    assert reconstructed.via is not None and reconstructed.via.id == "w1"
    assert reconstructed.to is not None and reconstructed.to.id == "2"


def test_connection_model_accepts_wire_models():
    left = PinClass(index=0, id="1", label="A", color=MultiColor("RD"), parent="X1")
    wire_model = WireModel(parent="W1", index=0, id="w1", color=MultiColor("BK"))
    right = PinClass(index=1, id="2", label="B", color=MultiColor("GN"), parent="X2")
    model = ConnectionModel(from_=left, via=wire_model, to=right)
    reconstructed = model.to_connection()
    assert reconstructed.via is not None and reconstructed.via.id == "w1"
    assert reconstructed.via is not None and reconstructed.via.parent == "W1"


def test_fake_pin_and_loop_factories():
    pin = FakePinModelFactory.create(with_color=True, anonymous=True)
    assert pin.color is not None
    assert getattr(pin, "anonymous_flag", False) is True
    loop = FakeLoopModelFactory.create(with_color=True)
    loop_dc = loop.to_loop()
    assert loop_dc.first is not None and loop_dc.second is not None
    assert loop_dc.color is None or isinstance(loop_dc.color, MultiColor)


def test_fake_connection_factory_variants():
    connection = FakeConnectionModelFactory.create(
        allow_partial=True, use_wire=True, use_shield=False
    )
    built = connection.to_connection()
    assert built.via is not None
    if built.from_ is None or built.to is None:
        # at least one endpoint should be present even when partial
        assert bool(built.from_) or bool(built.to)
    full_connection = FakeConnectionModelFactory.create(
        allow_partial=False, use_shield=True
    )
    converted = full_connection.to_connection()
    assert converted.from_ is not None
    assert converted.to is not None
    assert converted.via is not None
