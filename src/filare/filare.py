#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

from enum import Enum

from filare.flows import build_harness_from_files
from filare.models.document import DocumentRepresentation


def parse(
    inp: List[Path],
    metadata_files: List[Path],
    return_types: Union[None, str, Tuple[str]] = None,
    output_formats: Union[None, str, Tuple[str]] = None,
    output_dir: Path = None,
    extra_metadata: Dict = {},
    shared_bom: Dict = {},
    output_name_override: str = None,
    connector_view: str = "detailed",
    metadata_output_name: str = None,
    update_shared_bom: bool = True,
) -> Any:
    """
    Wrapper to build and optionally render a Harness from YAML inputs.
    """

    harness = build_harness_from_files(
        inp=inp,
        metadata_files=metadata_files,
        return_types=return_types,
        output_formats=output_formats,
        output_dir=output_dir,
        extra_metadata=extra_metadata,
        shared_bom=shared_bom,
        output_name_override=output_name_override,
        connector_view=connector_view,
        metadata_output_name=metadata_output_name,
        update_shared_bom=update_shared_bom,
    )

    if return_types and ("document" in return_types or "doc" in return_types):
        # Build a lightweight document representation for callers that want pre-render data.
        return _build_document_representation(harness)

    return harness


def _build_document_representation(harness) -> DocumentRepresentation:
    """Build a document representation from a harness for pre-render use."""
    metadata_dict = {}
    if hasattr(harness, "metadata"):
        if hasattr(harness.metadata, "model_dump"):
            metadata_dict = harness.metadata.model_dump(mode="json")
        elif hasattr(harness.metadata, "dict"):
            metadata_dict = harness.metadata.dict()
        metadata_dict = _make_jsonable(metadata_dict)
    notes_text = str(harness.notes) if getattr(harness, "notes", None) else None
    options_dict = {}
    if hasattr(harness, "options"):
        if hasattr(harness.options, "model_dump"):
            options_dict = harness.options.model_dump(mode="json")
        elif hasattr(harness.options, "dict"):
            options_dict = harness.options.dict()
        options_dict = _make_jsonable(options_dict)
    pages = [
        {
            "type": "harness",
            "name": getattr(getattr(harness, "metadata", None), "name", ""),
            "formats": options_dict.get("formats", []),
        }
    ]
    bom_data = {} if not getattr(harness.options, "include_bom", True) else {}
    return DocumentRepresentation(
        metadata=metadata_dict,
        pages=pages,
        notes=notes_text,
        bom=bom_data,
        extras={"options": options_dict},
    )


def _make_jsonable(value):
    """Coerce values to JSON/YAML-safe types."""
    if isinstance(value, dict):
        return {k: _make_jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_make_jsonable(v) for v in value]
    if isinstance(value, (Path,)):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    return value
