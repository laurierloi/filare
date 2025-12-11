# Dataclass migration plan for Connector/Cable/Wire

uid: ISS-0010
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

## Upcoming steps for the next slice

1. Sweep remaining direct dataclass imports (`connections.py`, `wire.py`, `graphviz.py`, `models/__init__.py`) and replace them with model-first shims plus lazy dataclass fallbacks where compatibility requires.
2. Thread connector/cable/wire models through harness/build_harness and renderer helpers so model inputs are normalized before touching dataclasses; add regression coverage for loop normalization and model-based adders.
3. Once shims are in place, narrow `models/__init__.py` dataclass exports and document the compatibility layer to guide downstream consumers.

### Progress 2025-12-10

- Color helpers: migrated `MultiColor` to a Pydantic model and kept legacy iteration/formatting semantics; validated usage surfaces for connectors/cables/render.
- Wiring shims: added `WireModel`/`ShieldModel` Pydantic adapters with round-trip converters to `WireClass`/`ShieldClass`; tests cover basic roundtrips and ConnectionModel now accepts wire models.
- Flow integration: `Harness.connect_model()` added to route ConnectionModel/dict through existing connect logic; build_harness_from_models can consume connection models for straight-through wiring setup.
- Next: peel renderer/graphviz to accept connection/wire models, and incrementally replace direct dataclass usage in graph building and BOM population.

### Progress 2025-12-10 (later)

- Resolved rebase conflicts while keeping HEAD changes intact and added compatibility aliases for GraphicalComponent to smooth imports.
- Normalized `ConnectorModel.to_connector()` to emit loop dictionaries from `LoopModel`/`PinModel` inputs so the dataclass constructor can validate pins consistently.
- Extended `Harness.add_connector`/`add_cable` to accept models and dicts, keying by the resulting designator to avoid unhashable model keys; validated with `just test-all`.
- Next: continue peeling dataclass imports from `connections.py` and `wire.py`, and tighten `models/__init__.py` exports once the shim coverage is broader.
