---
description: List next ready tasks for a role from Taskwarrior export  Split Taskwarrior
  backlog into dependency-safe pools  Update a Taskwarrior task (status/notes) in
  the export; can stamp completion time  Generate a branch name from a Taskwarrior
  task UID (optionally check out)  Generate Graphviz timeline (DOT + optional SVG)
---

List next ready tasks for a role from Taskwarrior export  Split Taskwarrior backlog into dependency-safe pools  Update a Taskwarrior task (status/notes) in the export; can stamp completion time  Generate a branch name from a Taskwarrior task UID (optionally check out)  Generate Graphviz timeline (DOT + optional SVG)
Category: project_management.

Command to run inside the repo:
```bash
source scripts/agent-setup.sh >/dev/null && just timeline-graphviz
```
After execution, summarize the outcome succinctly and mention any errors or next steps.
