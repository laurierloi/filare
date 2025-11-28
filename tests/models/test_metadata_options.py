from wireviz.models.metadata import Metadata, PageTemplateConfig, PageTemplateTypes
from wireviz.models.options import get_page_options


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
