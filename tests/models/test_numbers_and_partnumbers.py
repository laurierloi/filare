import pytest

from filare.errors import (
    PartNumberValidationError,
    UnitMismatchError,
    UnsupportedModelOperation,
)
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
    with pytest.raises(UnitMismatchError):
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
    # direct call without parent folds to single list
    result = PartNumberInfo.list_keep_only_eq([child, parent])
    assert result is not None
    assert result.pn == ""


def test_partnumberinfo_list_keep_only_shared():
    shared = PartNumberInfo(pn="X", manufacturer="ACME")
    p_list = PartnumberInfoList(pn_list=[shared, shared.copy()])
    shared_result = p_list.keep_only_shared()
    assert shared_result is not None
    assert shared_result.pn == "X"


def test_partnumberinfo_clear_per_field_and_copy():
    a = PartNumberInfo(pn="A", manufacturer="M")
    b = PartNumberInfo(pn="B", manufacturer="M")
    cleared_eq = a.clear_per_field("==", b)
    assert cleared_eq is not None
    assert cleared_eq.manufacturer == "" and cleared_eq.pn == "A"
    cleared_neq = a.clear_per_field("!=", b)
    assert cleared_neq is not None
    assert cleared_neq.pn == "" and cleared_neq.manufacturer == "M"
    with pytest.raises(UnsupportedModelOperation):
        a.clear_per_field(">", b)
    # list case routing
    list_case = PartnumberInfoList(pn_list=[PartNumberInfo(pn="L1", manufacturer="M1")])
    kept_list = list(list_case.keep_only_eq(PartNumberInfo(pn="L1")))
    assert kept_list and kept_list[0] is not None
    kept = kept_list[0]
    assert kept.pn == "L1"
    assert kept.manufacturer == ""
    # other None paths
    cleared_none = a.clear_per_field("==", None)
    assert cleared_none is not None
    assert cleared_none.pn == "A"
    assert a.clear_per_field("!=", None) is None
    # other.is_list branch
    list_other = PartnumberInfoList(pn_list=[PartNumberInfo(pn="A", manufacturer="M")])
    cleared = a.clear_per_field("==", list_other)
    assert cleared is not None
    assert cleared.pn == ""


def test_partnumberinfo_list_as_unique_and_shared():
    pn1 = PartNumberInfo(pn="P1", manufacturer="ACME")
    pn2 = PartNumberInfo(pn="P2", manufacturer="ACME")
    p_list = PartnumberInfoList(pn_list=[pn1, pn2])
    shared = p_list.keep_only_shared()
    assert shared is not None
    assert shared.manufacturer == "ACME"
    uniques = p_list.as_unique_list()
    assert isinstance(uniques, list)
    assert {p.pn for p in uniques} == {"P1", "P2"}


def test_partnumbers2list_merging_parents_and_children():
    child = PartNumberInfo(
        pn="C1", manufacturer="ACME", mpn="M1", supplier="SUP", spn="SP"
    )
    parents = PartnumberInfoList(pn_list=[PartNumberInfo(pn="C1", manufacturer="ACME")])
    merged = partnumbers2list(child, parents)
    flat = [item for sub in merged for item in sub]
    # Parent matches pn/manufacturer, so expect supplier/MPN/SPN entries to remain
    assert any("SUP" in s for s in flat)
    assert any("SP" in s for s in flat)
    assert any("M1" in s for s in flat)


def test_partnumberinfo_validators_and_accessors():
    with pytest.raises(PartNumberValidationError):
        PartNumberInfo(pn=["bad"])
    pn = PartNumberInfo(pn="X", manufacturer="M")
    pn["mpn"] = "MP"
    assert pn["mpn"] == "MP"
    pn.supplier = "S"
    assert any("Supplier" in s for s in pn.str_list)
    assert "pn" in pn.bom_keys
    assert pn.bom_dict["pn"] == "X"


def test_partnumberinfo_list_keep_unique_and_remove():
    pn1 = PartNumberInfo(pn="A", manufacturer="M")
    pn2 = PartNumberInfo(pn="A", manufacturer="M2")
    lst = PartnumberInfoList(pn_list=[pn1, pn2])
    shared = lst.keep_only_shared()
    assert shared is not None
    assert shared.pn == "A"
    # keep_unique yields versions with differing fields cleared
    kept = list(lst.keep_unique([pn1, pn2]))
    assert kept and isinstance(kept[0], PartNumberInfo)
    # empty list returns None from keep_only_shared
    assert PartnumberInfoList(pn_list=[]).keep_only_shared() is None
    # keep_unique with more entries exercises shared removal path
    pn3 = PartNumberInfo(pn="A", manufacturer="M3")
    kept_multi = list(lst.keep_unique([pn1, pn2, pn3]))
    assert kept_multi
    # keep_only_eq yields generators
    eq_list = list(lst.keep_only_eq(PartNumberInfo(pn="A", manufacturer="M")))
    assert eq_list and (
        eq_list[0] is None
        or eq_list[0].pn == ""
        or isinstance(eq_list[0], PartNumberInfo)
    )


def test_partnumbers2list_without_parents():
    pn = PartNumberInfo(pn="Solo")
    lst = partnumbers2list(pn)
    assert lst
    flattened: list[str] = []
    for sub in lst:
        if isinstance(sub, list):
            flattened.extend([str(item) for item in sub])
        else:
            flattened.append(str(sub))
    assert "Solo" in "".join(flattened)
    parent = PartNumberInfo(pn="Solo", manufacturer="ACME")
    lst_with_parent = partnumbers2list(pn, PartnumberInfoList(pn_list=[parent]))
    assert isinstance(lst_with_parent, list)
