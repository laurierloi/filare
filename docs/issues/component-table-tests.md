# Issue: Strengthen component_table template tests

uid: ISS-0203
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

## Status

BACKLOG

## Summary

Current component_table template tests only assert the presence of designators because the template rendering doesn’t surface row descriptions directly. Improve the tests (and, if needed, the template/model payload) so descriptions/notes are validated explicitly.

## Requirements

- Investigate why descriptions are not present in rendered component_table output.
- Update the model/test setup or the template to ensure row descriptions are rendered.
- Tighten assertions to check descriptions (and notes) instead of only designators.

## Progress Log

2025-12-11: Filed issue after loosening assertions to designators in component_table tests.

## Related

- tests/templates/test_component_table_template_model.py
- docs/features/templates/component_table_model.md
