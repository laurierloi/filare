from __future__ import annotations

from pydantic import Field

from filare.models.interface.base import FilareInterfaceModel


class OptionsInterfaceModel(FilareInterfaceModel):
    """Document-level options controlling rendering and outputs."""

    include_bom: bool = Field(
        default=True,
        description="Whether to include the bill of materials in rendered outputs.",
    )
    include_cut_diagram: bool = Field(
        default=False,
        description="Whether to generate cut diagrams for harness wires.",
    )
    include_termination_diagram: bool = Field(
        default=False,
        description="Whether to generate termination diagrams for harness wires.",
    )
    split_bom_page: bool = Field(
        default=False,
        description="Whether to emit BOM on a dedicated page when rendering documents.",
    )
    split_notes_page: bool = Field(
        default=False,
        description="Whether to emit notes on a dedicated page when rendering documents.",
    )
    split_index_page: bool = Field(
        default=False,
        description="Whether to emit the index table on a dedicated page when rendering documents.",
    )
