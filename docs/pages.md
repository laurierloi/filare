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
