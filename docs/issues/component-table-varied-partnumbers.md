# Issue: Refine component_table template for varied partnumbers
uid: ISS-0103
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

## Summary

The component_table template currently assumes shared/duplicate partnumber fields when rendering lists. This can hide valid cases where partnumbers differ per entry. Refine the template/model/tests so varied partnumbers render gracefully without forcing duplication.

## Requirements

- Allow non-duplicated partnumbers to render in component_table.html.
- Adjust the model/factory and tests to cover varied partnumber lists (distinct manufacturers/PN/MPN/etc.).
- Ensure shared-field optimization (keep_only_shared) still works but doesn’t block varied displays.

## Related

- src/filare/models/templates/component_table_template_model.py
- tests/templates/test_component_table_template_model.py
