uid: FEAT-CLI-0017
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: [FEAT-CLI-0016, FEAT-DOCS-0004]
risk: medium
milestone: backlog

# Metadata Interface Flow and CLI

## Summary

Implement a metadata interface flow that extracts one metadata block from a mapping, builds a `MetadataInterfaceModel`, and exposes CLI actions to load/edit/save/check/generate metadata YAML. Define a sibling `MetadataConfigurationInterfaceModel` (can start empty) to host parsing modifiers, and a `FakeMetadataInterfaceFactory` for sample generation and tests.

## Usage Targets

- Feeds document title block and revision/author rendering in HTML/Graphviz outputs.
- Provides metadata for downstream BOM/title pages and any schema export relying on document identity.

## Flow Requirements

- Accept `metadata_map: dict[str, Any]` and `key: str`; fail fast if the key is missing or payload is empty.
- Normalize the payload (strip whitespace, drop null-only fields), then call `MetadataInterfaceModel.model_validate`.
- Ensure `template` defaults to `TemplateInterfaceModel` when omitted; keep authors/revisions dictionaries intact without rekeying.
- Preserve `schema_version`; allow overriding only through explicit parameter, not implicit defaults.
- Return the validated model plus `to_yaml()` output for serialization; surface validation errors with key/type context.
- Accept an optional configuration object (`MetadataConfigurationInterfaceModel`) to control parsing tweaks as they are added; support `--config <path>` and optional `--config-key` to select a sub-config (use entire config when not provided).

## CLI Hooks

- `filare interface metadata load|check`: read YAML map, select `--key`, optional `--config/--config-key`, validate via the flow, and print normalized YAML or errors.
- `edit`: accept `--set title=\"...\" --set pn=...` style overrides or open `$EDITOR`/`$VISUAL` when `--editor` is provided, accept `--config/--config-key`, revalidate, and show a diff before optional save.
- `save`: write validated YAML to `--output`, honoring `--force` for overwrite and `--format yaml|json`.
- `generate`: use `FakeMetadataInterfaceFactory` to emit sample entries keyed by provided identifiers; allow `--count` and `--seed`.

## Completion Criteria

- Flow and CLI paths enforce the common interface guarantees (keyed input, forbid extras, stable YAML output).
- Required metadata fields (`title`, `pn`, `company`, `address`) are enforced; optional signature fields remain optional.
- Example commands documented to show load/edit/save/check/generate paths for metadata.
