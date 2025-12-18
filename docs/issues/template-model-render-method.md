uid: ISS-0217
status: IN_PROGRESS
priority: medium
owner_role: REWORK
estimate: 1d
dependencies: []
risk: low
milestone: templates-models

# Add TemplateModel.render helper and update tests

## Summary

Add a `render()` method to `TemplateModel` that renders the model using its `template_name` and `to_render_dict()`, then update all template tests to use this helper instead of calling `get_template(...).render(...)` directly. This ensures a consistent, model-centric render path in tests and simplifies future refactors.

## Requirements

- Implement `TemplateModel.render()` in `src/filare/models/templates/template_model.py`, using `get_template(f"{template_name}.html")` and `to_render_dict()`.
- Update template tests (`tests/templates/*`) to call `model.render()` instead of `get_template(...).render(...)`.
- Keep behavior unchanged; this is a test-focused API addition.

## Related

- src/filare/models/templates/template_model.py
- tests/templates/
