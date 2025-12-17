import pytest

from filare.models.templates import FakeConnectorTemplateFactory
from filare.models.templates.connector_template_model import ConnectorTemplateModel


def test_connector_template_render_minimal():
    factory = FakeConnectorTemplateFactory(pincount=2)
    model = factory()

    assert isinstance(model, ConnectorTemplateModel)
    rendered = model.render()

    comp = model.component
    assert comp.designator in rendered
    assert comp.type.clean in rendered
    assert comp.pins[0].id in rendered
    assert comp.pins[-1].id in rendered
    assert f"{comp.pincount}-pin" in rendered


@pytest.mark.render
@pytest.mark.parametrize(
    "ports_left, ports_right, has_pincolors",
    [
        (True, True, True),
        (True, False, False),
        (False, True, True),
        (False, False, False),
    ],
)
def test_connector_template_variants(ports_left, ports_right, has_pincolors):
    factory = FakeConnectorTemplateFactory(pincount=3)
    model = factory()
    comp = model.component
    comp.ports_left = ports_left
    comp.ports_right = ports_right
    comp.has_pincolors = has_pincolors

    rendered = model.render()

    # Ensure pins render regardless of port sides; verify labels or ids appear
    for pin in comp.pins:
        assert pin.id in rendered
    # When pin colors are enabled, expect the color table content
    if has_pincolors:
        assert "bgcolor" in rendered


@pytest.mark.render
@pytest.mark.parametrize("pincount", [1, 10, 50])
def test_connector_template_pincounts(pincount):
    factory = FakeConnectorTemplateFactory(pincount=pincount)
    model = factory()
    comp = model.component

    rendered = model.render()

    assert str(comp.pincount) in rendered
    assert len(comp.pins) == pincount
    # First and last pin IDs should appear
    assert comp.pins[0].id in rendered
    assert comp.pins[-1].id in rendered
