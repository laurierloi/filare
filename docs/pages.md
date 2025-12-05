# Document Pages

Filare assembles engineering documents as a set of page types. Each page carries its own purpose and data; the document representation (`*.document.yaml`) lists the pages to render.

## Page types

- **title**: Title page/front matter. Carries project metadata (part number, revision, company, authors, etc.).
- **harness**: The primary harness diagram page (GraphViz-rendered connector/cable graph embedded in HTML/PDF).
- **bom**: Bill of Materials page. Tabular listing of parts, quantities, and per-harness data. By default included and rendered to TSV/HTML.
- **cut**: Wire cut table/diagram. Intended to list wire IDs, gauges, lengths, and colors. Optional; disabled by default.
- **termination**: Termination table/diagram. Intended to list per-wire ends, splices/crimps, connector pins, and lengths. Optional; disabled by default.

## Defaults

- The default document includes: `title`, `harness`, and `bom` pages.
- `cut` and `termination` pages are opt-in; enable via `options.include_cut_diagram` / `options.include_termination_diagram`.
- BOM inclusion can be turned off with `options.include_bom`.
- The index table is generated only on the title page. When split output is requested, the title page excludes the index content and writes `titlepage.index.html` instead.

## Pagination and split tables

- Set `options.split_bom_page: true` and `options.bom_rows_per_page` to paginate the BOM into multiple HTML pages. The first page writes to `<harness>.bom.html`; subsequent pages use lettered suffixes (`<harness>.bom.b.html`, `<harness>.bom.c.html`, …). `options.bom_force_single_page` keeps everything on one page even if `bom_rows_per_page` is set.
- Cut and termination tables also paginate when `cut_rows_per_page` / `termination_rows_per_page` are set alongside their respective `include_*_diagram` toggles. Additional pages use the same lettered suffix scheme.
- When pagination is active and `options.table_page_suffix_letters` is true (default), the index table lists lettered page names (e.g., `h.bom.a`, `h.cut.b`) and cut/termination title blocks display the letter suffix next to the sheet number.

## Data provided

- **Title**: Metadata (PN, revision, company, address, authors, revisions, git status).
- **Harness**: Connector/cable graph, notes, title block, embedded images.
- **BOM**: Part numbers, quantities, per-harness quantities, designators, optional distributor fields; TSV + HTML render.
- **Cut**: Wire IDs, gauges, lengths, colors (planned); useful for shop-floor cutting.
- **Termination**: Wire ends with connector/pin, splices/crimps, lengths, notes (planned); useful for assembly steps.

## Document representation

`*.document.yaml` lists pages with their types and names. Example snippet:

```yaml
pages:
  - type: title
    name: titlepage
  - type: harness
    name: MAIN
    formats: [svg]
  - type: bom
    name: bom
  - type: cut
    name: cut
  - type: termination
    name: term
```

User edits to the document YAML are preserved (hash-guarded). Delete `*.document.yaml` and `document_hashes.yaml` to regenerate from the harness if needed.

### Minimal cut/termination example

Enable optional cut/termination pages via harness options:

```yaml
metadata:
  title: Example with cut/termination
options:
  include_cut_diagram: true
  include_termination_diagram: true
connectors:
  X1:
    type: D-Sub
    pincount: 3
  X2:
    type: D-Sub
    pincount: 3
cables:
  W1:
    wirecount: 3
connections:
  - - X1: [1-3]
    - W1: [1-3]
    - X2: [1-3]
```

Run `uv run filare example.yml -o outputs` to emit `example.document.yaml` and page stubs for cut/termination alongside the regular title/harness/BOM. The cut/termination tables are currently minimal; use them to list lengths, colors, and pin ends until richer layouts arrive.

### Using an existing document representation

If a `*.document.yaml` already exists for the harness (same stem as the harness file, located in the output directory), Filare will load it and drive generation from it:

- Options in `extras.options` are applied before rendering (e.g., `include_cut_diagram`, `include_termination_diagram`, `split_bom_page`, `split_notes_page`, `split_index_page`).
- Page entries define which pages render; BOM/TSV output is skipped when the document omits a BOM page.
- Document-requested formats on each page are merged with CLI formats.
- Locked documents (`document_hashes.yaml` with `allow_override: false`) are respected and not overwritten.

### Quick demo

1. Copy `examples/demo01.document.yaml` alongside the demo harness outputs (e.g., `cp examples/demo01.document.yaml outputs/`).
2. Run `uv run filare examples/demo01.yml -f hpst -o outputs` to build SVG/PNG/TSV and the document YAML; split pages and index links follow the document.
3. Edit `outputs/demo01.document.yaml` and rerun to see document-driven rendering; locked files (via `document_hashes.yaml`) are left untouched.
