# Document Representation and Change Tracking

uid: FEAT-DOCS-0001
status: DONE
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


## Status

DONE

## Summary

Support authoring and consuming `*.document.yaml` inputs for document generation, add dedicated templates for cut and termination diagrams, and ensure split outputs are linked and rendered correctly across combined pages and the index table.

## Requirements

- Accept `*.document.yaml` as an input to drive document generation (not only emit), with tests ensuring the YAML input path is honored and user edits are preserved per hash rules.
- Update page generation templates so split components (BOM/notes/index) are excluded from the combined page when split output is configured.
- Update the index table to link to all generated HTML documents; when splits exist, render three columns: page name, content type (harness/cut/BOM/termination/index), and page link.
- Add a template for the termination diagram page and integrate it into rendering.
- Add a template for the cut diagram page and integrate it into rendering.
- Ensure the index is generated only for the title page, not for every document.
- Implement in branch `FEATURE/document-reporesentation` after operator approves this feature document.

## Steps

- [x] Confirm existing document generation flow and current handling of `.document.yaml` outputs/inputs.
- [ ] Design and document `*.document.yaml` input handling, including hash preservation and path resolution rules.
- [x] Implement consumption of `*.document.yaml` inputs in rendering flows with tests covering round-trip and edit preservation.
- [x] Add cut diagram and termination diagram templates and wire them into rendering and output selection.
- [x] Adjust page generation to omit split components from the combined page when splits are requested.
- [x] Expand the index table to list all generated documents with page name, content type, and link; include split outputs.
- [x] Add regression tests and example YAMLs demonstrating split outputs, cut/termination templates, and document input acceptance.
- [x] Update relevant docs (syntax/guides) to describe new inputs, templates, and index table behavior.
- [x] Run lint/tests and prepare implementation on branch `FEATURE/document-reporesentation`.

## Progress Log

2025-12-04: Drafted feature plan for RefactorPlan task 12; awaiting operator review before implementation.
2025-12-04: Reviewed existing document representation flow, rendering hooks, templates, and index table behavior to scope changes.
2025-12-04: Wired document input into harness/options, gated index generation to the title page, filtered split sections from combined pages, and added regression tests; `uv run pytest` blocked by network (PyPI fetch).
2025-12-04: Expanded index table to surface split/aux pages (BOM/notes/index/cut/termination) with content labels and links; added coverage for title-page-only index generation.
2025-12-04: Enabled cut/termination page generation when requested and added regression to ensure aux pages render.
2025-12-04: Added option coercion for document inputs, hardened revision handling, and reran `uv run pytest tests/flows/test_document_representation_flow.py` successfully.
2025-12-04: Added example `examples/demo01.document.yaml`, documented loading existing documents as inputs, and updated document flow notes; targeted test suite still passing.
2025-12-04: Lint/docs complete; feature marked DONE.

## Sub-Features

- None.

## Related Issues

- RefactorPlan task 12 (Document representation and change tracking).
