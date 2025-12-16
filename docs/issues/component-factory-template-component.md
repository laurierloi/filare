uid: ISS-0102
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

# Issue: Add FakeComponentFactory and TemplateComponent derivation helper

## Summary

Add a faker-backed `FakeComponentFactory` in `src/filare/models/component.py` to generate realistic ComponentModel instances, plus a helper to derive the TemplateComponent used by `component_table.html` from it. This would reduce duplication across template factories and keep template payloads aligned with the core component model.

## Requirements

- Implement a `FakeComponentFactory` alongside ComponentModel in `component.py`, producing populated fields (designators, partnumbers, notes, additional_components, etc.).
- Provide a conversion/helper to derive the `TemplateComponent` used in `component_table_template_model` directly from a generated ComponentModel.
- Keep factory parameters configurable (e.g., partnumber count, notes/images toggles).

## Related

- src/filare/models/component.py
- src/filare/models/templates/component_table_template_model.py
- tests/templates/test_component_table_template_model.py
