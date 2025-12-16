uid: ISS-0105
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

# Issue: Save rendered template outputs for review

## Summary

When running template tests, rendered HTML/diagrams aren’t persisted. Add an option/fixture to write rendered outputs to a dedicated directory (e.g., `outputs/tests/templates/<template_name>.html`) so operators can review artifacts after test runs.

## Requirements

- Identify all template render tests (under `tests/templates/`).
- Add a consistent mechanism (pytest fixture or helper) to save rendered output for each template into `outputs/tests/templates/`.
- Ensure directory creation is handled and paths are deterministic per template/test.
- Keep saving optional/configurable to avoid polluting outputs during normal runs.

## Related

- tests/templates/\*
