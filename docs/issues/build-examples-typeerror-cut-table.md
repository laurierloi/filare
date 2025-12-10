# `just build-examples` fails on cut table generation

uid: ISS-0003
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


## Category

BUG

## Evidence

- Running `source scripts/agent-setup.sh >/dev/null && just build-examples` aborts on the first example (`examples/ex01.yml`) with `TypeError: can only concatenate str (not "int") to str`.
- Repro via `source scripts/agent-setup.sh >/dev/null && uv run filare run examples/ex01.yml -f ghpstb -o examples` shows the failure originates in `_build_cut_table` (`src/filare/models/harness.py`), at `{"wire": f"{cable.designator}-{idx + 1}", ...}`.
- The cut-table builder iterates `cable.wire_objects`, whose keys include the shield id `'s'`; adding `1` to `'s'` raises the TypeError.

## Hypothesis

- Cut table generation assumes all wire ids are numeric, but shield ids are strings (`"s"`). When options enable `include_cut_diagram` (true for `ex01`), the shield entry triggers `idx + 1` with a string id, crashing the run and stopping the examples build.

## Steps Taken

- Reproduced with `just build-examples` and `uv run filare run examples/ex01.yml -f ghpstb -o examples`.
- Traced the stack to `_build_cut_table` (`src/filare/models/harness.py`) where `idx + 1` is evaluated on a shield id `"s"`.
- Implemented a guard that formats wire suffixes by coercing numeric ids to int and leaving non-numeric ids as-is.
- Added regression coverage for shielded cables with cut diagrams (`tests/models/test_harness_unit.py::test_build_cut_table_handles_shield_id`).

## Fix Summary

- `src/filare/models/harness.py`: avoid adding integers to non-numeric wire ids when building cut-table labels (handles shield `"s"` ids).
- `tests/models/test_harness_unit.py`: regression test to ensure shield wires render without raising and keep a sensible `-s` suffix.

## Suggested Next Steps

- None; fix and regression test in place.
