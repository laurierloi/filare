---
description: Build documentation, validate Mermaid diagrams and backlog headers.
---

Build documentation, validate Mermaid diagrams and backlog headers.
Category: project_management.

Command to run inside the repo:
```bash
source scripts/agent-setup.sh >/dev/null && bash -lc 'just build-docs && just mermaid-gantt-check && just check-backlog-headers'
```
After execution, summarize the outcome succinctly and mention any errors or next steps.
