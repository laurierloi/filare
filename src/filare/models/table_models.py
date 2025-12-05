"""Shared table models for BOM, cut, and termination-style tables."""

from string import ascii_lowercase
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class TableCell(BaseModel):
    """Represents a single cell in a rendered table."""

    value: str = ""
    css_class: Optional[str] = None


class TableRow(BaseModel):
    """A row of table cells."""

    cells: List[TableCell] = Field(default_factory=list)

    @property
    def values(self) -> List[str]:
        return [cell.value for cell in self.cells]


class TablePaginationOptions(BaseModel):
    """Settings for table pagination."""

    rows_per_page: Optional[int] = None
    force_single_page: bool = False
    use_letter_suffix: bool = True

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def enabled(self) -> bool:
        return bool(self.rows_per_page) and not self.force_single_page


class TablePage(BaseModel):
    """A rendered chunk of a table with optional suffix metadata."""

    index: int
    suffix: str = ""
    rows: List[TableRow] = Field(default_factory=list)
    html: str = ""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def with_html(self, html: str) -> "TablePage":
        return TablePage(
            index=self.index, suffix=self.suffix, rows=self.rows, html=html
        )


def letter_suffix(index: int) -> str:
    """Return a letter suffix (a, b, c, …, aa, ab, …) for a zero-based index."""
    if index < 0:
        return ""
    base = len(ascii_lowercase)
    result = ""
    value = index
    while True:
        result = ascii_lowercase[value % base] + result
        value = value // base - 1
        if value < 0:
            break
    return result


def paginate_rows(
    rows: List[TableRow], pagination: TablePaginationOptions
) -> List[TablePage]:
    """Split rows into pages according to the pagination options."""
    if not pagination.enabled or not pagination.rows_per_page:
        return [TablePage(index=0, suffix="", rows=rows)]

    per_page = int(pagination.rows_per_page)
    chunks: List[List[TableRow]] = [
        rows[i : i + per_page] for i in range(0, len(rows), per_page)
    ]
    suffixes: List[str] = []
    if pagination.use_letter_suffix and len(chunks) > 1:
        suffixes = [letter_suffix(idx) for idx in range(len(chunks))]
    else:
        suffixes = ["" for _ in chunks]

    return [
        TablePage(index=idx, suffix=suffixes[idx], rows=chunk)
        for idx, chunk in enumerate(chunks)
    ]
