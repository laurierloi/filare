import pytest

from filare.models.templates import (
    FakeSimpleConnectorTemplateFactory,
    SimpleConnectorTemplateModel,
)
from filare.render.templates import get_template


def test_simple_connector_template_render_minimal():
    model = FakeSimpleConnectorTemplateFactory()()
    assert isinstance(model, SimpleConnectorTemplateModel)

    rendered = get_template("simple-connector.html").render(model.to_render_dict())

    assert model.component.type.clean in rendered
    assert str(model.component.pincount) in rendered
    assert model.component.pins_to_show()[0].id in rendered


@pytest.mark.render
def test_simple_connector_without_color():
    model = FakeSimpleConnectorTemplateFactory(show_color=False)()
    rendered = get_template("simple-connector.html").render(model.to_render_dict())

    assert "colorbar" not in rendered or model.component.color is None
