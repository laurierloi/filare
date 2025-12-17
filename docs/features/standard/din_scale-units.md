# DIN Scale and Units

uid: FEAT-DOCS-0013
status: BACKLOG
priority: high
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Summary

Surface scale and units in title blocks per DIN/EN ISO practices (metric default, explicit scale or “NTS” when not to scale).

## Requirements

- Metadata fields for scale and units; default to metric.
- Title block rendering for scale/units fields.
- Validation to ensure scale/units are present or explicitly marked NTS.

## Steps

- [ ] Add scale/unit metadata and defaults.
- [ ] Render fields in title block templates.
- [ ] Add regression fixtures asserting scale/unit text in SVG/HTML.

## Progress Log

- 2025-02-20: Feature drafted from DIN research; awaiting implementation.

## Related Issues

- docs/issues/din-scale-units.md
