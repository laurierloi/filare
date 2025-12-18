uid: FEAT-CLI-0016
status: IN_PROGRESS
priority: high
owner_role: REWORK
estimate: TBD
dependencies: [FEAT-DOCS-0004]
risk: medium
milestone: backlog

# Filare Interface Flows and CLI

## Summary

Define interface-specific flows under `src/filare/flows/interface/` and expose them via a new `filare interface` CLI group. Each flow accepts a mapping of interfaces and a selected key, returns a fully populated `FilareInterfaceModel` instance, and can emit validated YAML. The CLI must let users load, edit, save, check, and generate interface YAML without altering the underlying contract. Each interface also ships a sibling `Configuration` model (per-interface, initially empty) in `src/filare/models/interface/` to host parsing modifiers, plus a `Fake<Interface>InterfaceFactory` to seed `generate` output and tests.

## Deliverables

- Flow module per interface type (metadata, options, connector, cable, connection, harness) exporting load/save helpers that round-trip YAML ↔ interface models.
- Shared conventions for input dict shape, validation, defaults, and error handling across all flows.
- CLI group `filare interface` with subcommands: `load`, `edit`, `save`, `check`, `generate`, wired to the flows and supporting all interface types.
- Per-interface `Configuration` model defined alongside the interface model to capture behavior toggles (can start empty but is the future home of modifiers).
- Per-interface `Fake<Interface>InterfaceFactory` available for CLI `generate` and for tests that need sample YAML.
- Documentation and examples that demonstrate flow usage and CLI invocations for each interface type.

## Common Flow Requirements

- Accept inputs as `interfaces: dict[str, Any]` plus `key: str`; raise a clear error if the key is missing or the payload is empty.
- Normalize/alias field names before validation (e.g., respect `from` aliasing in connections) and reject unexpected keys via `FilareInterfaceModel.model_validate`.
- Apply mapping-key fallbacks where the model expects a designator (e.g., set `designator` when absent for keyed connectors/cables).
- Preserve or default `schema_version`, enforce `extra="forbid"`, and strip whitespace consistently.
- Return a fully validated model instance and expose a `to_yaml()` save helper that emits YAML with stable key order and no Python-specific artifacts.
- Provide consistent error objects/exceptions for downstream CLI: include interface type, key, and validation details.
- Accept an optional per-interface configuration object to tweak parsing/normalization; the configuration model lives next to the interface model. Configuration selection supports `--config` plus optional `--config-key` (use the whole config when no key is given).

## CLI Behavior Requirements

- Typer-based CLI: use Typer for the `filare interface` group with pretty/colored logs and friendly prints configured globally.
- Command shape: `filare interface <type> <action> [OPTIONS]`, where `<type>` is one of `metadata|options|connector|cable|connection|harness` and `<action>` is `load|edit|save|check|generate`.
- `load`: read YAML (stdin or file), pick `--key <id>`, run the flow, print a normalized YAML dump of the selected interface.
- `edit`: same as load, apply `--set key=value` or `--patch file.yaml` mutations, then validate and preview diff before saving.
- `edit` may optionally open the user's editor (`$EDITOR`/`$VISUAL`) when `--editor` is set; default remains non-interactive.
- `save`: write the validated interface YAML to `--output <path>`; refuse to clobber unless `--force` is set.
- `check`: validate without writing; exit non-zero on errors and print structured validation failures.
- `generate`: emit sample YAML for the chosen interface type using the corresponding `Fake<Model>Factory`; allow `--count` and `--output` to control quantity and destination.
- All subcommands must accept `--interfaces-file <path>` (YAML map of interfaces), `--key`, and `--format yaml|json` for output. Config-aware commands also accept `--config <path>` and optional `--config-key` to select a sub-config.
- CLI must be non-interactive by default; any editor-based flows must be opt-in and avoid opening editors in automation.

## Implementation Steps (Imperative)

- Create `src/filare/flows/interface/__init__.py` plus one module per interface type with `load_<type>`, `save_<type>`, and shared error helpers.
- Add unit-style checks that guard required keys, normalize aliases, and populate designators before calling `model_validate`.
- Wire CLI entrypoints in `src/filare/cli.py` (or a dedicated Typer app) to dispatch to the correct flow based on `<type>` and `<action>`, enabling Typer's pretty output configuration.
- Reuse `FakeInterfaceFactory` instances to seed `generate` outputs and to provide defaults when the requested interface payload is incomplete.
- Add usage notes to examples/tutorials once flows and CLI ship; keep schema and rendering behavior unchanged.
