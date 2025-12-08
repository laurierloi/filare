# Filare Logging Sources and Guidance

This note documents where Filare emits logs and when to add new ones. It focuses on log sources, not log handling or configuration.

## Current log sources

- **Flow fallbacks**: `flows/build_harness.py` logs warnings when document options contain invalid color overrides so users can fix the input document.
- **Option normalization**: `models/options.py` warns when non-numeric pagination values are provided, indicating automatic pagination will be used instead.
- **Render imports**: `render/imported_svg.py` logs info when SVG dimensions are non-numeric and viewBox injection is skipped; suggests providing numeric sizes.
- **Example build tooling**: `tools/build_examples.py` warns when a `.document.yaml` file cannot be parsed and the manifest omits its metadata.

## When to add logs

- Prefer `warning` when a user-provided configuration or input can be corrected to avoid the fallback behavior.
- Prefer `info` when Filare transparently chooses a safe default and user action is optional.
- Do not log inside tight loops or per-item validation unless the message is actionable and deduplicated.

## What to include

- The offending input value and its source (file/path/field).
- The fallback behavior and any user-visible consequence.
- A short hint on how the user can correct the input.
