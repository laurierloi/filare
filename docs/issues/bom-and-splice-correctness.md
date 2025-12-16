# BOM and splice correctness
uid: ISS-0200
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Category

FIXER

## Evidence

- Loopback connections without explicit cables may miss length/gauge capture in the BOM.
- Splices involving differing gauges should surface in BOM output with guidance (e.g., “near connector”) but aren’t explicitly tracked.
- A cables overview summarizing runs and key attributes isn’t documented separately.

## Expected Outcome

- BOM includes loopback lengths/gauges when no explicit cable is defined.
- Splices involving differing gauges surface in BOM with location guidance.
- Cables overview section summarizes runs and key attributes.

## Proposed Next Steps

1. Identify current BOM behavior for loopbacks and gauge-mismatch splices; add regression YAML if missing.
2. Implement/verify loopback length/gauge capture and splice inclusion with guidance text.
3. Add cables overview output and document its structure.
4. Add tests/regressions for loopback and splice cases; update docs/examples accordingly.
