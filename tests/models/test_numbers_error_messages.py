import pytest

from filare.models.cable import Cable
from filare.models.numbers import NumberAndUnit
from filare.errors import InvalidNumberFormat


def test_number_and_unit_invalid_string_context():
    with pytest.raises(InvalidNumberFormat) as excinfo:
        NumberAndUnit.to_number_and_unit("abc m")
    assert "abc m" in str(excinfo.value)
    assert "number" in str(excinfo.value).lower()


def test_cable_length_error_includes_context():
    with pytest.raises(InvalidNumberFormat) as excinfo:
        Cable(designator="W1", wirecount=1, length="abc")
    msg = str(excinfo.value)
    assert "cable w1 length" in msg.lower()
    assert "abc" in msg
