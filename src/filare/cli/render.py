"""Typer-based entrypoint for the main Filare CLI."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Sequence, Set

import typer
import yaml

import filare.filare as wv
from filare import APP_NAME, __version__
from filare.flows.index_pages import build_pdf_bundle, build_titlepage
from filare.flows.shared_bom import build_shared_bom
from filare.models.document import DocumentRepresentation
from filare.models.page import PageBase, PageType
from filare.render.templates import get_template

format_codes = {
    "c": "csv",
    "g": "gv",
    "h": "html",
    "p": "png",
    "P": "pdf",
    "s": "svg",
    "t": "tsv",
    "b": "shared_bom",
}
format_name_to_code = {v: k for k, v in format_codes.items()}


def _codes_from_formats(formats: Sequence[str]) -> str:
    """Convert format names/codes into a compact codes string."""
    codes: List[str] = []
    for fmt in formats:
        if len(fmt) == 1 and fmt in format_codes:
            codes.append(fmt)
        else:
            code = format_name_to_code.get(fmt)
            if code:
                codes.append(code)
    return "".join(codes)


epilog = (
    "The -f or --formats option accepts a string containing one or more of the "
    "following characters to specify which file types to output:\n"
    + f", ".join([f"{key} ({value.upper()})" for key, value in format_codes.items()])
)

run_app = typer.Typer(
    add_completion=True,
    no_args_is_help=True,
    context_settings={
        "help_option_names": ["-h", "--help"],
        "allow_interspersed_args": True,
    },
    epilog=epilog,
    help="Parses the provided harness files and generates the requested outputs.",
)

harness_app = typer.Typer(
    add_completion=True,
    no_args_is_help=True,
    context_settings={
        "help_option_names": ["-h", "--help"],
        "allow_interspersed_args": True,
    },
    help="Render harness-only outputs without title pages or PDF bundles.",
)

document_app = typer.Typer(
    add_completion=True,
    no_args_is_help=True,
    invoke_without_command=True,
    context_settings={
        "help_option_names": ["-h", "--help"],
        "allow_interspersed_args": True,
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
    help="Render full documents including title page and optional PDF bundle.",
)

page_app = typer.Typer(
    add_completion=True,
    no_args_is_help=True,
    context_settings={
        "help_option_names": ["-h", "--help"],
        "allow_interspersed_args": True,
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
    help="Render a single harness page without document bundling.",
)


@page_app.callback()
def page_callback(ctx: typer.Context) -> None:
    """Store page config for subcommands (parsed manually)."""
    page_config: Optional[Path] = None
    args = list(ctx.args)
    for idx, arg in enumerate(args):
        if arg in ("--page-config", "-C") and idx + 1 < len(args):
            page_config = Path(args[idx + 1])
            break
    ctx.obj = ctx.obj or {}
    ctx.obj["page_config"] = page_config


@document_app.callback()
def document_callback(ctx: typer.Context) -> None:
    """Store document config for subcommands (parsed manually to allow extra args)."""
    ctx.obj = ctx.obj or {}
    document_config: Optional[Path] = ctx.obj.get("document_config")
    args = list(ctx.args)
    for idx, arg in enumerate(args):
        if arg in ("--document-config", "-D") and idx + 1 < len(args):
            document_config = Path(args[idx + 1])
            break
    ctx.obj["document_config"] = document_config


def _render_cli(
    files: Sequence[Path],
    formats: str,
    components: Sequence[Path],
    metadata: Sequence[Path],
    output_dir: Optional[Path],
    output_name: Optional[str],
    version: bool,
    use_qty_multipliers: bool,
    multiplier_file_name: str,
    *,
    create_titlepage: bool = True,
    allowed_format_codes: Optional[set[str]] = None,
    single_page: bool = False,
) -> None:
    if version:
        typer.echo(f"{APP_NAME} {__version__}")
        raise typer.Exit()

    files_list = sorted(files)
    components_list = sorted(components)
    resolved_output_dir = files_list[0].parent if output_dir is None else output_dir

    selected_codes = set(formats)
    if allowed_format_codes is not None:
        selected_codes &= allowed_format_codes
    output_formats = {format_codes[f] for f in selected_codes if f in format_codes}
    harness_output_formats = output_formats.copy()
    shared_bom = {}
    titlepage_metadata_files = tuple(metadata) if metadata else tuple(files_list)

    extra_metadata = {
        "output_dir": resolved_output_dir,
        "files": files_list,
        "output_names": [_file.stem for _file in files_list],
        "sheet_total": len(files_list),
        "sheet_current": 1,
        "use_qty_multipliers": use_qty_multipliers,
        "multiplier_file_name": multiplier_file_name,
    }

    if create_titlepage and not single_page:
        extra_metadata["titlepage"] = Path("titlepage")
        extra_metadata["output_names"].insert(0, "titlepage")
        extra_metadata["sheet_current"] += 1
        extra_metadata["sheet_total"] += 1

    if "pdf" in harness_output_formats:
        harness_output_formats.remove("pdf")

    for harness_file in files_list:
        effective_output_name = output_name or harness_file.stem

        typer.echo(f"Input file:   {harness_file}")
        typer.echo(
            "Output file:  "
            f"{resolved_output_dir / effective_output_name}.[{'|'.join(output_formats)}]"
        )

        extra_metadata["sheet_name"] = effective_output_name.upper()

        ret = wv.parse(
            tuple(components_list) + (harness_file,),
            metadata_files=tuple(metadata),
            return_types=("shared_bom"),
            output_formats=list(harness_output_formats),
            output_dir=resolved_output_dir,
            extra_metadata=extra_metadata,
            shared_bom=shared_bom,
            output_name_override=output_name,
            metadata_output_name=effective_output_name,
        )
        shared_bom = ret["shared_bom"]
        extra_metadata["sheet_current"] += 1

    shared_bom_base = None
    if "shared_bom" in output_formats:
        shared_bom_base = build_shared_bom(
            output_dir=resolved_output_dir,
            shared_bom=shared_bom,
            use_qty_multipliers=use_qty_multipliers,
            files=tuple(files_list),
            multiplier_file_name=multiplier_file_name,
        )

    if ("html" in output_formats) and create_titlepage and not single_page:
        build_titlepage(titlepage_metadata_files, extra_metadata, shared_bom)

        if "pdf" in output_formats:
            extra_metadata["titlepage"] = extra_metadata["titlepage"].with_stem(
                f"{extra_metadata['titlepage'].stem}_for_pdf"
            )
            build_titlepage(
                titlepage_metadata_files, extra_metadata, shared_bom, for_pdf=True
            )

    if "pdf" in output_formats and not single_page:
        build_pdf_bundle(
            [resolved_output_dir / p for p in extra_metadata["output_names"]]
        )

    typer.echo()  # blank line after execution


def render_callback(
    *,
    files: Sequence[Path],
    formats: str = "hpst",
    components: Sequence[Path] = (),
    metadata: Sequence[Path] = (),
    output_dir: Optional[Path] = None,
    output_name: Optional[str] = None,
    version: bool = False,
    use_qty_multipliers: bool = False,
    multiplier_file_name: str = "quantity_multipliers.txt",
    create_titlepage: bool = True,
    allowed_format_codes: Optional[set[str]] = None,
) -> None:
    """Direct entrypoint used by tests and internal tooling."""
    _render_cli(
        files=files,
        formats=formats,
        components=components,
        metadata=metadata,
        output_dir=output_dir,
        output_name=output_name,
        version=version,
        use_qty_multipliers=use_qty_multipliers,
        multiplier_file_name=multiplier_file_name,
        create_titlepage=create_titlepage,
        allowed_format_codes=allowed_format_codes,
    )


@run_app.callback(invoke_without_command=True)
def run(
    files: List[Path] = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="YAML harness files to process.",
    ),
    formats: str = typer.Option(
        "hpst",
        "-f",
        "--formats",
        show_default=True,
        help="Output formats (see below).",
    ),
    components: List[Path] = typer.Option(
        [],
        "-c",
        "--components",
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
        help="YAML file containing component templates prepended to each harness (optional).",
    ),
    metadata: List[Path] = typer.Option(
        [],
        "-d",
        "--metadata",
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
        help="YAML file containing metadata/options merged into each harness (optional).",
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output-dir",
        exists=True,
        readable=True,
        file_okay=False,
        dir_okay=True,
        help="Directory to use for output files, if different from input file directory.",
    ),
    output_name: Optional[str] = typer.Option(
        None,
        "-O",
        "--output-name",
        help="File name (without extension) to use for output files, if different from input file name.",
    ),
    version: bool = typer.Option(
        False,
        "-V",
        "--version",
        help=f"Output {APP_NAME} version and exit.",
    ),
    use_qty_multipliers: bool = typer.Option(
        False,
        "-u",
        "--use-qty-multipliers",
        help="If set, the shared BOM counts will be scaled with the qty-multipliers.",
    ),
    multiplier_file_name: str = typer.Option(
        "quantity_multipliers.txt",
        "-m",
        "--multiplier-file-name",
        help="Name of file used to fetch the qty_multipliers.",
    ),
) -> None:
    """Parse provided harness files and generate the specified outputs."""
    _render_cli(
        files=files,
        formats=formats,
        components=components,
        metadata=metadata,
        output_dir=output_dir,
        output_name=output_name,
        version=version,
        use_qty_multipliers=use_qty_multipliers,
        multiplier_file_name=multiplier_file_name,
    )


@harness_app.command("render", context_settings={"allow_interspersed_args": True})
def harness_render(
    files: List[Path] = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="YAML harness files to process.",
    ),
    formats: str = typer.Option(
        "hpst",
        "-f",
        "--formats",
        show_default=True,
        help="Output formats (subset of harness outputs: c,g,h,p,s,t,b).",
    ),
    components: List[Path] = typer.Option(
        [],
        "-c",
        "--components",
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
        help="YAML file containing component templates prepended to each harness (optional).",
    ),
    metadata: List[Path] = typer.Option(
        [],
        "-d",
        "--metadata",
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
        help="YAML file containing metadata/options merged into each harness (optional).",
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output-dir",
        exists=True,
        readable=True,
        file_okay=False,
        dir_okay=True,
        help="Directory to use for output files, if different from input file directory.",
    ),
    output_name: Optional[str] = typer.Option(
        None,
        "-O",
        "--output-name",
        help="File name (without extension) to use for output files, if different from input file name.",
    ),
    use_qty_multipliers: bool = typer.Option(
        False,
        "-u",
        "--use-qty-multipliers",
        help="If set, the shared BOM counts will be scaled with the qty-multipliers.",
    ),
    multiplier_file_name: str = typer.Option(
        "quantity_multipliers.txt",
        "-m",
        "--multiplier-file-name",
        help="Name of file used to fetch the qty_multipliers.",
    ),
) -> None:
    """Render harness-only outputs without title pages or PDF bundles."""
    allowed = {
        "c",
        "g",
        "h",
        "p",
        "s",
        "t",
        "b",
    }  # csv, gv, html, png, svg, tsv, shared_bom
    render_callback(
        files=files,
        formats=formats,
        components=components,
        metadata=metadata,
        output_dir=output_dir,
        output_name=output_name,
        use_qty_multipliers=use_qty_multipliers,
        multiplier_file_name=multiplier_file_name,
        create_titlepage=False,
        allowed_format_codes=allowed,
    )


@document_app.command("render", context_settings={"allow_interspersed_args": True})
def document_render(
    ctx: typer.Context,
    files: List[Path] = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="YAML harness files to process.",
    ),
    formats: str = typer.Option(
        "hpstP",
        "-f",
        "--formats",
        show_default=True,
        help="Output formats (includes titlepage/PDF bundling).",
    ),
    components: List[Path] = typer.Option(
        [],
        "-c",
        "--components",
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
        help="YAML file containing component templates prepended to each harness (optional).",
    ),
    metadata: List[Path] = typer.Option(
        [],
        "-d",
        "--metadata",
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
        help="YAML file containing metadata/options merged into each harness (optional).",
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output-dir",
        exists=True,
        readable=True,
        file_okay=False,
        dir_okay=True,
        help="Directory to use for output files, if different from input file directory.",
    ),
    output_name: Optional[str] = typer.Option(
        None,
        "-O",
        "--output-name",
        help="File name (without extension) to use for output files, if different from input file name.",
    ),
    use_qty_multipliers: bool = typer.Option(
        False,
        "-u",
        "--use-qty-multipliers",
        help="If set, the shared BOM counts will be scaled with the qty-multipliers.",
    ),
    multiplier_file_name: str = typer.Option(
        "quantity_multipliers.txt",
        "-m",
        "--multiplier-file-name",
        help="Name of file used to fetch the qty_multipliers.",
    ),
) -> None:
    """Render full documents including title page and optional PDF bundle."""
    formats_arg = formats
    create_titlepage = True
    document_config = (ctx.obj or {}).get("document_config")
    if document_config:
        doc = DocumentRepresentation.from_yaml(document_config)
        create_titlepage = any(
            getattr(page, "include", True)
            and getattr(page, "type", None) == PageType.title
            for page in doc.pages
        )
        doc_formats: List[str] = []
        for page in doc.pages:
            doc_formats.extend(getattr(page, "formats", []) or [])
        codes = _codes_from_formats(doc_formats)
        if codes:
            formats_arg = codes
    render_callback(
        files=files,
        formats=formats_arg,
        components=components,
        metadata=metadata,
        output_dir=output_dir,
        output_name=output_name,
        use_qty_multipliers=use_qty_multipliers,
        multiplier_file_name=multiplier_file_name,
        create_titlepage=create_titlepage,
    )


@page_app.command(
    "render",
    context_settings={
        "allow_interspersed_args": True,
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
)
def page_render(
    ctx: typer.Context,
    file: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="Single harness YAML file to render.",
    ),
    formats: str = typer.Option(
        "hst",
        "-f",
        "--formats",
        show_default=True,
        help="Output formats (harness page only: h,s,t).",
    ),
    components: List[Path] = typer.Option(
        [],
        "-c",
        "--components",
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
        help="YAML file containing component templates prepended to the harness (optional).",
    ),
    metadata: List[Path] = typer.Option(
        [],
        "-d",
        "--metadata",
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
        help="YAML file containing metadata/options merged into the harness (optional).",
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output-dir",
        exists=True,
        readable=True,
        file_okay=False,
        dir_okay=True,
        help="Directory to use for output files, if different from input file directory.",
    ),
    output_name: Optional[str] = typer.Option(
        None,
        "-O",
        "--output-name",
        help="File name (without extension) to use for output files, if different from input file name.",
    ),
    page_config: Optional[Path] = typer.Option(
        None,
        "--page-config",
        "-C",
        exists=True,
        readable=True,
        dir_okay=False,
        help="Optional Page model YAML (type/formats) to drive rendering.",
    ),
) -> None:
    """Render a single harness page without title page or PDF bundle."""
    page_model: Optional[PageBase] = None
    page_config = page_config or (ctx.obj or {}).get("page_config")
    if page_config:
        data = PageBase.model_validate(yaml.safe_load(Path(page_config).read_text()))
        page_model = data
        cfg_codes = _codes_from_formats(getattr(data, "formats", []) or [])
        if cfg_codes:
            formats = cfg_codes
    allowed = set(format_codes.keys()) if not page_model else set(format_codes.keys())
    if page_model and getattr(page_model, "type", None) == PageType.title:
        # Render title page only.
        resolved_output_dir = file.parent if output_dir is None else output_dir
        title_name = output_name or "titlepage"
        extra_metadata = {
            "output_dir": resolved_output_dir,
            "files": [file],
            "output_names": [title_name],
            "sheet_total": 1,
            "sheet_current": 1,
            "use_qty_multipliers": False,
            "multiplier_file_name": "quantity_multipliers.txt",
            "titlepage": Path(title_name),
        }
        build_titlepage(metadata or [file], extra_metadata, shared_bom={})
        return

    render_callback(
        files=[file],
        formats=formats,
        components=components,
        metadata=metadata,
        output_dir=output_dir,
        output_name=output_name,
        create_titlepage=False,
        allowed_format_codes=allowed,
        version=False,
        use_qty_multipliers=False,
        multiplier_file_name="quantity_multipliers.txt",
    )


cli = run_app
