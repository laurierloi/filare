# -*- coding: utf-8 -*-

import logging
import re
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Dict, List

import filare  # for doing filare.__file__
from filare.index_table import IndexTable
from filare.models.bom import BomContent, BomRenderOptions
from filare.models.metadata import Metadata
from filare.models.notes import Notes, get_page_notes
from filare.models.options import PageOptions, get_page_options
from filare.render.templates import get_template
from filare.models.harness_quantity import HarnessQuantity


def generate_shared_bom(
    output_dir,
    shared_bom,
    use_qty_multipliers=False,
    files=None,
    multiplier_file_name=None,
):
    shared_bom_base = output_dir / "shared_bom"
    shared_bom_file = shared_bom_base.with_suffix(".tsv")
    print(f"Generating shared bom at {shared_bom_base}")

    if use_qty_multipliers:
        harnesses = HarnessQuantity(files, multiplier_file_name, output_dir=output_dir)
        harnesses.fetch_qty_multipliers_from_file()
        print(f"Using quantity multipliers: {harnesses.multipliers}")
        for bom_item in shared_bom.values():
            bom_item.scale_per_harness(harnesses.multipliers)

    bom_render = BomContent(shared_bom).get_bom_render(
        options=BomRenderOptions(
            restrict_printed_lengths=False,
            filter_entries=False,
            no_per_harness=False,
            reverse=False,
        )
    )

    shared_bom_file.open("w").write(bom_render.as_tsv())

    return shared_bom_base


# TODO: should define the dataclass needed to avoid doing any dict shuffling in here
def generate_html_output(
    filename: Path,
    bom: List[List[str]],
    metadata: Metadata,
    options: PageOptions,
    notes: Notes,
    rendered: Dict[str, str] = None,
    bom_render_options: BomRenderOptions = None,
):
    print("Generating html output")
    assert metadata and isinstance(metadata, Metadata), "metadata should be defiend"
    template_name = metadata.template.name

    if rendered is None:
        rendered = {}

    if bom_render_options is None:
        bom_render_options = BomRenderOptions(
            restrict_printed_lengths=True,
            filter_entries=True,
            no_per_harness=True,
            reverse=metadata.template.has_bom_reversed(),
        )

    bom_render = BomContent(bom).get_bom_render(options=bom_render_options)
    options.bom_rows = len(bom_render.rows)
    rendered["bom"] = bom_render.render(
        page_options=options, bom_options=bom_render_options
    )

    # TODO: instead provide a PageOption to generate or not the svg
    svgdata = None
    if template_name != "titlepage":
        # embed SVG diagram for all but the titlepage
        with filename.with_suffix(".svg").open("r") as f:
            svgdata = re.sub(
                "^<[?]xml [^?>]*[?]>[^<]*<!DOCTYPE [^>]*>",
                "<!-- XML and DOCTYPE declarations from SVG file removed -->",
                f.read(),
                1,
            )

    match = re.search(r"[0-9]+$", str(filename))
    if not match:
        harness_number = metadata.sheet_current + 1
    else:
        harness_number = int(match[0])

    partno = f"{metadata.pn}-{metadata.revision}"
    if template_name != "titlepage":
        partno += f"-{harness_number}"

    replacements = {
        "options": options,
        "diagram": svgdata,
        "metadata": metadata,
        "notes": notes,
        "partno": partno,
    }

    # TODO: all rendering should be done within their respective classes

    # prepare titleblock
    rendered["titleblock"] = get_template("titleblock.html").render(replacements)

    # preparate Notes
    if "notes" in replacements and replacements["notes"].notes:
        rendered["notes"] = get_template("notes.html").render(replacements)

    # generate page template
    page_rendered = get_template(template_name, ".html").render(
        {
            **replacements,
            **rendered,
        }
    )

    # save generated file
    filename.with_suffix(".html").open("w").write(page_rendered)


def generate_titlepage(yaml_data, extra_metadata, shared_bom, for_pdf=False):
    print("Generating titlepage")

    titlepage_metadata = {
        **yaml_data.get("metadata", {}),
        **extra_metadata,
        "sheet_current": 1,
        "sheet_name": "titlepage",
        "output_name": "titlepage",
    }
    titlepage_metadata["template"]["name"] = "titlepage"
    metadata = Metadata(**titlepage_metadata)
    index_table = IndexTable.from_pages_metadata(metadata)

    bom_render_options = BomRenderOptions(
        restrict_printed_lengths=False,
        filter_entries=True,
        no_per_harness=True,
        reverse=False,
    )

    # todo: index table options as a dataclass
    options = get_page_options(yaml_data, "titlepage")
    options.bom_updated_position = "top: 20mm; left: 10mm"
    options.for_pdf = for_pdf

    generate_html_output(
        extra_metadata["output_dir"] / extra_metadata["titlepage"],
        bom=shared_bom,
        metadata=metadata,
        options=options,
        notes=get_page_notes(yaml_data, "titlepage"),
        rendered={"index_table": index_table.render(options)},
        bom_render_options=bom_render_options,
    )
