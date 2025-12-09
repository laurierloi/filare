import pytest

from filare.errors import ComponentValidationError
from filare.models.cable import Cable


def test_cable_rejects_unknown_color_code():
    with pytest.raises(ComponentValidationError) as excinfo:
        Cable(designator="W1", wirecount=2, color_code="BAD")
    message = str(excinfo.value)
    assert "W1" in message and "BAD" in message
