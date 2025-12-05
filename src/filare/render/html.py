# -*- coding: utf-8 -*-

import copy
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel, ConfigDict

from filare.index_table import IndexTable
from filare.models.bom import BomContent, BomRenderOptions
from filare.models.harness_quantity import HarnessQuantity
from filare.models.metadata import Metadata
from filare.models.notes import Notes, get_page_notes
from filare.models.options import PageOptions, get_page_options
from filare.models.table_models import TablePage, TablePaginationOptions, letter_suffix
from filare.render.templates import get_template


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


class _RenderReplacements(BaseModel):
    """Container for template replacement values."""

    options: PageOptions
    diagram: Optional[str]
    metadata: Metadata
    notes: Notes
    partno: str

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def as_mapping(self) -> Dict[str, object]:
        return {
            "options": self.options,
            "diagram": self.diagram,
            "metadata": self.metadata,
            "notes": self.notes,
            "partno": self.partno,
        }


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

    options_for_render = (
        options.model_copy(deep=True)
        if hasattr(options, "model_copy")
        else copy.deepcopy(options)
    )
    rendered = {} if rendered is None else dict(rendered)

    bom_render_options = _ensure_bom_render_options(
        bom_render_options, metadata.template.has_bom_reversed()
    )
    bom_html, bom_rows, bom_pages = _render_bom_section(
        bom, bom_render_options, options_for_render
    )
    options_for_render.bom_rows = bom_rows
    options.bom_rows = bom_rows
    rendered["bom"] = bom_html
    cut_rows = rendered.get("cut_rows")
    termination_rows = rendered.get("termination_rows")
    cut_pages = (
        _chunk_rows(
            cut_rows,
            getattr(options_for_render, "cut_rows_per_page", None),
            getattr(options_for_render, "table_page_suffix_letters", True),
        )
        if getattr(options_for_render, "include_cut_diagram", False)
        else None
    )
    termination_pages = (
        _chunk_rows(
            termination_rows,
            getattr(options_for_render, "termination_rows_per_page", None),
            getattr(options_for_render, "table_page_suffix_letters", True),
        )
        if getattr(options_for_render, "include_termination_diagram", False)
        else None
    )
    if cut_pages == [] and getattr(options_for_render, "include_cut_diagram", False):
        cut_pages = [("", [])]
    if termination_pages == [] and getattr(options_for_render, "include_termination_diagram", False):
        termination_pages = [("", [])]

    is_title_page = (
        template_name == "titlepage" or getattr(metadata, "sheet_name", "") == "titlepage"
    )
    pagination_hints = {
        key: value
        for key, value in {
            "bom": [p.suffix or "" for p in bom_pages] if bom_pages else [],
            "cut": [page_suffix for page_suffix, _ in (cut_pages or [])],
            "termination": [
                page_suffix for page_suffix, _ in (termination_pages or [])
            ],
        }.items()
        if value
    }

    should_render_index = options.split_index_page or (
        is_title_page and options.show_index_table
    )
    options_for_render.show_index_table = (
        options.show_index_table and is_title_page
    )
    if should_render_index:
        rendered["index_table"] = IndexTable.from_pages_metadata(
            metadata.pages_metadata,
            options_for_render,
            paginated_pages=pagination_hints,
        ).render(options_for_render)

    # TODO: instead provide a PageOption to generate or not the svg
    diagram = _load_svg_diagram(filename) if template_name != "titlepage" else None
    harness_number = _derive_harness_number(filename, metadata.sheet_current)
    partno = _build_part_number(
        metadata.pn, getattr(metadata, "revision", ""), harness_number, template_name
    )

    replacements = _RenderReplacements(
        options=options_for_render,
        diagram=diagram,
        metadata=metadata,
        notes=notes,
        partno=partno,
    ).as_mapping()

    # TODO: all rendering should be done within their respective classes

    # prepare titleblock
    rendered["titleblock"] = get_template("titleblock.html").render(replacements)

    if replacements.get("notes") and replacements["notes"].notes:
        rendered["notes"] = get_template("notes.html").render(replacements)

    filtered = _filtered_sections(options_for_render, rendered)

    # generate page template
    page_rendered = get_template(template_name, ".html").render(
        {
            **replacements,
            **filtered,
        }
    )

    # save generated file
    filename.with_suffix(".html").open("w").write(page_rendered)
    _write_split_sections(
        filename, metadata, options, rendered, bom_pages=bom_pages
    )
    _write_aux_pages(
        filename,
        metadata,
        options,
        rendered,
        cut_rows=cut_rows,
        termination_rows=termination_rows,
        cut_pages=cut_pages,
        termination_pages=termination_pages,
    )


def _ensure_bom_render_options(
    bom_render_options: Optional[BomRenderOptions], reverse_bom: bool
) -> BomRenderOptions:
    """Provide default BOM render options when none are supplied."""
    if bom_render_options is not None:
        return bom_render_options
    return BomRenderOptions(
        restrict_printed_lengths=True,
        filter_entries=True,
        no_per_harness=True,
        reverse=reverse_bom,
    )


def _render_bom_section(
    bom: List[List[str]],
    bom_render_options: BomRenderOptions,
    options: PageOptions,
) -> Tuple[str, int, List]:
    """Render BOM HTML snippet and return HTML plus row count and paginated pages."""
    bom_render = BomContent(bom).get_bom_render(options=bom_render_options)
    bom_rows = len(bom_render.rows)
    pagination = TablePaginationOptions(
        rows_per_page=options.bom_rows_per_page,
        force_single_page=options.bom_force_single_page,
        use_letter_suffix=options.table_page_suffix_letters,
    )
    bom_pages = []
    if options.split_bom_page and pagination.enabled:
        bom_pages = bom_render.paginate(
            pagination, page_options=options, bom_options=bom_render_options
        )
        if not bom_pages:
            bom_html = bom_render.render(page_options=options, bom_options=bom_render_options)
            bom_pages = [TablePage(index=0, suffix="", rows=[], html=bom_html)]
        else:
            bom_html = bom_pages[0].html
    else:
        bom_html = bom_render.render(page_options=options, bom_options=bom_render_options)
    return (bom_html, bom_rows, bom_pages)


def _derive_harness_number(filename: Path, sheet_current: int) -> int:
    """Extract harness number from filename, falling back to sheet index."""
    match = re.search(r"[0-9]+$", str(filename))
    if not match:
        return sheet_current + 1
    return int(match[0])


def _build_part_number(pn: str, revision: str, harness_number: int, template_name: str) -> str:
    """Compose part number string used on rendered pages."""
    base = pn if not revision else f"{pn}-{revision}"
    if template_name != "titlepage":
        suffix = harness_number
        return f"{base}-{suffix}" if base else f"{pn}-{suffix}"
    return base


def _load_svg_diagram(filename: Path) -> str:
    """Load and sanitize the SVG diagram content for embedding."""
    with filename.with_suffix(".svg").open("r") as f:
        return re.sub(
            "^<[?]xml [^?>]*[?]>[^<]*<!DOCTYPE [^>]*>",
            "<!-- XML and DOCTYPE declarations from SVG file removed -->",
            f.read(),
            1,
        )


def _filtered_sections(options: PageOptions, rendered: Dict[str, str]) -> Dict[str, str]:
    """Hide sections when split pages are requested while preserving source content."""
    filtered = dict(rendered)
    if options.split_bom_page:
        options.show_bom = False
        filtered["bom"] = ""
    if options.split_notes_page:
        options.show_notes = False
        filtered["notes"] = ""
    if options.split_index_page:
        options.show_index_table = False
        filtered["index_table"] = ""
    return filtered


def _write_split_sections(
    filename: Path,
    metadata: Metadata,
    options: PageOptions,
    rendered: Dict[str, str],
    bom_pages: Optional[List] = None,
) -> None:
    """Emit split section HTML files based on options."""
    splits = {
        "bom": options.split_bom_page and "bom" in rendered,
        "notes": options.split_notes_page and "notes" in rendered,
        "index": options.split_index_page and "index_table" in rendered,
    }
    for section, should_write in splits.items():
        if not should_write:
            continue
        if section == "bom" and bom_pages:
            for idx, page in enumerate(bom_pages):
                if not page.html:
                    continue
                suffix = page.suffix or letter_suffix(idx)
                has_letters = len(bom_pages) > 1
                target = (
                    filename.with_suffix(f".bom.{suffix}.html")
                    if has_letters and suffix
                    else filename.with_suffix(".bom.html")
                )
                title_bits = [
                    getattr(metadata, "title", ""),
                    f"{section}.{suffix or ''}" if has_letters else section,
                ]
                title = " - ".join([t for t in title_bits if t])
                wrapped = _wrap_section_html(title or section, page.html)
                target.write_text(wrapped, encoding="utf-8")
                logging.info("Wrote paginated %s page to %s", section, target)
                if has_letters and idx == 0:
                    legacy_target = filename.with_suffix(".bom.html")
                    if legacy_target != target:
                        legacy_target.write_text(wrapped, encoding="utf-8")
                        logging.info(
                            "Wrote legacy first paginated %s page to %s",
                            section,
                            legacy_target,
                        )
            continue

        content = rendered.get(section if section != "index" else "index_table")
        if not content:
            continue
        title_bits = [getattr(metadata, "title", ""), section]
        title = " - ".join([t for t in title_bits if t])
        page = _wrap_section_html(title or section, content)
        target = filename.with_suffix(f".{section}.html")
        target.write_text(page, encoding="utf-8")
        logging.info("Wrote split %s page to %s", section, target)


def _wrap_section_html(title: str, body: str) -> str:
    return (
        "<!doctype html>\n"
        "<html>\n"
        "<head>\n"
        '<meta charset="utf-8">\n'
        f"<title>{title}</title>\n"
        "</head>\n"
        "<body>\n"
        f"{body}\n"
        "</body>\n"
        "</html>\n"
    )


def _chunk_rows(
    rows: Optional[List[Dict[str, str]]],
    rows_per_page: Optional[int],
    use_letters: bool,
) -> List[Tuple[str, List[Dict[str, str]]]]:
    """Split a list of row dicts into paginated chunks with optional letter suffixes."""
    if not rows:
        return []
    if not rows_per_page:
        return [("", rows)]
    per_page = int(rows_per_page)
    chunks: List[List[Dict[str, str]]] = [
        rows[i : i + per_page] for i in range(0, len(rows), per_page)
    ]
    suffixes: List[str] = (
        [letter_suffix(idx) for idx in range(len(chunks))]
        if use_letters and len(chunks) > 1
        else ["" for _ in chunks]
    )
    return list(zip(suffixes, chunks))


def _write_aux_pages(
    filename: Path,
    metadata: Metadata,
    options: PageOptions,
    rendered: Dict[str, str],
    cut_rows: Optional[List[Dict[str, str]]] = None,
    termination_rows: Optional[List[Dict[str, str]]] = None,
    cut_pages: Optional[List[Tuple[str, List[Dict[str, str]]]]] = None,
    termination_pages: Optional[List[Tuple[str, List[Dict[str, str]]]]] = None,
) -> None:
    """Emit auxiliary pages such as cut/termination placeholders when requested."""
    aux_pages = []
    if getattr(options, "include_cut_diagram", False):
        pages = cut_pages
        if pages is None:
            pages = _chunk_rows(
                cut_rows,
                getattr(options, "cut_rows_per_page", None),
                getattr(options, "table_page_suffix_letters", True),
            )
        aux_pages.append(
            (
                "cut",
                get_template("cut", ".html"),
                get_template("cut_table", ".html"),
                rendered.get("cut_table", ""),
                pages,
            )
        )
    if getattr(options, "include_termination_diagram", False):
        pages = termination_pages
        if pages is None:
            pages = _chunk_rows(
                termination_rows,
                getattr(options, "termination_rows_per_page", None),
                getattr(options, "table_page_suffix_letters", True),
            )
        aux_pages.append(
            (
                "termination",
                get_template("termination", ".html"),
                get_template("termination_table", ".html"),
                rendered.get("termination_table", ""),
                pages,
            )
        )
    for suffix, template, table_template, default_html, pages in aux_pages:
        if not pages:
            pages = [("", [])]
        total_pages = len(pages)
        for idx, (page_suffix, rows) in enumerate(pages):
            table_html = (
                table_template.render({"rows": rows}) if rows else default_html
            )
            suffix_for_file = (
                f".{page_suffix or letter_suffix(idx)}" if total_pages > 1 else ""
            )
            target = filename.with_suffix(f".{suffix}{suffix_for_file}.html")
            sheet_suffix = (
                page_suffix if (total_pages > 1 and page_suffix is not None) else ""
            )
            page_metadata = (
                metadata.model_copy(update={"sheet_suffix": sheet_suffix})
                if hasattr(metadata, "model_copy")
                else metadata
            )
            page_partno = _build_part_number(
                getattr(page_metadata, "pn", ""),
                getattr(page_metadata, "revision", ""),
                getattr(page_metadata, "sheet_current", 0),
                getattr(getattr(page_metadata, "template", None), "name", ""),
            )
            page_titleblock = get_template("titleblock.html").render(
                {
                    "metadata": page_metadata,
                    "options": options,
                    "partno": page_partno,
                }
            )
            page = template.render(
                {
                    f"{suffix}_table": table_html,
                    "metadata": page_metadata,
                    "options": options,
                    "titleblock": page_titleblock,
                    "notes": rendered.get("notes", ""),
                    "bom": rendered.get("bom", ""),
                    "diagram": rendered.get("diagram", ""),
                }
            )
            target.write_text(page, encoding="utf-8")


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
