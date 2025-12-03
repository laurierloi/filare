from pathlib import Path

from filare.models.document import DocumentHashRegistry, DocumentRepresentation
from filare.models.harness import Harness
from filare.models.notes import Notes
from filare.models.page import (
    BOMPage,
    CutPage,
    HarnessPage,
    PageBase,
    PageType,
    TerminationPage,
    TitlePage,
)
from filare.filare import _build_document_representation


def test_document_representation_round_trip(tmp_path: Path):
    doc = DocumentRepresentation(
        metadata={"title": "Harness", "pn": "PN-1"},
        pages=[PageBase(type=PageType.harness, name="main")],
        notes="remember to torque",
        bom={"items": [{"id": "1", "desc": "wire"}]},
    )
    path = tmp_path / "doc.yaml"
    doc.to_yaml(path)

    loaded = DocumentRepresentation.from_yaml(path)
    assert loaded.metadata["title"] == "Harness"
    assert loaded.pages[0].name == "main"
    assert loaded.notes == "remember to torque"
    assert loaded.bom["items"][0]["id"] == "1"


def test_document_hash_registry_tracks_hashes(tmp_path: Path):
    doc = DocumentRepresentation(metadata={"title": "Harness"})
    digest = doc.compute_hash()
    reg_path = tmp_path / "hashes.yaml"
    registry = DocumentHashRegistry(reg_path)
    registry.load()
    assert not registry.contains("doc.yaml", digest)
    registry.add("doc.yaml", digest)
    registry.save()

    registry2 = DocumentHashRegistry(reg_path)
    registry2.load()
    assert registry2.contains("doc.yaml", digest)


def test_build_document_from_harness(basic_metadata, basic_page_options):
    harness = Harness(
        metadata=basic_metadata, options=basic_page_options, notes=Notes([])
    )
    doc = _build_document_representation(harness)
    assert isinstance(doc, DocumentRepresentation)
    assert doc.metadata.get("pn") == basic_metadata.pn
    assert "options" in doc.extras
    assert isinstance(doc.pages[0], HarnessPage)


def test_document_pages_are_models(tmp_path: Path):
    doc = DocumentRepresentation(
        metadata={"title": "Harness"},
        pages=[HarnessPage(type="harness", name="H1", formats=["svg"])],
    )
    path = tmp_path / "doc.yaml"
    doc.to_yaml(path)

    loaded = DocumentRepresentation.from_yaml(path)
    assert isinstance(loaded.pages[0], HarnessPage)
    assert loaded.pages[0].name == "H1"


def test_document_recognizes_page_types(tmp_path: Path):
    pages = [
        HarnessPage(type=PageType.harness, name="H1"),
        BOMPage(type=PageType.bom, name="BOM"),
        CutPage(type=PageType.cut, name="CUT"),
        TerminationPage(type=PageType.termination, name="TERM"),
        TitlePage(type=PageType.title, name="TITLE"),
    ]
    doc = DocumentRepresentation(metadata={}, pages=pages)
    path = tmp_path / "doc.yaml"
    doc.to_yaml(path)

    loaded = DocumentRepresentation.from_yaml(path)
    assert isinstance(loaded.pages[0], HarnessPage)
    assert isinstance(loaded.pages[1], BOMPage)
    assert isinstance(loaded.pages[2], CutPage)
    assert isinstance(loaded.pages[3], TerminationPage)
