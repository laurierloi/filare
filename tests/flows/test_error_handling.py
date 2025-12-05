import pytest

from filare.errors import (
    ConnectionCountMismatchError,
    MissingOutputSpecification,
    MultipleSeparatorError,
    FilareFlowException,
)
from filare.flows.build_harness import (
    _normalize_connection_set,
    build_harness_from_files,
)


def test_build_harness_requires_outputs_or_returns(tmp_path):
    dummy = tmp_path / "harness.yml"
    dummy.touch()
    with pytest.raises(MissingOutputSpecification):
        build_harness_from_files(
            inp=[dummy],
            metadata_files=[],
            output_formats=(),
            return_types=(),
        )


def test_normalize_connection_set_rejects_mismatched_lengths():
    connection_set = [{"A": [1]}, {"B": [1, 2]}]
    with pytest.raises(ConnectionCountMismatchError):
        _normalize_connection_set(connection_set, "-", {}, {})


def test_normalize_connection_set_rejects_multiple_separators():
    connection_set = [["TEMP--J1"]]
    with pytest.raises(MultipleSeparatorError):
        _normalize_connection_set(connection_set, "-", {}, {})


def test_build_metadata_type_error_wrapped(tmp_path, monkeypatch):
    dummy = tmp_path / "harness.yml"
    dummy.write_text("metadata: {}")
    monkeypatch.setattr(
        "filare.flows.build_harness._build_metadata",
        lambda *args, **kwargs: (_ for _ in ()).throw(TypeError("bad meta")),
    )
    with pytest.raises(FilareFlowException):
        build_harness_from_files(
            inp=[dummy],
            metadata_files=[],
            output_formats=("html",),
            return_types=("harness",),
        )
