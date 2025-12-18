from pathlib import Path

from filare.models.document import (
    DocumentRepresentation,
    FakeDocumentManifestEntryFactory,
    FakeDocumentManifestFactory,
    FakeDocumentRepresentationFactory,
)
from filare.models.notes import FakeNotesFactory
from filare.models.page import (
    FakeBOMPageFactory,
    FakeCutPageFactory,
    FakeHarnessPageFactory,
    FakeTerminationPageFactory,
    FakeTitlePageFactory,
)


def test_fake_document_manifest_factories():
    manifest_entry = FakeDocumentManifestEntryFactory.create()
    assert manifest_entry.path.endswith(".yml")
    manifest = FakeDocumentManifestFactory.create(documents=[manifest_entry])
    assert manifest.documents
    assert manifest.documents[0].name
    assert manifest.title_metadata


def test_fake_page_factories_types():
    assert FakeHarnessPageFactory.create().type.value == "harness"
    assert FakeBOMPageFactory.create().type.value == "bom"
    assert FakeCutPageFactory.create().type.value == "cut"
    assert FakeTerminationPageFactory.create().type.value == "termination"
    assert FakeTitlePageFactory.create().type.value == "title"


def test_fake_document_representation_factory(tmp_path):
    doc = FakeDocumentRepresentationFactory.create()
    assert isinstance(doc, DocumentRepresentation)
    assert doc.pages and doc.metadata
    out_path = tmp_path / "doc.yml"
    doc.to_yaml(out_path)
    loaded = DocumentRepresentation.from_yaml(out_path)
    assert loaded.pages
    assert loaded.metadata


def test_fake_notes_factory_html():
    notes = FakeNotesFactory.create()
    html = notes.as_html_list()
    assert "<li>" in html or notes.notes == []
