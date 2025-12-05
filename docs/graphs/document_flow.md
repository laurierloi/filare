# Document Representation Flow (Mermaid)

```mermaid
flowchart TD
  subgraph Input
    Y[YAML harness files]
    M[Metadata YAML]
  end

  subgraph Build
    P1[parser.parse_concat_merge_files]
    F1[flows.build_harness]
    DR[DocumentRepresentation]
    DH[document_hashes.yaml]
  end

  subgraph Render
    R1[render_outputs]
    OUT[SVG/PNG/HTML/TSV/PDF]
  end

  Y --> P1
  M --> P1
  P1 --> F1
  F1 -->|Harness| R1
  F1 --> DR
  DR --> DH
  R1 --> OUT
```

Key points:

- `DocumentRepresentation` captures metadata, page stubs, notes, BOM (if enabled), and options.
- Written to `*.document.yaml` with hash tracking in `document_hashes.yaml`; user edits are preserved (no overwrite if hash changes).
- Rendering still operates on the harness; the document YAML is a pre-render view for inspection or manual tweaking.
- If a matching `*.document.yaml` already exists, it is loaded to drive options/page selection and merged formats before rendering.
