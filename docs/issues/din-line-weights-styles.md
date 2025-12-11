# DIN line weights and styles

uid: ISS-0050
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

Category: FEATURE

## Summary

Parameterize line weights and styles (visible/hidden/center) to DIN 15 / EN ISO 128 defaults and apply them across rendered outputs.

## Evidence

- DIN research notes line weights are not standardized in current outputs.
- EN ISO 128 defines stroke widths/dash patterns expected on compliant drawings.

## Recommended steps

1. Define default stroke widths/dash patterns for line types.
2. Apply styles in renderers/templates.
3. Add regression fixture checking SVG strokes/classes against DIN defaults.
