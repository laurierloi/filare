# DIN revision table support

uid: ISS-0048
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

Category: FEATURE

## Summary

Add a revision table to Filare outputs capturing revision ID, date, description, and approvals, per DIN/EN ISO practices.

## Evidence

- DIN research identifies lack of revision table in current templates.
- Compliance often requires a revision history block on drawings.

## Recommended steps

1. Define revision metadata schema.
2. Render revision table in templates when provided.
3. Add regression fixture verifying table structure/values in outputs.
