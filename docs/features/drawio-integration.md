from: docs/features/drawio-svg-import.md

# DrawIO Authoring Integration

## Status

WAITING_FOR_OPERATOR

## Summary

Provide tighter DrawIO integration so Filare can generate SVGs directly from DrawIO source files, create new DrawIO files from harness metadata, and optionally open DrawIO on demand for a given harness.

## Requirements

- Support generating output SVGs directly from DrawIO (`.drawio` or `.dio`) sources without manual export steps.
- Offer a command or workflow to create a starter DrawIO file from a Filare harness name/metadata, including basic layout scaffolding.
- Provide an option to launch DrawIO with the generated or existing file for interactive editing from the Filare tooling.
- Preserve compatibility with existing SVG import flows and avoid forcing DrawIO usage when not needed.
- Document the end-to-end flow for using DrawIO with Filare, including generation, editing, and embedding.

## Steps

- [ ] Define workflow and CLI/API surface for generating SVGs from DrawIO files and for creating starter DrawIO files from harness metadata.
- [ ] Implement DrawIO invocation/automation to produce SVGs and to open files on demand, with safe defaults and fallbacks.
- [ ] Add docs and regression examples demonstrating the DrawIO-integrated workflow end to end.

## Progress Log

2025-12-04: Created follow-up feature request for deeper DrawIO integration; pending operator review.

## Sub-Features

- None.

## Related Issues

- None.
