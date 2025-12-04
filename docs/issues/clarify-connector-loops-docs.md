# Clarify connector loop syntax and examples
The connector `loops` description is mis-indented, missing accepted keys, and lacks a working YAML example.

## Category
DOCUMENTATION

## Evidence
- docs/syntax.md:84-91 shows the `loops` section with mis-indented YAML and no example; the keys are unclear and omit optional fields like `color` and supported tuple shorthand.
- The current text does not explain how `side` and `show_label` affect rendering or how loops interact with connector pin activation, leaving users to guess the proper structure.

## Suggested Next Steps
1. Rewrite the `loops` subsection with a clean YAML snippet that lists accepted keys (`first`, `second`, `side`, `show_label`, `color`) and notes the tuple shorthand.
2. Add a minimal example illustrating a loop rendered on a specific side with/without labels, tied to the existing pins in a connector definition.
3. Mention any rendering constraints (e.g., sides required when pins are only on one side) and link to a test/example harness if available.
