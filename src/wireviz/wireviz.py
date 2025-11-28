#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

from wireviz.flows import build_harness_from_files


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

    return build_harness_from_files(
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
