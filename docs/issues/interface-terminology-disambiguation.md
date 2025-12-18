uid: ISS-0120
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Disambiguate "interface" terminology

## Summary

Clarify and separate the usage of "interfaces" for YAML parsing models versus "interface" as a logical electrical interface node to avoid user and developer confusion. Ensure docs, CLI help, and flow naming consistently distinguish configuration interfaces (parsing layer) from electrical interfaces (graph semantics).

## Tasks

- Document the preferred terms for parsing interfaces vs. logical/electrical interfaces and update relevant docs/features.
- Audit CLI help/commands to ensure naming clearly signals which meaning is intended.
- Adjust internal comments/names where necessary to avoid conflating the two concepts.
