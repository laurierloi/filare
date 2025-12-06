import pytest
from datetime import datetime

from filare.models.metadata import Metadata, PageTemplateConfig, PageTemplateTypes
from filare.models.options import get_page_options
from filare.errors import MetadataValidationError


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
        authors={"created": {"name": "Alice", "date": "2024-01-01"}},
        revisions={"a": {"name": "Bob", "date": "2024-01-02", "changelog": "init"}},
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
    from filare.models.metadata import PageTemplateConfig, SheetSizes, Orientations

    tpl = PageTemplateConfig(sheetsize=SheetSizes.A4)
    assert tpl.orientation == Orientations.portrait
    tpl2 = PageTemplateConfig(sheetsize=SheetSizes.A3)
    assert tpl2.orientation == Orientations.landscape
