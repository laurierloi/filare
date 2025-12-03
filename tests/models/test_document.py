from pathlib import Path

from filare.models.document import DocumentHashRegistry, DocumentRepresentation


def test_document_representation_round_trip(tmp_path: Path):
    doc = DocumentRepresentation(
        metadata={"title": "Harness", "pn": "PN-1"},
        pages=[{"type": "diagram", "name": "main"}],
        notes="remember to torque",
        bom={"items": [{"id": "1", "desc": "wire"}]},
    )
    path = tmp_path / "doc.yaml"
    doc.to_yaml(path)

    loaded = DocumentRepresentation.from_yaml(path)
    assert loaded.metadata["title"] == "Harness"
    assert loaded.pages[0]["name"] == "main"
    assert loaded.notes == "remember to torque"
    assert loaded.bom["items"][0]["id"] == "1"


def test_document_hash_registry_tracks_hashes(tmp_path: Path):
    doc = DocumentRepresentation(metadata={"title": "Harness"})
    digest = doc.compute_hash()
    reg_path = tmp_path / "hashes.yaml"
    registry = DocumentHashRegistry(reg_path)
    registry.load()
    assert not registry.contains(digest)
    registry.add(digest)
    registry.save()

    registry2 = DocumentHashRegistry(reg_path)
    registry2.load()
    assert registry2.contains(digest)
