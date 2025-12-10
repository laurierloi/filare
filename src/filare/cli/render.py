"""Typer-based entrypoint for the main Filare CLI."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Sequence

import typer

import filare.filare as wv
from filare import APP_NAME, __version__
from filare.flows.index_pages import build_pdf_bundle, build_titlepage
from filare.flows.shared_bom import build_shared_bom

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
) -> None:
    if version:
        typer.echo(f"{APP_NAME} {__version__}")
        raise typer.Exit()

    files_list = sorted(files)
    components_list = sorted(components)
    resolved_output_dir = files_list[0].parent if output_dir is None else output_dir

    output_formats = {format_codes[f] for f in formats if f in format_codes}
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

    # Always generate a titlepage
    create_titlepage = True
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

    if ("html" in output_formats) and create_titlepage:
        build_titlepage(titlepage_metadata_files, extra_metadata, shared_bom)

        if "pdf" in output_formats:
            extra_metadata["titlepage"] = extra_metadata["titlepage"].with_stem(
                f"{extra_metadata['titlepage'].stem}_for_pdf"
            )
            build_titlepage(
                titlepage_metadata_files, extra_metadata, shared_bom, for_pdf=True
            )

    if "pdf" in output_formats:
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


cli = run_app
