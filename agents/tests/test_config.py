import pytest

from orchestrator.config import ManifestError, load_manifest

pytestmark = pytest.mark.agent


def test_load_manifest_with_defaults(tmp_path):
    manifest = tmp_path / "manifest.yml"
    manifest.write_text(
        """
defaults:
  workspace: work
  env_file: env/.env
  ssh_key: keys/id_rsa
  branch: main
sessions:
  - id: alpha
    role: FEATURE
    goal: "Do work"
    tags: [fast, demo]
"""
    )

    sessions = load_manifest(manifest)
    assert len(sessions) == 1
    session = sessions[0]
    assert session.id == "alpha"
    assert session.role == "FEATURE"
    assert session.branch == "main"
    assert session.workspace == (tmp_path / "work")
    assert session.env_file == (tmp_path / "env/.env")
    assert session.ssh_key == (tmp_path / "keys/id_rsa")
    assert session.tags == ["fast", "demo"]
    assert session.manifest_path == manifest.resolve()


def test_manifest_requires_branch(tmp_path):
    manifest = tmp_path / "manifest.yml"
    manifest.write_text(
        """
sessions:
  - id: missingbranch
    role: FEATURE
    workspace: work
    env_file: env/.env
    ssh_key: keys/id_rsa
"""
    )

    with pytest.raises(ManifestError):
        load_manifest(manifest)


def test_duplicate_ids_raise(tmp_path):
    manifest = tmp_path / "manifest.yml"
    manifest.write_text(
        """
defaults:
  workspace: work
  env_file: env/.env
  ssh_key: keys/id_rsa
  branch: main
sessions:
  - id: dup
    role: FEATURE
  - id: dup
    role: TOOLS
"""
    )

    with pytest.raises(ManifestError):
        load_manifest(manifest)
