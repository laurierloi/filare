# Pydantic migration of core models

uid: FEAT-PYDANTIC-0001
status: PLANNED
priority: high
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: beta

## Summary

Migrate legacy dataclasses (Component/Connector/Cable/BOM/color helpers) and config objects to Pydantic BaseModels with round-trip YAML compatibility, then update flows/CLI/rendering to consume the new models while preserving behavior.

## Requirements

- Add Pydantic BaseModels for connectors, cables, BOM, color helpers, and config inputs (ConnectorConfig/CableConfig/WireConfig/ConnectionConfig/MetadataConfig/PageOptionsConfig/PinConfig).
- Provide template-input models and mapping layers from config -> BaseModels -> template inputs.
- Incrementally wire parsing/build flows to use BaseModels without breaking existing YAML/CLI behavior; keep legacy compatibility until migration completes.
- Remove `arbitrary_types_allowed` usage by adding proper converters/wrappers.
- Replace dataclass usage in rendering once parity is validated; plan removal of `src/filare/models/dataclasses.py` after migration.

## Steps

- [ ] Scaffold BaseModels for core components and configs with validation and defaults.
- [ ] Add conversion/mapping layer to template-input models; include round-trip tests.
- [ ] Wire build/render flows to accept BaseModels, keeping legacy paths temporarily.
- [ ] Sweep for `arbitrary_types_allowed` and replace with explicit type handling.
- [ ] Validate parity against examples/tests; add regressions where gaps appear.
- [ ] Deprecate and remove dataclass usage once parity is confirmed.

## Related Items

- RefactorPlan steps 3, 7, 8, 13.
- `docs/tasks.md`: pydantic BaseModel migration entries.
