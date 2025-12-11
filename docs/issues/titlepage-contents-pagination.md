# Paginate titlepage contents table when large

uid: ISS-0043
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Category

FEATURE

## Evidence

- The titlepage content/index table can grow long (multiple harnesses/split pages) and currently stays on the titlepage without pagination. When it exceeds a reasonable length, it should be split out.

## Suggested Next Steps

- Introduce a threshold (default 20 rows) to emit the content/index table on its own page when it exceeds that size.
- Keep links and sheet numbering consistent with lettered suffix behavior for split pages.
- Make the threshold configurable via options.
- Add a regression example and test covering a multi-harness document exceeding the threshold.
