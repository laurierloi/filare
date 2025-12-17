import pytest

from filare.models.templates import FakeSimpleTemplateFactory, SimpleTemplateModel
from filare.render.templates import get_template


def test_simple_template_render_minimal():
    model = FakeSimpleTemplateFactory()()
    assert isinstance(model, SimpleTemplateModel)

    rendered = get_template("simple.html").render(model.to_render_dict())

    assert model.title in rendered
    assert model.description in rendered
    assert model.diagram in rendered
    assert model.notes in rendered
    assert model.bom in rendered


@pytest.mark.render
def test_simple_template_container_options():
    model = FakeSimpleTemplateFactory(
        diagram_container_class="diagram-default",
        diagram_container_style="max-height:50mm;",
    )()
    rendered = get_template("simple.html").render(model.to_render_dict())

    assert "diagram-default" in rendered
    assert "max-height:50mm;" in rendered


@pytest.mark.render
@pytest.mark.parametrize(
    "fontname,bgcolor,generator",
    [
        ("Arial", "#FFFFFF", "Filare"),
        ("Helvetica", "#DDDDDD", "CustomGen"),
    ],
)
def test_simple_template_options(fontname, bgcolor, generator):
    model = FakeSimpleTemplateFactory(
        generator=generator,
        options={"fontname": fontname, "bgcolor": bgcolor},
    )()
    rendered = get_template("simple.html").render(model.to_render_dict())

    assert fontname in rendered
    assert bgcolor in rendered
    assert generator in rendered


@pytest.mark.render
def test_simple_template_custom_classes():
    model = FakeSimpleTemplateFactory()()
    model.diagram_container_class = "diagram-class"
    model.diagram_container_style = "height:100px;"

    rendered = get_template("simple.html").render(model.to_render_dict())

    assert model.diagram_container_class in rendered
    assert model.diagram_container_style in rendered
