# DIN scale and units

uid: ISS-0053
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

Category: FEATURE

## Summary

Expose scale and units in title blocks per DIN/EN ISO practices (metric default, explicit scale or NTS when not to scale).

## Evidence

- DIN research shows scale/units are not consistently surfaced.
- Compliance requires clear scale/unit declaration in the title block.

## Recommended steps

1. Add metadata for scale and units; default to metric with NTS option.
2. Render scale/unit fields in title block templates.
3. Add regression fixtures asserting scale/unit text in outputs.
