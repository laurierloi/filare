import itertools

import pytest

from filare.models.templates import FakeDin6771TemplateFactory
from filare.models.templates.din_6771_template_model import Din6771TemplateModel


def test_din_6771_template_render_minimal():
    model = FakeDin6771TemplateFactory(with_notes=True, with_bom=True)()
    assert isinstance(model, Din6771TemplateModel)

    rendered = model.render()

    assert model.diagram in rendered
    assert model.metadata.template.sheetsize.value in rendered
    if model.notes:
        assert model.notes in rendered
    if model.bom:
        assert model.bom in rendered


@pytest.mark.render
@pytest.mark.parametrize(
    "with_notes,with_bom,bom_rows,bom_row_height",
    list(itertools.product([True, False], [True, False], [1, 2], [3.0, 5.0])),
)
def test_din_6771_template_toggle_sections(
    with_notes, with_bom, bom_rows, bom_row_height
):
    model = FakeDin6771TemplateFactory(
        with_notes=with_notes,
        with_bom=with_bom,
        bom_rows=bom_rows,
        bom_row_height=bom_row_height,
        diagram="<svg><rect /></svg>",
        diagram_container_class="diagram-default",
        diagram_container_style="max-height:50mm;",
    )()
    rendered = model.render()

    # Notes
    if with_notes:
        assert model.notes in rendered
    else:
        assert model.notes is None

    # BOM
    if with_bom:
        assert model.bom in rendered
        assert (
            str(bom_rows) in rendered or str(int(bom_rows * bom_row_height)) in rendered
        )
    else:
        assert model.bom is None

    # Diagram container and title
    assert model.diagram in rendered
    assert "diagram-default" in rendered
    assert "max-height:50mm;" in rendered
