# Log handling and configuration switches
uid: ISS-0014
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

Filare currently emits logs from flow fallbacks, option normalization, and tooling, but there is no centralized way to configure log levels/handlers. Users must rely on defaults or set global Python logging manually.

## Category

FEATURE

## Motivation

- Provide a consistent way to enable/disable logging noise across commands (`filare`, `filare-qty`, tools).
- Allow redirecting logs to files or structured outputs without custom wrappers.
- Align CLI flags/env vars with documentation and developer expectations.

## Proposal

1. Introduce a logging configuration helper backed by Pydantic settings:
   - Env prefix: `FIL_LOG_`.
   - Settings fields: `level` (default INFO), `dir` (optional), `config_file` (YAML path), `config` (pre-parsed dict).
2. Support Python logging YAML configs:
   - Load YAML → dict → `logging.config.dictConfig`.
   - If both YAML and settings are provided, apply YAML first, then override `level`/`dir` from settings/env.
   - Warn if the YAML cannot be parsed; fall back to default console logging.
3. CLI flags take precedence over all other inputs:
   - `--log-level` overrides settings/env/YAML level.
   - `--log-dir` overrides settings/env/YAML handler destinations when applicable (e.g., FileHandler root path).
4. Document precedence:
   - CLI flags > env (`FIL_LOG_*`) > YAML config file > built-in defaults.
5. Add regression tests ensuring CLI invocations honor the requested log level and file output.

## Notes

This issue focuses on configuring handling (levels, destinations); log source guidelines are tracked separately in `docs/dev/logging-sources.md`.
