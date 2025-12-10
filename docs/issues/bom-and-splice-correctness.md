# BOM and splice correctness

## Category

FIXER

## Evidence

- RefactorPlan step 9 calls for loopback support to capture length/gauge when cables aren’t explicit, ensuring splices from differing gauges appear in the BOM with “near connector” guidance, and adding a cables overview.
- Current docs/features do not track these BOM correctness items separately.

## Expected Outcome

- BOM includes loopback lengths/gauges when no explicit cable is defined.
- Splices involving differing gauges surface in BOM with location guidance.
- Cables overview section summarizes runs and key attributes.

## Proposed Next Steps

1. Identify current BOM behavior for loopbacks and gauge-mismatch splices; add regression YAML if missing.
2. Implement/verify loopback length/gauge capture and splice inclusion with guidance text.
3. Add cables overview output and document its structure.
4. Add tests/regressions for loopback and splice cases; update docs/examples accordingly.

## Related Items

- RefactorPlan step 9.
