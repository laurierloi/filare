# Template Models and Factories

## Status
IN_PROGRESS

## Summary
Add Pydantic template models under `src/filare/models/templates/` (one per template in `src/filare/templates/*.html`) inheriting from `template_model.py`, plus factory_boy factories to cover all template attributes for testing.

## Requirements
- Create a model per template file (e.g., `additional_components.html` -> `additional_components_model.py`) inheriting from `template_model.py`.
- Add factory_boy factories for each model to generate complete attribute permutations for template tests.
- Keep naming and field coverage aligned with the template context used in rendering.
- Backward compatible: no changes to existing template rendering inputs/outputs.

## Steps
- [x] Inventory templates and align naming for model files and factories.
- [x] Define shared/base fields in `template_model.py` and extend per-template models with specific fields.
- [x] Add factory_boy-style factories for each template model with sensible defaults and complete attribute coverage.
- [ ] Wire models/factories into tests that exercise templates with full attribute sets.
- [ ] Update docs/help to describe template model coverage and factory usage.

## Progress Log
2025-12-10: Created parent feature and outlined requirements/steps.
2025-12-10: Added template models/factories for all templates under `src/filare/templates/`; tests/docs wiring pending.
2025-12-11: Implemented base `TemplateModel` + factory_boy factory with render-focused tests, `render` pytest marker, classvar `template_name`, and forbidden extras to align with strict template payloads.
2025-12-11: Implemented AdditionalComponentsTemplateModel + factory and render tests (faker-backed, id/unit variants, multi-component coverage).
2025-12-11: Implemented ConnectorTemplateModel + faker factory and render tests (ports/pincolor variants, pincount coverage).
2025-12-11: Implemented BomTemplateModel + faker factory and render tests (reverse header variants).
2025-12-11: Implemented CableTemplateModel + faker factory and render tests (wirecount/shield variants).
2025-12-11: Implemented ColorsMacroTemplateModel + faker factory and render tests (legend count variants).
2025-12-11: Implemented ComponentTableTemplateModel + faker factory and render tests (partnumber list vs single, notes/images/additional components).
2025-12-11: Implemented CutTableTemplateModel + faker factory with typed colors and render tests.
2025-12-11: Implemented CutTemplateModel + faker factory that renders cut_table HTML with varying row counts.
2025-12-11: Implemented Din6771TemplateModel + faker factory with notes/BOM toggles and diagram container styling plus render tests.
2025-12-11: Implemented ImagesTemplateModel + faker factory (caption/fixed-size variants) and render tests.

## Command & Testing Notes
- Use `just test-specific <path> -- <args>` to target template model tests, e.g., `just test-specific tests/templates/test_additional_components_model.py`.
- Faker-backed factories generate IDs and descriptions dynamically; when asserting, prefer reading values from the model instead of hard-coding literals.
- When templates render lists/rows, include tests across small/medium/large counts (e.g., 1/10/50) to exercise layout and header/footer paths.

## Sub-Features
- templates/additional_components_model
- templates/bom_model
- templates/cable_model
- templates/colors_macro_model
- templates/component_table_model
- templates/connector_model
- templates/cut_model
- templates/cut_table_model
- templates/din-6771_model
- templates/images_model
- templates/index_table_model
- templates/notes_model
- templates/page_model
- templates/simple-connector_model
- templates/simple_model
- templates/termination_model
- templates/termination_table_model
- templates/titleblock_model
- templates/titlepage_model

## Related Issues
- None
