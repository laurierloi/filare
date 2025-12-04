import pytest

from filare.models.numbers import NumberAndUnit
from filare.models.partnumber import (
    PartNumberInfo,
    PartnumberInfoList,
    partnumbers2list,
)


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
    pn = PartNumberInfo(
        pn="PN1", manufacturer="ACME", mpn="M1", supplier="S", spn="SPN"
    )
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


def test_partnumberinfo_clear_per_field_and_copy():
    a = PartNumberInfo(pn="A", manufacturer="M")
    b = PartNumberInfo(pn="B", manufacturer="M")
    cleared_eq = a.clear_per_field("==", b)
    assert cleared_eq.manufacturer == "" and cleared_eq.pn == "A"
    cleared_neq = a.clear_per_field("!=", b)
    assert cleared_neq.pn == "" and cleared_neq.manufacturer == "M"
    with pytest.raises(NotImplementedError):
        a.clear_per_field(">", b)


def test_partnumberinfo_list_as_unique_and_shared():
    pn1 = PartNumberInfo(pn="P1", manufacturer="ACME")
    pn2 = PartNumberInfo(pn="P2", manufacturer="ACME")
    p_list = PartnumberInfoList(pn_list=[pn1, pn2])
    shared = p_list.keep_only_shared()
    assert shared.manufacturer == "ACME"
    uniques = p_list.as_unique_list()
    assert isinstance(uniques, list)
    assert {p.pn for p in uniques} == {"P1", "P2"}


def test_partnumbers2list_merging_parents_and_children():
    child = PartNumberInfo(pn="C1", manufacturer="ACME", mpn="M1", supplier="SUP", spn="SP")
    parents = PartnumberInfoList(pn_list=[PartNumberInfo(pn="C1", manufacturer="ACME")])
    merged = partnumbers2list(child, parents)
    flat = [item for sub in merged for item in sub]
    # Parent matches pn/manufacturer, so expect supplier/MPN/SPN entries to remain
    assert any("SUP" in s for s in flat)
    assert any("SP" in s for s in flat)
    assert any("M1" in s for s in flat)
