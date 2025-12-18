import pytest

from filare.models.colors import SingleColor
from filare.models.templates import FakeTitlePageTemplateFactory
from filare.models.templates.page_template_model import FakeTemplatePageMetadataFactory
from filare.models.templates.titleblock_template_model import (
    FakeTitleblockTemplateFactory,
)
from filare.models.templates.titlepage_template_model import (
    FakeTemplateTitlePageOptionsFactory,
    TitlePageTemplateModel,
)


@pytest.fixture
def rendered_titleblock():
    model = FakeTitleblockTemplateFactory(
        author_count=1, revision_count=1, with_logo=False
    )()
    html = model.render()
    return html, model


@pytest.mark.render
@pytest.mark.parametrize(
    "with_notes,with_bom,with_index",
    [
        (True, True, True),
        (True, False, False),
        (False, True, False),
        (False, False, True),
    ],
)
def test_titlepage_template_toggle_sections(
    rendered_titleblock, with_notes, with_bom, with_index
):
    titleblock_html, tb_model = rendered_titleblock
    model = FakeTitlePageTemplateFactory(
        with_notes=with_notes,
        with_bom=with_bom,
        with_index=with_index,
        titleblock=titleblock_html,
    )()
    assert isinstance(model, TitlePageTemplateModel)

    rendered = model.render()

    assert model.metadata.title is not None
    assert model.metadata.title in rendered
    assert (model.notes is not None) == with_notes
    assert (model.bom is not None) == with_bom
    assert (model.index_table is not None) == with_index
    if with_notes:
        assert model.notes is not None
        assert model.notes in rendered
    if with_bom:
        assert model.bom is not None
        assert model.bom in rendered
    if with_index:
        assert model.index_table is not None
        assert model.index_table in rendered
    # Titleblock should be injected into the final render.
    assert tb_model.metadata.company in rendered


def test_titlepage_respects_page_options(rendered_titleblock):
    titleblock_html, tb_model = rendered_titleblock
    bgcolor = SingleColor("#AABBCC")
    options = FakeTemplateTitlePageOptionsFactory.create(
        fontname="Fira Code",
        bgcolor=bgcolor,
        titleblock_rows=4,
        titleblock_row_height=6.5,
        show_notes=True,
        show_bom=False,
        show_index_table=True,
    )
    metadata = FakeTemplatePageMetadataFactory.create(title="Configured Title")
    model = FakeTitlePageTemplateFactory(
        with_notes=True,
        with_bom=False,
        with_index=True,
        options=options,
        metadata=metadata,
        titleblock=titleblock_html,
    )()

    rendered = model.render()

    assert "Configured Title" in rendered
    assert options.fontname is not None
    assert f"font-family:  {options.fontname}" in rendered
    assert bgcolor.html is not None
    assert f"background-color:  {bgcolor.html}" in rendered
    expected_bottom = (options.titleblock_rows + 1) * options.titleblock_row_height + 10
    assert f"bottom: {expected_bottom}mm;" in rendered
    assert model.notes is not None
    assert model.notes in rendered
    assert model.bom is None
    assert model.index_table is not None
    assert model.index_table in rendered
    assert tb_model.metadata.company in rendered
