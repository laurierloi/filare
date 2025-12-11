uid: FEAT-DOCS-0004
status: IN_PROGRESS
priority: high
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Filare Interface Models Contract

## Summary

Define explicit, user-facing interface models to represent the YAML contract Filare accepts. These models live under `src/filare/models/interface/`, inherit from a shared `FilareInterfaceModel` base, and use only YAML-friendly types (scalars, lists, dicts). They serve as the single source of truth for input validation, JSON Schema generation, and downstream tooling that needs to understand allowed inputs.

## Goals

- Provide a clear, versioned interface contract for Filare inputs.
- Generate JSON Schema directly from interface models to aid docs, tooling, and compatibility checks.
- Keep interface models decoupled from internal/legacy dataclasses while offering adapters to internal models.
- Detect contract changes (breaking or additive) via schema diffs and targeted tests.
- Enable future tooling (e.g., editors, CLI validation) to rely on these schemas without guessing YAML structure.
- Use Pydantic v2 for all interface models; every `Field` must include a human-friendly `description` so schema/docs stay self-explanatory.

## Scope and Placement

- New interface models live in `src/filare/models/interface/<model_name>.py`.
- All interface models subclass `FilareInterfaceModel` (new base in the same package) to centralize config (strict mode, extra handling) and helpers (schema export, version tagging).
- Models expose only simple types that align with YAML primitives; any richer types are expressed as enums or nested interface models.
- Converters/adapters map interface models to existing internal/domain models without changing rendering or BOM behaviors.
- Each interface model includes a companion `factory_boy` factory named `Fake<ModelName>Factory`, subclassing `FakeInterfaceFactory`. The base factory must provide helpers to emit YAML from generated instances so tests can render flows directly from interface models.

## JSON Schema Generation

- Schema is produced from the interface models (e.g., `FilareInterfaceModel.model_json_schema()`).
- CI/tests will snapshot schemas to detect contract drift; docs will link to the generated schema as a user-facing contract.
- Schema artifacts are guidance only; source of truth remains the Python models.

## Change Management

- Additive fields default-safe to preserve compatibility; breaking changes require explicit review.
- Interface model versions (e.g., `schema_version`) recorded in the base class to track migrations.
- Tests cover:
  - Model validation of representative YAML inputs.
  - Round-trip or adapter correctness to internal models.
  - Schema stability snapshots.
  - Factories (`FakeInterfaceFactory` subclasses) build valid models and export YAML suitable for rendering.

## Workflow Overview

1. User supplies YAML → parsed to interface models (strict validation).
2. Interface models → JSON Schema (for docs/tooling) and adapters → internal models/flows.
3. Internal processing/rendering unchanged; interface layer isolates user contract from internal refactors.

## Open Questions / To Refine

- Which top-level inputs get models first (metadata/options/connectors/cables/connections)?
- How to publish schema artifacts (path, versioning strategy)?
- Do we provide a CLI flag to emit schema or validate files against it directly?

## Next Steps

- Introduce `FilareInterfaceModel` base with shared config and schema helper.
- Define initial interface models (metadata, options, connectors, cables, connections).
- Add schema generation wiring (build task + tests) and document usage in examples/tutorials.
