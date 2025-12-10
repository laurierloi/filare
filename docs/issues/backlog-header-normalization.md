uid: ISS-PM-0001

uid: ISS-0002
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


# Add standard headers to all backlog files

Category: TOOLS

## Summary

Apply the new planning header (uid, status, priority, owner_role, estimate, dependencies, risk, milestone) to every file in `docs/issues/` and `docs/features/` to make work items addressable in manifests, Taskwarrior, Mermaid, and timeline exports.

## Evidence

- Current backlog markdown lacks consistent metadata; only some items list Category or Status.
- Project-management research recommends immutable UIDs and normalized fields for automation and conflict avoidance.

## Recommended steps

1. Assign UIDs using the standard format (`ISS-<4 digits>` for issues, `FEAT-<AREA>-<4 digits>` for features) as documented in `docs/issues/header-template.md`.
2. Sweep all backlog files to insert the header block with unique UIDs and normalized fields.
3. Add a manifest entry for each item using the new UIDs to prepare for generator outputs.
4. Update contributor guidance to require the header on new backlog items (add the scheme to AGENTS.md and any contributor docs).

## Risks/notes

- Needs careful UID assignment to avoid duplicates; consider a simple allocator or maintainer review gate.
- Some files may already contain partial metadata; ensure canonical values are chosen during the sweep.
