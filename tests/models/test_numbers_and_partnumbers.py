import pytest

from filare.models.numbers import NumberAndUnit
from filare.models.partnumber import PartNumberInfo, PartnumberInfoList, partnumbers2list


def test_number_and_unit_add_mul_and_to_number():
    a = NumberAndUnit(2, "m")
    b = NumberAndUnit.to_number_and_unit("3 m")
    c = a + b
    assert c.number == 5 and c.unit == "m"
    d = a * 2
    assert d.number == 4 and d.unit == "m"
    with pytest.raises(ValueError):
        _ = a + NumberAndUnit(1, "kg")


def test_partnumberinfo_str_list_and_eq():
    pn = PartNumberInfo(pn="PN1", manufacturer="ACME", mpn="M1", supplier="S", spn="SPN")
    assert pn
    assert "PN1" in pn.str_list[0]
    pn2 = pn.copy()
    assert pn == pn2
    pn2.mpn = "M2"
    assert pn != pn2


def test_partnumbers2list_with_parent_filter():
    child = PartNumberInfo(pn="C1", manufacturer="ACME", mpn="M1")
    parent = PartNumberInfo(pn="P1", manufacturer="ACME", mpn="M1")
    # When identical, child fields matching parent are cleared
    lst = partnumbers2list(child, PartnumberInfoList(pn_list=[parent]))
    # The returned list is list-of-lists when parents are provided; flatten for assertion
    flat = [item for sub in lst for item in sub]
    assert "P1" not in "".join(flat)


def test_partnumberinfo_list_keep_only_shared():
    shared = PartNumberInfo(pn="X", manufacturer="ACME")
    p_list = PartnumberInfoList(pn_list=[shared, shared.copy()])
    assert p_list.keep_only_shared().pn == "X"
