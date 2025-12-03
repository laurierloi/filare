"""Page models used within DocumentRepresentation."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class PageType(str, Enum):
    title = "title"
    harness = "harness"
    bom = "bom"
    cut = "cut"
    termination = "termination"


class PageBase(BaseModel):
    """Base page info shared by all page types."""

    type: PageType = Field(..., description="Page type identifier")
    name: Optional[str] = Field(None, description="Logical page name or designator")

    model_config = ConfigDict(extra="allow")


class HarnessPage(PageBase):
    """Page representing a harness diagram."""

    formats: List[str] = Field(
        default_factory=list, description="Requested output formats"
    )

    model_config = ConfigDict(extra="allow")


class BOMPage(PageBase):
    """Page representing a BOM table."""

    include: bool = True
    formats: List[str] = Field(
        default_factory=list, description="Requested output formats"
    )

    model_config = ConfigDict(extra="allow")


class CutPage(PageBase):
    """Page representing a wire cut table/diagram."""

    include: bool = False
    formats: List[str] = Field(
        default_factory=list, description="Requested output formats"
    )

    model_config = ConfigDict(extra="allow")


class TerminationPage(PageBase):
    """Page representing a termination table/diagram."""

    include: bool = False
    formats: List[str] = Field(
        default_factory=list, description="Requested output formats"
    )

    model_config = ConfigDict(extra="allow")


class TitlePage(PageBase):
    """Page representing a title page/front matter."""

    include: bool = True
    formats: List[str] = Field(
        default_factory=list, description="Requested output formats"
    )

    model_config = ConfigDict(extra="allow")
