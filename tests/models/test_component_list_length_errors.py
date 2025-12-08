import pytest

from filare.models.cable import Cable
from filare.errors import ComponentValidationError


def test_part_data_list_length_matches_wirecount():
    with pytest.raises(ComponentValidationError) as excinfo:
        Cable(designator="W1", wirecount=2, pn=["A"], colors=["RD", "BK"])
    assert "W1" in str(excinfo.value)
    assert "wirecount" in str(excinfo.value)
