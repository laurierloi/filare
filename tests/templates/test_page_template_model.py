import pytest

from filare.models.templates import FakePageTemplateFactory, PageTemplateModel
from filare.models.templates.titleblock_template_model import (
    FakeTitleblockTemplateFactory,
)


def test_page_template_render_minimal():
    model = FakePageTemplateFactory()()

    assert isinstance(model, PageTemplateModel)
    rendered = model.render()

    assert model.metadata.generator in rendered
    assert model.metadata.template.sheetsize.value in rendered
    assert model.titleblock in rendered


@pytest.mark.render
@pytest.mark.parametrize(
    "fontname,bgcolor_hex,titleblock_rows,titleblock_row_height",
    [
        ("Arial", "#FFFFFF", 3, 5.0),
        ("Helvetica", "#DDDDDD", 4, 6.0),
    ],
)
def test_page_template_options(
    fontname, bgcolor_hex, titleblock_rows, titleblock_row_height
):
    model = FakePageTemplateFactory(
        options={
            "fontname": fontname,
            "bgcolor": {"html": bgcolor_hex, "code_en": None},
            "titleblock_rows": titleblock_rows,
            "titleblock_row_height": titleblock_row_height,
        }
    )()
    rendered = model.render()

    assert fontname in rendered
    assert bgcolor_hex in rendered
    assert str(titleblock_rows) in rendered


@pytest.fixture
def rendered_titleblock():
    model = FakeTitleblockTemplateFactory()()
    return model.render()


@pytest.mark.render
def test_page_template_with_rendered_titleblock(rendered_titleblock):
    model = FakePageTemplateFactory(titleblock=rendered_titleblock)()
    rendered = model.render()

    assert rendered_titleblock in rendered
    assert model.metadata.template.sheetsize.value in rendered
