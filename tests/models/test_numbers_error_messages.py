import pytest

from filare.models.numbers import NumberAndUnit


def test_number_and_unit_invalid_string_context():
    with pytest.raises(ValueError) as excinfo:
        NumberAndUnit.to_number_and_unit("abc m")
    assert "abc m" in str(excinfo.value)
    assert "number" in str(excinfo.value).lower()
