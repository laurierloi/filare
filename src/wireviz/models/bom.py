from typing import ClassVar, Dict, List, Union

import tabulate as tabulate_module
from pydantic import BaseModel, Field, root_validator

from wireviz.models.numbers import NumberAndUnit
from wireviz.models.partnumber import PartNumberInfo
from wireviz.models.utils import remove_links
from wireviz.render.templates import get_template


class BomEntryBase(BaseModel):
    qty: NumberAndUnit
    partnumbers: PartNumberInfo
    id: str = ""
    amount: Union[NumberAndUnit, None] = None
    qty_multiplier: Union[int, float, object] = 1
    description: str = ""
    category: str = ""
    ignore_in_bom: bool = False
    designators: List = Field(default_factory=list)
    per_harness: Dict = Field(default_factory=dict)
    MAX_PRINTED_DESCRIPTION: ClassVar[int] = 40
    MAX_PRINTED_DESIGNATORS: ClassVar[int] = 2
    restrict_printed_lengths: bool = True
    scaled_per_harness: bool = False
    BOM_KEY_TO_COLUMNS: ClassVar[Dict[str, str]] = {
        "id": "#",
        "qty": "Qty",
        "unit": "Unit",
        "description": "Description",
        "designators": "Designators",
        "per_harness": "Per Harness",
    }

    class Config:
        arbitrary_types_allowed = True
        allow_mutation = True

    @root_validator
    def _scale_qty(cls, values):
        try:
            values["qty_multiplier"] = float(values.get("qty_multiplier", 1))
        except Exception:
            values["qty_multiplier"] = 1
        if values.get("qty") is not None:
            values["qty"] *= float(values.get("qty_multiplier", 1))
        if values.get("amount") is not None:
            values["amount"] *= float(values.get("qty_multiplier", 1))
        return values

    def __hash__(self):
        return hash((self.partnumbers, self.description))

    def __eq__(self, other):
        if isinstance(other, list):
            return False
        elif isinstance(other, BomEntryBase):
            return hash(self) == hash(other)

    def __add__(self, other):
        if isinstance(other, list):
            return [self + o for o in other]
        elif isinstance(other, BomEntryBase):
            self.qty += other.qty
            self.designators += other.designators
            return self
        else:
            raise NotImplementedError(f"__add__ for {type(other)}")

    def scale_per_harness(self, multipliers):
        if self.scaled_per_harness:
            logging.warning(
                "scale_per_harness() was called twice for item with no ID"
            )
            return
        for k, v in self.per_harness.items():
            if k in multipliers:
                v["qty"] *= multipliers[k]
        self.scaled_per_harness = True

    @property
    def unit(self):
        return self.qty.unit if self.qty.unit else ""

    @property
    def description_clean(self):
        desc = self.description
        if self.restrict_printed_lengths:
            desc = (
                self.description[: self.MAX_PRINTED_DESCRIPTION] + "..."
                if len(self.description) > self.MAX_PRINTED_DESCRIPTION
                else self.description
            )
        return remove_links(desc)

    @property
    def designators_str(self):
        if self.restrict_printed_lengths and len(self.designators) > 0:
            designators = self.designators[: self.MAX_PRINTED_DESIGNATORS]
            more = len(self.designators) - len(designators)
            return ", ".join(designators) + (" (...)" if more > 0 else "")
        else:
            return ", ".join(self.designators)

    @property
    def per_harness_str(self):
        if not self.per_harness:
            return ""
        parts = []
        for harness, data in self.per_harness.items():
            qty = data["qty"]
            parts.append(f"{harness}: {qty}")
        return "; ".join(parts)

    def as_list(self, filter_empty=False, include_per_harness=False):
        lst = [
            getattr(self, "id", ""),
            self.qty.number,
            self.unit,
            self.description_clean,
            self.designators_str,
        ]
        if include_per_harness:
            lst.append(self.per_harness_str)
        if not filter_empty:
            return lst
        return [item for item in lst if item]


class BomEntry(BomEntryBase):
    id: str = ""
    BOM_KEY_TO_COLUMNS: ClassVar[Dict[str, str]] = BomEntryBase.BOM_KEY_TO_COLUMNS.copy()

    def __repr__(self):
        return f"{self.id}: {self.partnumbers}, {self.qty}"

    class Config:
        arbitrary_types_allowed = True
        allow_mutation = True

class BomRender:
    def __init__(self, header, rows, strip_empty_columns=False, columns_class=None):
        self.header = header
        self.rows = rows
        self.strip_empty_columns = strip_empty_columns
        self.options = None
        self.content = rows
        if columns_class is None:
            self.columns_class = [""] * len(header)
        else:
            self.columns_class = columns_class

    def as_tsv(self):
        tsv = tabulate_module.tabulate(self.rows, self.header, tablefmt="tsv")
        return tsv

    @property
    def headers(self):
        return self.header

    def render(self, page_options=None, bom_options=None):
        if page_options is None:
            page_options = {}
        if bom_options is None:
            bom_options = BomRenderOptions()
        if self.strip_empty_columns:
            # remove empty columns in header and rows
            index_to_remove = [i for i, v in enumerate(self.header) if v == ""]
            stripped_rows = self.rows.copy()
            stripped_header = self.header.copy()
            for i in index_to_remove[::-1]:
                stripped_header.pop(i)
                for row in stripped_rows:
                    row.pop(i)

            header = stripped_header
            rows = stripped_rows
        else:
            header = self.header
            rows = self.rows

        self.options = bom_options
        return get_template("bom.html").render(
            {
                "bom": self,
                "table_header": header,
                "table_rows": rows,
                "options": page_options,
            }
        )


class BomRenderOptions:
    def __init__(
        self,
        restrict_printed_lengths=False,
        filter_entries=True,
        no_per_harness=False,
        reverse=False,
    ):
        self.restrict_printed_lengths = restrict_printed_lengths
        self.filter_entries = filter_entries
        self.no_per_harness = no_per_harness
        self.reverse = reverse


class BomContent(dict):
    def __init__(self, bom):
        self._bom = bom
        super().__init__(bom)

    def filter_entries(self, restrict_printed_lengths=True, filter_entries=True):
        # TODO: Refactor to not mutate in place
        for _, entry in self.items():
            entry.restrict_printed_lengths = restrict_printed_lengths

        # remove entries without partnumbers or quantities
        if filter_entries:
            _keys_to_remove = []
            for key, entry in self.items():
                if not entry.partnumbers or entry.qty.number <= 0:
                    _keys_to_remove.append(key)
            for key in _keys_to_remove:
                del self[key]

    def get_bom_render(self, options=BomRenderOptions()):
        """Return a BomRender object using class properties for BOM rendering options."""

        self.filter_entries(
            options.restrict_printed_lengths,
            options.filter_entries,
        )

        header = [
            BomEntry.BOM_KEY_TO_COLUMNS["id"],
            BomEntry.BOM_KEY_TO_COLUMNS["qty"],
            BomEntry.BOM_KEY_TO_COLUMNS["unit"],
            BomEntry.BOM_KEY_TO_COLUMNS["description"],
            BomEntry.BOM_KEY_TO_COLUMNS["designators"],
        ]
        include_per_harness = not getattr(options, "no_per_harness", False)
        if include_per_harness:
            header.append(BomEntry.BOM_KEY_TO_COLUMNS["per_harness"])
        rows = []
        columns_class = [
            "bom_col_id",
            "bom_col_qty",
            "bom_col_unit",
            "bom_col_description",
            "bom_col_designators",
        ]
        if include_per_harness:
            columns_class.append("bom_col_per_harness")

        # TODO: in reverse mode we probably want to re-sort BOM by description here

        for entry in self.values():
            row = entry.as_list(False, include_per_harness=include_per_harness)
            rows.append(row)
        if options.reverse:
            rows = rows[::-1]
        return BomRender(header, rows, columns_class=columns_class)


def print_bom_table(bom):
    header = [
        BomEntry.BOM_KEY_TO_COLUMNS["id"],
        BomEntry.BOM_KEY_TO_COLUMNS["qty"],
        BomEntry.BOM_KEY_TO_COLUMNS["unit"],
        BomEntry.BOM_KEY_TO_COLUMNS["description"],
        BomEntry.BOM_KEY_TO_COLUMNS["designators"],
    ]

    rows = []
    for entry in bom.values():
        rows.append(entry.as_list())

    print(tabulate_module.tabulate(rows, header))
