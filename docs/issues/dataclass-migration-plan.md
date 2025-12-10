# Dataclass migration plan for Connector/Cable/Wire
uid: ISS-0007
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

Category: REWORK

## Summary

Gradually migrate remaining dataclass-heavy models (Connector, Cable, WireClass/ShieldClass, Connection/Loop wiring flows) to Pydantic BaseModels while keeping legacy imports stable.

## Evidence

- Dataclass usage in `src/filare/models/dataclasses.py` underpins connectors/cables/wires and connection wiring; it couples rendering/flows to mutable objects and complicates validation.
- Recent primitives extraction and Pydantic models (Component/Cable/Connector/etc.) exist, but wiring objects (Pin/Loop/Connection) still rely solely on dataclasses.
- Tests still import dataclasses directly for enums/constants and wiring objects, indicating ongoing coupling.

## Recommended steps

1. Introduce Pydantic models for Connector/Cable wiring that leverage the new Pin/Loop/Connection adapters; ensure parity converters to/from dataclasses.
2. Update flows (`build_harness`, renderer helpers) to accept Pydantic wiring models while preserving legacy dataclass usage until full switch.
3. Sweep tests to consume Pydantic adapters where possible; add regression coverage for connection/wire creation and BOM quantities.
4. Deprecate direct dataclass imports in a staged manner (module-level shims) once consumers are migrated; then remove `models/dataclasses.py` or gate it behind compatibility layer.

## Risks/notes

- Rendering code expects dataclass-specific attributes/mutability; adapters must retain behavior during transition.
- Graphviz output relies on pin activation side effects; ensure Pydantic-backed objects preserve those semantics or provide compatibility wrappers.
- Legacy YAML parsing might construct dataclasses implicitly; migration must keep backward compatibility paths until schemas are confirmed stable.
