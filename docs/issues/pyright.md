# Pyright typing cleanup plan

uid: ISS-0026
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


Pyright currently reports ~262 errors across CLI, flows, models, render, and tooling. This plan tracks goals and phased fixes.

## Goals

- Bring Pyright to zero errors on the codebase under `./scripts/pyright.sh` using the config in `pyproject.toml`.
- Avoid behavior changes; prioritize typing correctness and narrow annotations.
- Keep changes incremental with passing pytest.

## Scope

- CLI and flow argument types (`cli.py`, `filare.py`, `flows/build_harness.py`, `parser/harness_parser.py`).
- Model construction and validators (BOM, cable, metadata, partnumber, template inputs).
- Render utilities (graphviz/html/html_utils/pdf).
- Harness/index table typing.

## Phased steps

1. **CLI/entrypoints**: Fix `cli.py` and `filare.py` signatures and data shims; ensure tuples/sets are coerced to expected types.
2. **Flows/build_harness**: Type the connection/templates metadata and resolve Optional Path/str issues; adjust helper signatures for dict/model unions.
3. **Parser**: Narrow YAML merge function inputs (List vs tuple).
4. **Models (BOM/partnumber/cable/component)**: Clean setter overloads, Optional handling, and enum coercions; fix logging reference in `bom.py`.
5. **Render (graphviz/html/pdf/html_utils)**: Align return types (Table vs str), handle optional ImportedSVGOptions, and correct iterable types.
6. **Harness/index_table**: Fix tuple/list type expressions and Optional fields.
7. **Final sweep**: Re-run Pyright and pytest; document remaining suppressions if any.

## Progress

- [ ] Step 1: CLI/entrypoints
- [ ] Step 2: Flows/build_harness
- [ ] Step 3: Parser
- [ ] Step 4: Models (BOM/partnumber/cable/component) — in progress
- [ ] Step 5: Render
- [ ] Step 6: Harness/index_table
- [ ] Step 7: Final sweep (pyright + pytest)

### Models progress (Step 4)

- Adjusted `models/bom.py` qty_multiplier typing and added logging import.
- Updated `models/utils.py` signature for `smart_file_resolve` (broader path types).
- Guarded NumberAndUnit arithmetic against `None`.

## Notes

- Use minimal structural changes; prefer explicit casts/narrowing helpers where inputs are permissive.
- If any change appears user-visible, pause and consult.\*\*\*
