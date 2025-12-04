# Clarify connector loop syntax and examples (Resolved)
The connector `loops` documentation was previously mis-indented, missing accepted keys, and lacked a working YAML example.

## Category
DOCUMENTATION

## Evidence
- Prior to PR #<number>, docs/syntax.md:84-91 showed the `loops` section with mis-indented YAML and no example; the keys were unclear and omitted optional fields like `color` and supported tuple shorthand.
- The previous text did not explain how `side` and `show_label` affect rendering or how loops interact with connector pin activation, leaving users to guess the proper structure.

## Resolution
The documentation was updated in PR #<number> (docs/syntax.md lines 85-104) to clarify the `loops` subsection, provide a clean YAML snippet listing accepted keys (`first`, `second`, `side`, `show_label`, `color`), note the tuple shorthand, and add a minimal example. Rendering constraints and links to test/example harnesses were also added as appropriate.

## Status
Resolved
