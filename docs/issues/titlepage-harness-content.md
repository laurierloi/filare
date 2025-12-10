# Titlepage includes harness content
uid: ISS-0037
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

- Titlepage output currently shows a "Harness" content entry when split pages or content listings are generated; titlepage should be limited to index/title information only.

## Suggested Next Steps

- Adjust titlepage rendering/index generation to omit any harness content rows for the titlepage.
- Add regression test to ensure titlepage pages do not list or embed harness content blocks.
- Verify downstream templates and index tables remain correct once titlepage content is pruned.
