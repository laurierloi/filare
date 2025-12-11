import pytest

from filare.models.templates import BomTemplateModel, FakeBomTemplateFactory
from filare.render.templates import get_template


def test_bom_template_render_minimal():
    factory = FakeBomTemplateFactory(rows=2)
    model = factory()
    assert isinstance(model, BomTemplateModel)

    rendered = get_template("bom.html").render(model.to_render_dict())

    assert "BOM" in rendered
    for header in model.bom.headers:
        assert header in rendered
    for row in model.bom.content:
        for cell in row:
            assert cell in rendered


@pytest.mark.render
@pytest.mark.parametrize(
    "rows, reverse",
    [
        (1, False),
        (10, False),
        (50, False),
        (10, True),
    ],
)
def test_bom_template_rows_and_header_variants(rows, reverse):
    factory = FakeBomTemplateFactory(rows=rows, options={"reverse": reverse})
    model = factory()
    rendered = get_template("bom.html").render(model.to_render_dict())

    # Headers appear either before or after rows based on reverse flag
    assert model.bom.headers[0] in rendered
    # Check some row content
    assert model.bom.content[0][0] in rendered
    assert model.bom.content[-1][0] in rendered
