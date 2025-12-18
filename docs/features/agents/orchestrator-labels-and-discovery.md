# Container labeling and discovery for orchestrated sessions

uid: FEAT-TOOLS-0012
status: BACKLOG
priority: medium
owner_role: TOOLS
estimate: TBD
dependencies: [FEAT-TOOLS-0003, FEAT-TOOLS-0005]
risk: medium
milestone: backlog

## Summary

Ensure all orchestrated containers carry consistent labels (e.g., `filare.session`, `filare.role`, `filare.branch`) so lifecycle commands (resume, stop, tail, dashboard) can discover and target the right container without manual IDs.

## Proposal

- Update the Python runner (`orchestrator.run_container`) to apply labels on `docker run`.
- Use labels in `resume-all`, tail, stop/restart, and dashboard collection to find containers.
- Optionally name containers predictably (`filare-<session-id>`).

## Verification & Validation

- Containers launched via orchestrator show expected labels (`docker ps --filter label=filare.session=...`).
- Lifecycle commands can locate containers using labels alone.

## Dependencies

- Builds on container launcher (`FEAT-TOOLS-0003`) and lifecycle (`FEAT-TOOLS-0005`).

## Progress / Notes

- Added label support to the Python container runner (`orchestrator.run_container`) and pass session/role/branch from `build_run_command`; labels applied to `docker run`.
- Next: consume labels in resume/stop/tail/dashboard for container discovery; optionally set predictable container names.
