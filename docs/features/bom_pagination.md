# BOM Pagination and Derivative Diagrams

uid: FEAT-BOM-0001
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

Add BOM pagination controls and new derivative diagrams (wire cut and termination tables) with shared table modeling, configurable page splits, and documentation/examples that surface the new outputs.

## Requirements

- Add option to force the BOM onto a single page; support optional multi-page BOM splitting with configurable rows per page and lettered page suffixes (a, b, c, …).
- Introduce a reusable table model shared by BOM, wire cut diagram, and termination diagram, and integrate it into rendering.
- Add per-harness wire cut diagram (HTML table) with optional multi-page splitting and lettered suffixes in page numbering.
- Add per-harness termination diagram (HTML table) capturing splices/crimps and lengths; support multi-page splitting and lettered suffixes.
- Add a BaseModel for termination details, allowing per-wire-end/connection definitions into connectors.
- Extend examples/tutorials to generate the new schematics and document usage, including example outputs of the new diagrams.
- Add configuration knobs so users can choose whether to include the new schematics in the engineering document.

## Steps

- [x] Design pagination/table model approach and config knobs for BOM and derivative diagrams.
- [x] Implement BOM pagination options and integrate shared table model.
- [x] Implement wire cut diagram generation with pagination.
- [x] Implement termination diagram generation with pagination and termination BaseModel.
- [x] Update tests, examples/tutorials, and docs to cover the new outputs and configuration.
- [x] Validate renders/regressions and finalize feature documentation.

## Progress Log

2025-12-04: Created feature file from RefactorPlan step 11 and marked IN_PROGRESS with requirements and steps.
2025-12-04: Added shared table pagination helpers, BOM/cut/termination pagination with lettered suffix handling, and sheet suffix support.
2025-12-04: Added pagination regression tests and documented new pagination options.
2025-12-04: Ran pagination regressions (`tests/features/bom_pagination`, `tests/flows/test_examples_and_tutorial.py`, `tests/render/test_split_sections.py`) and marked feature DONE.

## Sub-Features

- None

## Related Issues

- RefactorPlan step 11
