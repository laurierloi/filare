uid: ISS-0121
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Enforce interface models as inputs across the codebase

## Summary

Ensure every interface type is used as the structured input to downstream logic instead of relying on raw parsed YAML dicts. Map how each interface model feeds internal models and flows, and add any missing adapters to carry interface data into the existing pipelines.

## Objectives

- Audit where current code consumes raw YAML dicts and replace with the corresponding interface models.
- Identify and document the path from each interface model into internal models/flows; list any new flows/adapters needed to bridge gaps (research to be done later).
- Add validation/usage checks to prevent bypassing interface models in future code.
