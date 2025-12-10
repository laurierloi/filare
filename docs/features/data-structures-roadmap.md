# Data structures and parts library roadmap

uid: FEAT-DATA-0001
status: PLANNED
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Summary

Track data-structure tasks from `docs/tasks.md`, including networkx exploration, BOM/notes structures, and part library/bundle modeling.

## Scope

- Networkx graph exploration: `230404GTW1_networkx_all_familly_info_within_a_graph`, `230327GTW1_try_networkx_to_represent_harness_connections`, `230327GTW2_try_networkx_to_represent_harnesses_connections`
- BOM content/IDs: `230531GTW1_use_BomContent_class_in_xsc_harness_and_for_shared_bom`, `230329GTW4_BOM_class_has_unique_id_per_part_from_instantiation`
- Notes as class within components: `230629GTW1_use_notes_class_within_components`
- Parts library: `230327GTW4_part_independently_defined`, `230327GTW5_connector_from_a_part_library`, `230327GTW6_cable_from_a_part_library`
- Recursive/bundled cables: `230330GTW4_cable_are_recursive_aka_a_group_of_cable_or_wire`, `230330GTW6_outer_cable_is_just_a_bundle_of_bundle/cable/wire`

## Proposed Next Steps

1. Map overlaps with `docs/features/config-graph-models.md` and `docs/features/pydantic-migration.md`; decide integration points.
2. Prioritize BOM/notes structure changes and part library groundwork.
3. Add designs/experiments (networkx) and document outcomes; add regressions as features land.

## Related Items

- `docs/tasks.md` data-structure backlog.
- `docs/features/config-graph-models.md`, `docs/features/pydantic-migration.md`.
