from __future__ import annotations

from typing import Dict, Optional

from pydantic import Field

from filare.models.interface.base import FilareInterfaceModel


class TemplateInterfaceModel(FilareInterfaceModel):
    """Template configuration for documents."""

    name: str = Field(
        default="din-6771", description="Template name to use for rendering."
    )
    sheetsize: str = Field(
        default="A3", description="Sheet size identifier (e.g., A3, A4)."
    )


class AuthorSignatureInterfaceModel(FilareInterfaceModel):
    """Author or reviewer signature information."""

    name: str = Field(..., description="Full name of the author or reviewer.")
    date: Optional[str] = Field(
        None, description="ISO date string representing when the author signed."
    )


class RevisionSignatureInterfaceModel(FilareInterfaceModel):
    """Revision signature with changelog."""

    name: str = Field(
        ..., description="Full name of the person recording the revision."
    )
    date: Optional[str] = Field(None, description="ISO date string for the revision.")
    changelog: Optional[str] = Field(
        None, description="Short description of the revision changes."
    )


class MetadataInterfaceModel(FilareInterfaceModel):
    """Top-level document metadata supplied by the user."""

    title: str = Field(..., description="Document title displayed on the title page.")
    pn: str = Field(..., description="Part number or project identifier.")
    company: str = Field(..., description="Company name for the document.")
    address: str = Field(..., description="Company address for the document.")
    authors: Dict[str, AuthorSignatureInterfaceModel] = Field(
        default_factory=dict,
        description="Mapping of author roles (created, reviewed, approved) to signatures.",
    )
    revisions: Dict[str, RevisionSignatureInterfaceModel] = Field(
        default_factory=dict,
        description="Mapping of revision identifiers to signatures.",
    )
    template: TemplateInterfaceModel = Field(
        default_factory=TemplateInterfaceModel,
        description="Template configuration to drive document rendering defaults.",
    )


class MetadataConfigurationInterfaceModel(FilareInterfaceModel):
    """Configuration options controlling metadata parsing/normalization."""

    # Placeholder for future parsing toggles; keeps a dedicated config object per metadata payload.
    pass
