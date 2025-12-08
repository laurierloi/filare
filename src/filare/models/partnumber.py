from functools import reduce
from typing import Any, ClassVar, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

USING_PYDANTIC_V1 = False


from filare.errors import PartNumberValidationError, UnsupportedModelOperation
from filare.models.utils import awg_equiv, mm2_equiv, remove_links


class PartNumberInfo(BaseModel):
    """Container for part-identifying metadata used in BOM output."""

    pn: Optional[str] = ""
    manufacturer: Optional[str] = ""
    mpn: Optional[str] = ""
    supplier: Optional[str] = ""
    spn: Optional[str] = ""
    is_list: bool = False

    BOM_KEY_TO_COLUMNS: ClassVar[Dict[str, str]] = {
        "pn": "P/N",
        "manufacturer": "Manufacturer",
        "mpn": "MPN",
        "supplier": "Supplier",
        "spn": "SPN",
    }

    def __bool__(self):
        """Evaluate truthy if any identifying field is set."""
        return bool(
            self.pn or self.manufacturer or self.mpn or self.supplier or self.spn
        )

    def __hash__(self):
        return hash((self.pn, self.manufacturer, self.mpn, self.supplier, self.spn))

    def __eq__(self, other):
        return hash(self) == hash(other)

    @classmethod
    def model_validate(cls, *args, **kwargs):
        try:
            return super().model_validate(*args, **kwargs)
        except ValidationError as exc:
            value = None
            errors = exc.errors()
            if errors:
                value = errors[0].get("input", value)
            raise PartNumberValidationError(
                value if value is not None else exc
            ) from exc

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as exc:
            value = None
            errors = exc.errors()
            if errors:
                value = errors[0].get("input", value)
            raise PartNumberValidationError(
                value if value is not None else exc
            ) from exc

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    @field_validator("pn", "manufacturer", "mpn", "supplier", "spn", mode="before")
    def _clean_arg(cls, v):
        if isinstance(v, list):
            from filare.errors import PartNumberValidationError

            raise PartNumberValidationError(v)
        return remove_links("" if v is None else str(v))

    @property
    def bom_keys(self):
        """Return ordered BOM field keys."""
        return list(self.BOM_KEY_TO_COLUMNS.keys())

    @property
    def bom_dict(self):
        """Return a dict of BOM fields keyed by internal names."""
        return {k: self[k] for k in self.bom_keys}

    @property
    def str_list(self):
        """Return a human-readable list of formatted part metadata strings."""
        l = ["", "", ""]
        if self.pn:
            l[0] = f"P/N: {self.pn}"
        l[1] = self.manufacturer
        if self.mpn:
            if not l[1]:
                l[1] = "MPN"
            l[1] += ": "
            l[1] += self.mpn
        elif l[1]:
            l[1] = "Manufacturer: " + l[1]
        l[2] = self.supplier
        if self.spn:
            if not l[2]:
                l[2] = "SPN"
            l[2] += ": "
            l[2] += self.spn
        elif l[2]:
            l[2] = "Supplier: " + l[2]
        return [i for i in l if i]

    def copy(self):
        """Shallow copy of part number fields."""
        return PartNumberInfo(
            pn=self.pn,
            manufacturer=self.manufacturer,
            mpn=self.mpn,
            supplier=self.supplier,
            spn=self.spn,
        )

    def clear_per_field(self, op, other):
        """Clear matching or non-matching fields based on an operator."""
        part = self.copy()

        if other is None:
            if op == "==":
                return part
            elif op == "!=":
                return None
            else:
                raise UnsupportedModelOperation(f"op {op} not supported")

        if other.is_list:
            for item in other.pn_list:
                part = part.clear_per_field(op, item)
        else:
            for k in ["pn", "manufacturer", "mpn", "supplier", "spn"]:
                if op == "==":
                    if part[k] == other[k]:
                        part[k] = ""
                elif op == "!=":
                    if part[k] != other[k]:
                        part[k] = ""
                else:
                    raise UnsupportedModelOperation(f"op {op} not supported")
        return part

    def keep_only_eq(self, other):
        return self.clear_per_field("!=", other)

    def remove_eq(self, other):
        return self.clear_per_field("==", other)

    @staticmethod
    def list_keep_only_eq(partnumbers):
        pn = partnumbers[0]
        for p in partnumbers:
            pn = pn.keep_only_eq(p)
        return pn

    def as_list(self, parent_partnumbers=None):
        return partnumbers2list(self, parent_partnumbers)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
    )


class PartnumberInfoList(BaseModel):
    pn_list: List[PartNumberInfo] = []
    is_list: bool = True

    def keep_only_shared(self):
        uniques = set(tuple(self.pn_list))
        if not uniques:
            return

        shared = reduce(lambda x, y: x.keep_only_eq(y), uniques)
        return shared

    def as_unique_list(self):
        return list(set(tuple(self.pn_list)))

    def keep_only_eq(self, other):
        for pn in self.pn_list:
            yield pn.keep_only_eq(other)

    def remove_eq(self, other):
        for pn in self.pn_list:
            yield pn.remove_eq(other)

    def keep_unique(self, other):
        kept = []
        for pn_1 in self.pn_list:
            for pn_2 in self.pn_list:
                if pn_1 == pn_2:
                    continue
                eq = pn_1.keep_only_eq(pn_2)
                if eq:
                    kept.append(eq)
        if not kept:
            shared = self.keep_only_shared()
            if shared:
                for pn in other:
                    yield pn.remove_eq(shared)
            else:
                yield from other
        else:
            shared = reduce(lambda x, y: x.keep_only_eq(y), kept)
            for pn in other:
                yield pn.remove_eq(shared)

    def as_list(self, parent_partnumbers=None):
        for pn in self.pn_list:
            yield pn.as_list()

    if USING_PYDANTIC_V1:

        class Config:
            arbitrary_types_allowed = True

    else:
        model_config = ConfigDict(arbitrary_types_allowed=True)


def partnumbers2list(
    partnumbers: PartNumberInfo,
    parent_partnumbers: Union[PartNumberInfo, PartnumberInfoList, None] = None,
) -> List[str]:
    if not isinstance(partnumbers, list):
        partnumbers = [partnumbers]

    # if there's no parent, fold
    if parent_partnumbers is None:
        return PartNumberInfo.list_keep_only_eq(partnumbers).str_list

    if parent_partnumbers is not None:
        if isinstance(parent_partnumbers, PartNumberInfo):
            parent_partnumbers = PartnumberInfoList([parent_partnumbers])
    partnumbers = parent_partnumbers.keep_unique(partnumbers)

    return [p.str_list for p in partnumbers if p]
