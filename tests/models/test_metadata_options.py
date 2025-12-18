from datetime import datetime

import pytest

from filare.errors import MetadataValidationError
from filare.models.metadata import (
    AuthorSignature,
    FakeMetadataFactory,
    FakePageTemplateConfigFactory,
    Metadata,
    PageTemplateConfig,
    PageTemplateTypes,
    RevisionSignature,
    SheetSizes,
)
from filare.models.options import (
    FakeImportedSVGOptionsFactory,
    FakePageOptionsFactory,
    get_page_options,
)


def test_metadata_builds_authors_and_revisions(basic_metadata):
    assert basic_metadata.authors_list[0].role == "created"
    assert basic_metadata.revisions_list[0].revision == "a"
    assert basic_metadata.template.orientation.value in ("landscape", "portrait")


def test_metadata_name_appends_pn(basic_metadata):
    assert basic_metadata.name.startswith("PN-1-out")


def test_page_options_parses_from_parsed_data():
    data = {"options": {"bgcolor_connector": "0xFF0000", "notes_width": "80mm"}}
    options = get_page_options(data, "foo")
    assert "ff0000" in str(options.bgcolor_connector).lower()
    assert options.notes_width == "80mm"


def test_metadata_generator_and_lists(tmp_path):
    md = Metadata(
        title="T",
        pn="P",
        company="C",
        address="A",
        output_dir=tmp_path,
        output_name="o",
        sheet_total=1,
        sheet_current=1,
        sheet_name="S",
        titlepage=tmp_path / "titlepage",
        output_names=["titlepage"],
        files=["f.yml"],
        use_qty_multipliers=False,
        multiplier_file_name="m.txt",
        authors={"created": AuthorSignature(name="Alice", date="2024-01-01")},
        revisions={
            "a": RevisionSignature(name="Bob", date="2024-01-02", changelog="init")
        },
    )
    assert "Filare" in md.generator
    assert md.authors_list[0].role == "created"
    assert md.revisions_list[0].revision == "a"
    pages_md = md.pages_metadata
    assert pages_md.output_dir == tmp_path


def test_author_signature_date_parsing():
    from filare.models.metadata import AuthorSignature

    sig = AuthorSignature(name="A", date="TBD")
    assert sig.date == "TBD"
    assert AuthorSignature(name="A", date=None).date is None
    dt = datetime.now()
    assert AuthorSignature(name="A", date=dt).date == dt
    assert AuthorSignature(name="A", date="n/a").date == "n/a"
    # unsupported type passes through unchanged
    assert AuthorSignature(name="A", date=123).date == 123
    with pytest.raises(MetadataValidationError):
        AuthorSignature(name="A", date="01/01/2024")


def test_page_template_config_orientation_defaults():
    from filare.models.metadata import Orientations, PageTemplateConfig, SheetSizes

    tpl = PageTemplateConfig(sheetsize=SheetSizes.A4)
    assert tpl.orientation == Orientations.portrait
    tpl2 = PageTemplateConfig(sheetsize=SheetSizes.A3)
    assert tpl2.orientation == Orientations.landscape


def test_fake_metadata_factory_builds_nested_sections(tmp_path):
    metadata = FakeMetadataFactory.create(output_dir=tmp_path)
    assert metadata.title
    assert metadata.authors
    assert metadata.revisions
    assert metadata.template is not None
    assert metadata.output_dir == tmp_path
    pages = metadata.pages_metadata
    assert pages.output_dir == tmp_path
    assert metadata.generator.startswith("Filare")


def test_fake_page_options_factory_variants():
    options = FakePageOptionsFactory.create(with_svg=True, with_bg=True)
    assert options.bgcolor is not None
    assert options.bgcolor_node is not None
    assert options.diagram_svg is not None
    assert options.diagram_svg.src.endswith(".svg")
    assert isinstance(options.bom_row_height, float)


def test_fake_page_template_config_factory_orientation_randomized():
    tpl = FakePageTemplateConfigFactory.create()
    assert tpl.name in PageTemplateTypes
    assert tpl.sheetsize in SheetSizes
    assert tpl.orientation is None or tpl.orientation.name in ("landscape", "portrait")
