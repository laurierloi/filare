from enum import Enum
from pathlib import Path
from types import SimpleNamespace

from filare import filare as filare_module
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
from filare.filare import _build_document_representation, _make_jsonable


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
    registry.add("doc.yaml", digest, allow_override=False)
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


def test_parse_returns_document_and_optional_pages(monkeypatch):
    class DummyMeta:
        def dict(self):
            return {"pn": "PN-123"}

    class DummyOptions:
        def __init__(self):
            self.include_bom = True
            self.include_cut_diagram = True
            self.include_termination_diagram = True
            self.formats = ["svg"]

        def dict(self):
            return {
                "include_bom": self.include_bom,
                "include_cut_diagram": self.include_cut_diagram,
                "include_termination_diagram": self.include_termination_diagram,
                "formats": self.formats,
            }

    harness = SimpleNamespace(metadata=DummyMeta(), options=DummyOptions(), notes=None)

    def fake_build_harness_from_files(**kwargs):
        return harness

    monkeypatch.setattr(
        filare_module, "build_harness_from_files", fake_build_harness_from_files
    )

    doc = filare_module.parse(
        inp=[], metadata_files=[], return_types=("document",), output_formats=("svg",)
    )

    assert isinstance(doc, DocumentRepresentation)
    assert any(isinstance(page, CutPage) for page in doc.pages)
    assert any(isinstance(page, TerminationPage) for page in doc.pages)
    assert any(isinstance(page, BOMPage) for page in doc.pages)
    assert doc.extras["options"]["include_cut_diagram"]
    assert doc.extras["options"]["include_termination_diagram"]


def test_make_jsonable_handles_path_and_enum():
    class Dummy(Enum):
        VALUE = "value"

    result = _make_jsonable(
        {"path": Path("a/b.txt"), "choice": Dummy.VALUE, "items": [Path("c/d")]}
    )
    assert result["path"] == "a/b.txt"
    assert result["choice"] == "value"
    assert result["items"] == ["c/d"]
