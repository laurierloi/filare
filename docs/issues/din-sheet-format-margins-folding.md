# DIN sheet format, margins, and folding marks

uid: ISS-0046
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

Category: REWORK

## Summary

Implement EN ISO 5457 / DIN 823 sheet sizes, margins, frames, and folding marks in Filare templates.

## Evidence

- DIN research highlights the need for standardized frames and folding marks.
- Current templates reference DIN sizes but lack folding marks and strict margin enforcement.

## Recommended steps

1. Add DIN presets for sheet sizes/margins and render folding marks.
2. Provide configuration toggle and defaults that preserve existing outputs.
3. Add regression checks on SVG viewBox/frame and folding mark coordinates.
