import pytest

from filare.models.cable import Cable
from filare.errors import ComponentValidationError


def test_cable_rejects_unknown_color_code():
    with pytest.raises(ComponentValidationError) as excinfo:
        Cable(designator="W1", wirecount=2, color_code="BAD")
    message = str(excinfo.value)
    assert "W1" in message and "BAD" in message
