# EN ISO 7200 Title Block Compliance

uid: FEAT-DOCS-0007
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Summary

Standardize Filare title blocks to EN ISO 7200 fields (title, drawing number, revision, date, author/checker/approver, scale, projection, sheet/total, company).

## Requirements

- Provide a title block template with all EN ISO 7200 fields in standard layout/order.
- Map metadata keys to each field; warn when required fields are missing.
- Keep backward-compatible defaults for existing docs.

## Steps

- [ ] Define metadata keys and template slots for each EN ISO 7200 field.
- [ ] Implement rendering/template updates for EN ISO 7200 layout.
- [ ] Add validation/lint to ensure required fields are present; add regression fixture on SVG/HTML.

## Progress Log

- 2025-02-20: Feature drafted from DIN research; awaiting implementation.

## Related Issues

- docs/issues/eniso7200-title-block.md
