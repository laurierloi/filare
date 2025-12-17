import pytest

from filare.models.templates import (
    ComponentTableTemplateModel,
    FakeComponentTableTemplateFactory,
)
from filare.render.templates import get_template


@pytest.mark.render
@pytest.mark.parametrize("partnumber_count", [1, 3])
def test_component_table_renders_partnumbers(partnumber_count):
    model = FakeComponentTableTemplateFactory(
        partnumber_count=partnumber_count, with_partnumbers=True
    )()
    rendered = get_template("component_table.html").render(model.to_render_dict())

    assert isinstance(model.component.partnumbers, object)
    if partnumber_count == 1:
        assert model.component.partnumbers.pn in rendered  # type: ignore[union-attr]
    else:
        shared_manufacturer = model.component.partnumbers.pn_list[0].manufacturer  # type: ignore[union-attr]
        assert shared_manufacturer in rendered
    assert model.component.designator in rendered


@pytest.mark.render
def test_component_table_additional_components():
    model = FakeComponentTableTemplateFactory(
        additional_component_count=2, with_partnumbers=False, with_notes=False
    )()
    rendered = get_template("component_table.html").render(model.to_render_dict())

    for subitem in model.component.additional_components:
        assert subitem.bom_entry.description in rendered
        assert str(subitem.bom_entry.qty.number) in rendered


@pytest.mark.render
def test_component_table_notes_and_image():
    model = FakeComponentTableTemplateFactory(
        with_notes=True, with_image=True, with_partnumbers=False
    )()
    rendered = get_template("component_table.html").render(model.to_render_dict())

    assert model.component.notes.clean in rendered  # type: ignore[union-attr]
    assert model.component.image.src in rendered  # type: ignore[union-attr]
