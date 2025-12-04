# Document Representation and Change Tracking

## Status
IN_PROGRESS

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
- [ ] Confirm existing document generation flow and current handling of `.document.yaml` outputs/inputs.
- [ ] Design and document `*.document.yaml` input handling, including hash preservation and path resolution rules.
- [ ] Implement consumption of `*.document.yaml` inputs in rendering flows with tests covering round-trip and edit preservation.
- [ ] Add cut diagram and termination diagram templates and wire them into rendering and output selection.
- [ ] Adjust page generation to omit split components from the combined page when splits are requested.
- [ ] Expand the index table to list all generated documents with page name, content type, and link; include split outputs.
- [ ] Add regression tests and example YAMLs demonstrating split outputs, cut/termination templates, and document input acceptance.
- [ ] Update relevant docs (syntax/guides) to describe new inputs, templates, and index table behavior.
- [ ] Run lint/tests and prepare implementation on branch `FEATURE/document-reporesentation`.

## Progress Log
2025-12-04: Drafted feature plan for RefactorPlan task 12; awaiting operator review before implementation.

## Sub-Features
- None.

## Related Issues
- RefactorPlan task 12 (Document representation and change tracking).
