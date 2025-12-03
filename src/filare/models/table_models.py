"""Shared table models for BOM, cut, and termination-style tables."""

from typing import List, Optional

from pydantic import BaseModel, Field


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
