# Improve loop validation and graph rendering errors

uid: ISS-0022
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


## Category

REWORK

## Evidence

- `src/filare/models/dataclasses.py:408` raises `ValueError(f"Unsupported loop definition: {loop}")` without showing valid shapes or the connector designator.
- `src/filare/render/graphviz.py:72` raises `Exception("No side for loops")` with no connector/pin context when rendering loops.
- Unsupported loop values or missing sides result in opaque crashes during render instead of pointing to the specific connector in YAML.

## Suggested Next Steps

1. For invalid loop shapes, include the connector name and expected keys: `connector X1: loop entry {'foo': 1} is invalid; expected {'first', 'second', optional 'side'|'show_label'|'color'} or [<first>, <second>]`.
2. For missing side in graphviz, include connector and loop pins: `connector X1: loop between pins 1-2 missing side; set side: LEFT|RIGHT or omit to auto-place`.
3. Add a small YAML regression in `tests/rendering/` with a bad loop entry and assert the improved error string.
