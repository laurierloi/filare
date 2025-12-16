# Issue: Add fixtures for nested template rendering
uid: ISS-0104
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

## Summary

Several templates render the output of other templates (e.g., page includes titleblock, din-6771 includes notes/BOM). Identify all such dependencies and update tests to use fixtures that render the dependent templates before embedding them in the parent’s factory/test. This ensures nested rendering paths stay consistent and exercised.

## Requirements

- Inventory templates that include/extend other template renders (e.g., page/titleblock, din-6771/notes/bom, cut/cut_table, cable/component_table, connector/component_table).
- For each dependent relationship, add a pytest fixture that renders the child template via its factory and injects it into the parent factory in tests.
- Ensure tests assert that nested rendered content is present in the parent render.

## Related

- tests/templates/test_page_template_model.py
- tests/templates/test_din_6771_template_model.py
- tests/templates/test_cut_template_model.py
- tests/templates/test_cable_template_model.py
- tests/templates/test_connector_template_model.py
