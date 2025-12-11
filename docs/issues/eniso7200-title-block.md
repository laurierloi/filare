# EN ISO 7200 title block fields

uid: ISS-0047
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

Category: REWORK

## Summary

Standardize title blocks to EN ISO 7200 fields (title, drawing number, revision, date, author/checker/approver, scale, projection, sheet/total, company) and validate presence.

## Evidence

- DIN research notes current title block templates are not aligned to EN ISO 7200.
- Missing mandatory fields can block compliance with EU suppliers.

## Recommended steps

1. Define metadata keys for each EN ISO 7200 field.
2. Update templates to include all required fields in standard order/layout.
3. Add lint/regression to ensure required fields are present in rendered outputs.
