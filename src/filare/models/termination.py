"""Models for per-wire termination details."""

from typing import Optional

from pydantic import BaseModel

from filare.models.numbers import NumberAndUnit


class TerminationEnd(BaseModel):
    """Termination details for one wire end connecting into a component/pin."""

    harness: Optional[str] = None
    connector: Optional[str] = None
    pin: Optional[str] = None
    splice: Optional[str] = None
    crimp: Optional[str] = None
    length: Optional[NumberAndUnit] = None
    notes: Optional[str] = None


class TerminationRow(BaseModel):
    """Both ends of a wire for termination diagrams."""

    from_end: TerminationEnd
    to_end: TerminationEnd
    wire_id: Optional[str] = None
    gauge: Optional[NumberAndUnit] = None
    color: Optional[str] = None
