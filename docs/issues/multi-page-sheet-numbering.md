# Sheet numbering incorrect in multi-page documents

## Category
FEATURE

## Evidence
- Multi-page outputs (e.g., paginated BOM/cut/termination pages) show sheet numbers that do not align with page suffixes or split pages. Example: sheet numbering remains static or mismatched when lettered suffixes are present.

## Suggested Next Steps
- Reproduce with `examples/multi-page` builds and inspect sheet number rendering across base and lettered pages.
- Ensure sheet_current/sheet_suffix are set appropriately per split page and propagated into titleblocks/index metadata.
- Add regression tests to validate correct sheet numbering for split BOM/cut/termination pages with letter suffixes. 
