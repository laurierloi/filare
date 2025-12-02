# Metadata Development Guide

## Role of metadata

- Defines document-level information (title, PN, company/address).
- Controls template selection and sheet info (sheet_total/current/name, output_names, titlepage).
- Feeds titleblock and titlepage rendering; parts of metadata propagate into file names (`pn-output_name`).
- Authors/revisions are rendered in titleblocks; template config (sheetsize/orientation) affects layout direction and BOM ordering.

## Adding a new metadata field

1. Update `src/filare/models/metadata.py` to include the field in the `Metadata` dataclass (and any supporting enums/structures).
2. If the field is user-facing in HTML, add it to the appropriate template:
   - Titleblock: `src/filare/templates/titleblock.html`
   - Titlepage: `src/filare/templates/titlepage.html`
   - BOM/index table if relevant: `src/filare/templates/bom.html` or `src/filare/templates/index_table.html`
3. Wire the field into the rendering context if not already propagated:
   - `render/output.py` prepares `metadata` for template rendering; ensure the new field is accessible (usually automatic via `Metadata`).
4. Add or update documentation describing the field (e.g., docs/README.md metadata section).
5. Add tests:
   - Unit test in `tests/models` for `Metadata` to ensure parsing and defaults.
   - Rendering test in `tests/render` if the field appears in output (assert substring in generated HTML).

## Where metadata is rendered

- Titleblock (`templates/titleblock.html`): company, address, pn, revision, authors, sheet info.
- Titlepage (`templates/titlepage.html`): project/title info, index table, shared BOM summary.
- File naming: `Metadata.name` combines `pn` and `output_name` to form output file stems.

## Other development guide topics (to create)

- Adding a new component or connector attribute and surfacing it in Graphviz/HTML.
- Extending parser to support new YAML schema keys (with validation).
- Adding a new output format (e.g., CSV) to flows/render and CLI.
- Improving quantity multiplier handling (fil_harness_quantity) with tests.
