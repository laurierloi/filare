import pytest

from filare.flows.build_harness import _normalize_connection_set
from filare.errors import MultipleSeparatorError


def test_connection_set_multiple_separators_error():
    connection_set = [["A-B-C"]]
    with pytest.raises(MultipleSeparatorError) as excinfo:
        _normalize_connection_set(connection_set, "-", {}, {})
    assert "connections[0]" in str(excinfo.value)
    assert "A-B-C" in str(excinfo.value)
