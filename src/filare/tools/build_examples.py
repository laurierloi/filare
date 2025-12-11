#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import re
import sys
from pathlib import Path

import typer
import yaml

script_path = Path(__file__).absolute()
sys.path.insert(0, str(script_path.parent.parent.parent))  # to find filare module

import filare.cli as filare_cli
from filare import APP_NAME, __version__

cli = filare_cli.cli

base_dir = script_path.parent.parent.parent.parent
readme = "readme.md"
groups = {
    "examples": {
        "path": base_dir / "examples",
        "prefix": "ex",
        readme: [],  # Include no files
        "title": "Example Gallery",
    },
    "tutorial": {
        "path": base_dir / "tutorial",
        "prefix": "tutorial",
        readme: ["md", "yml"],  # Include .md and .yml files
        "title": f"{APP_NAME} Tutorial",
    },
    "demos": {
        "path": base_dir / "examples",
        "prefix": "demo",
    },
    "multi-page": {
        "path": base_dir / "examples" / "multi-page",
        "prefix": "ex",
        readme: [],  # Include no files
        "title": "Multi-page Examples",
    },
}

input_extensions = [".yml"]
extensions_not_containing_graphviz_output = [".gv", ".bom.tsv"]
extensions_containing_graphviz_output = [".png", ".svg", ".html", ".pdf"]
generated_extensions = (
    extensions_not_containing_graphviz_output + extensions_containing_graphviz_output
)


def collect_filenames(description, groupkey, ext_list):
    """Collect a sorted list of files in a group folder.

    Args:
        description: Human-friendly prefix for log output.
        groupkey: Key in `groups` indicating which collection to read.
        ext_list: List of extensions/globs to include (e.g., [".yml"]).

    Returns:
        A sorted list of matching Path objects.
    """
    path = groups[groupkey]["path"]
    patterns = [f"{groups[groupkey]['prefix']}*{ext}" for ext in ext_list]
    if ext_list != input_extensions and readme in groups[groupkey]:
        patterns.append(readme)
    print(f'{description} {groupkey} from "{path}"')
    return sorted([filename for pattern in patterns for filename in path.glob(pattern)])


def build_generated(groupkeys, output_base=None):
    """Build examples/tutorials for the provided group keys via the CLI.

    Args:
        groupkeys: Iterable of keys from `groups` to process.
        output_base: Optional root directory to place generated artifacts.

    Returns:
        None. Outputs rendered assets and document manifests to disk.
    """
    output_base = Path(output_base) if output_base else None
    all_dest_paths = []
    for key in groupkeys:
        # preparation
        src_path = groups[key]["path"]
        dest_path = src_path if output_base is None else output_base / key
        dest_path.mkdir(parents=True, exist_ok=True)
        all_dest_paths.append(dest_path)
        build_readme = readme in groups[key]
        if build_readme:
            include_readme = "md" in groups[key][readme]
            include_source = "yml" in groups[key][readme]
            with (dest_path / readme).open("w") as out:
                out.write(f'# {groups[key]["title"]}\n\n')
        # collect and iterate input YAML files
        yaml_files = [f for f in collect_filenames("Building", key, input_extensions)]
        try:
            cli(
                [
                    "run",
                    "--formats",
                    "ghpstb",  # no pdf for now
                    "--metadata",
                    str(yaml_files[0].parent / "metadata.yml"),
                    "--output-dir",
                    str(dest_path),
                    *[str(f) for f in yaml_files],
                ]
            )
        except BaseException as e:
            if str(e) != "0" and not isinstance(e, (typer.Exit, SystemExit)):
                raise

        if build_readme:
            for yaml_file in yaml_files:
                i = "".join(filter(str.isdigit, yaml_file.stem))

                with (dest_path / readme).open("a") as out:
                    if include_readme:
                        with yaml_file.with_suffix(".md").open("r") as info:
                            for line in info:
                                out.write(line.replace("## ", f"## {i} - "))
                            out.write("\n\n")
                    else:
                        out.write(f"## Example {i}\n")

                    if include_source:
                        with yaml_file.open("r") as src:
                            out.write("```yaml\n")
                            for line in src:
                                out.write(line)
                            out.write("```\n")
                        out.write("\n")

                    out.write(f"![]({yaml_file.stem}.png)\n\n")
                    out.write(
                        f"[Source]({yaml_file.name}) - [Bill of Materials]({yaml_file.stem}.tsv)\n\n\n"
                    )

    # Write a manifest of all document representations for each destination
    for dest in all_dest_paths:
        _write_document_manifest(dest)
    verify_bom_tables(all_dest_paths)


def clean_generated(groupkeys):
    """Remove generated artifacts for the provided groups.

    Args:
        groupkeys: Iterable of keys from `groups` indicating which outputs to clean.

    Returns:
        None. Deletes rendered assets and document manifests for a clean rebuild.
    """
    for key in groupkeys:
        # collect and remove files
        for filename in collect_filenames("Cleaning", key, generated_extensions):
            if filename.is_file():
                print(f'  rm "{filename}"')
                filename.unlink()

        manifest = groups[key]["path"] / "document_manifest.yaml"
        if manifest.exists():
            manifest.unlink()


def _bom_rows_in_html(html_path: Path) -> int:
    """Count BOM table rows inside an HTML file; returns -1 when no BOM exists."""
    try:
        content = html_path.read_text(encoding="utf-8")
    except Exception:
        return -1
    match = re.search(
        r"<div\\s+id=\"bom\"[^>]*>(?P<body>.*?)</div>",
        content,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return -1
    body = match.group("body")
    return len(re.findall(r"<tr", body, re.IGNORECASE))


def verify_bom_tables(output_dirs):
    """Ensure every rendered BOM HTML contains data rows."""
    failures = []
    for dest in output_dirs:
        for html in Path(dest).rglob("*.html"):
            rows = _bom_rows_in_html(html)
            if rows == -1:
                continue
            if rows <= 1:
                failures.append((html, rows))
    if failures:
        lines = "\n".join(f" - {path} (rows={rows})" for path, rows in failures)
        raise SystemExit(
            "BOM sanity check failed: header-only BOM tables found:\n" + lines
        )


def _write_document_manifest(output_dir: Path) -> None:
    """Collect all document representations and emit a manifest."""
    from filare.models.document import DocumentManifest, DocumentManifestEntry

    docs = []
    title_metadata = {}
    split_bom = False
    split_notes = False
    split_index = False
    for doc_file in sorted(output_dir.rglob("*.document.yaml")):
        rel = doc_file.relative_to(output_dir)
        docs.append(DocumentManifestEntry(path=str(rel), name=doc_file.stem))
        try:
            data = yaml.safe_load(doc_file.read_text(encoding="utf-8")) or {}
            if not title_metadata:
                title_metadata = data.get("metadata", {})
            opts = (data.get("extras") or {}).get("options", {})
            split_bom = split_bom or bool(opts.get("split_bom_page"))
            split_notes = split_notes or bool(opts.get("split_notes_page"))
            split_index = split_index or bool(opts.get("split_index_page"))
            logging.debug("Loaded document metadata from %s", doc_file)
        except Exception as exc:
            logging.warning(
                "Skipping document metadata from %s due to parse error; "
                "manifest may be incomplete. Fix the document YAML to include metadata/extras. error=%s",
                doc_file,
                exc,
            )
            if not title_metadata:
                title_metadata = {}

    # attempt to locate shared BOM under this output dir
    shared_bom = None
    for candidate in output_dir.rglob("shared_bom*.tsv"):
        shared_bom = str(candidate.relative_to(output_dir))
        logging.debug("Using shared BOM at %s", shared_bom)
        break

    manifest = DocumentManifest(
        documents=docs,
        title_metadata=title_metadata,
        shared_bom=shared_bom,
        split_combined_bom=split_bom,
        split_notes=split_notes,
        split_index=split_index,
    )
    manifest_path = output_dir / "document_manifest.yaml"
    manifest_path.write_text(
        yaml.safe_dump(manifest.model_dump(mode="json"), sort_keys=True),
        encoding="utf-8",
    )
    print(f"Wrote document manifest to {manifest_path}")


def parse_args():
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} Example Manager",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s - {APP_NAME} {__version__}",
    )
    parser.add_argument(
        "action",
        nargs="?",
        action="store",
        choices=["build", "clean", "compare", "diff", "restore"],
        default="build",
        help="what to do with the generated files (default: build)",
    )
    parser.add_argument(
        "-g",
        "--groups",
        nargs="+",
        choices=groups.keys(),
        default=groups.keys(),
        help="the groups of generated files (default: all)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=None,
        type=Path,
        help="Optional base directory for generated outputs (defaults to in-place).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.action == "build":
        build_generated(args.groups, output_base=args.output_dir)
    elif args.action == "clean":
        clean_generated(args.groups)


if __name__ == "__main__":
    main()
