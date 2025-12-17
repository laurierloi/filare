import pytest

from filare.models.templates import (
    FakeTitleblockTemplateFactory,
    TitleblockTemplateModel,
)
from filare.models.templates.titleblock_template_model import (
    FakeTemplateTitleblockMetadataFactory,
    FakeTemplateTitleblockOptionsFactory,
)
from filare.render.templates import get_template


@pytest.mark.render
@pytest.mark.parametrize(
    "author_count,revision_count,row_height,with_logo",
    [
        (0, 0, 4.0, False),
        (1, 1, 5.5, True),
        (3, 5, 7.0, True),
    ],
)
def test_titleblock_template_render_variants(
    author_count, revision_count, row_height, with_logo
):
    model = FakeTitleblockTemplateFactory(
        author_count=author_count,
        revision_count=revision_count,
        titleblock_row_height=row_height,
        with_logo=with_logo,
    )()
    assert isinstance(model, TitleblockTemplateModel)

    rendered = get_template("titleblock.html").render(model.to_render_dict())

    assert model.metadata.company in rendered
    assert model.metadata.title in rendered
    assert model.partno in rendered
    assert str(model.metadata.sheet_current) in rendered
    assert f"height: {model.options.titleblock_row_height}mm" in rendered
    if model.metadata.name:
        assert model.metadata.name in rendered
    if model.metadata.authors_list:
        assert model.metadata.authors_list[0].name in rendered
    if model.metadata.revisions_list:
        assert model.metadata.revisions_list[-1].revision in rendered
    if with_logo and model.metadata.logo:
        assert model.metadata.logo in rendered


def test_titleblock_respects_metadata_and_options_overrides():
    metadata = FakeTemplateTitleblockMetadataFactory.create(
        author_count=1, revision_count=1, sheet_total=4
    )
    options = FakeTemplateTitleblockOptionsFactory.create(titleblock_row_height=6.5)
    model = TitleblockTemplateModel(
        metadata=metadata, options=options, partno="PN-9000"
    )

    rendered = get_template("titleblock.html").render(model.to_render_dict())

    assert "PN-9000" in rendered
    assert "Sheet 1" in rendered
    assert "of 4" in rendered
    assert f"height: {options.titleblock_row_height}mm" in rendered
    assert metadata.revisions_list[0].revision in rendered
