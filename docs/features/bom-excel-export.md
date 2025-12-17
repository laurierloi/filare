# BOM Excel export

uid: FEAT-BOM-0100
status: BACKLOG
priority: low
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Summary

Provide a BOM export to Excel (XLSX) in addition to current TSV/HTML outputs, as requested by legacy task `230329GTW2_bom_class_generate_excel_see_MR`.

## Requirements

- Add an Excel/XLSX BOM export option (CLI flag/config) that mirrors TSV content and formatting expectations.
- Ensure BOM pagination/quantity data matches existing outputs.
- Document usage and include a regression example/test for XLSX export.

## Related Items

- BOM pagination: `docs/features/bom_pagination.md` (existing).
