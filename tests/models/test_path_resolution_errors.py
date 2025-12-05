import pytest

from filare.models.utils import smart_file_resolve


def test_smart_file_resolve_includes_search_paths(tmp_path):
    missing = tmp_path / "missing.png"
    with pytest.raises(FileNotFoundError) as excinfo:
        smart_file_resolve(missing.name, [tmp_path])
    message = str(excinfo.value)
    assert "missing.png" in message
    assert str(tmp_path) in message
