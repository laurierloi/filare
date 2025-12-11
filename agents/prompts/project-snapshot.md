---
description: Show current git status and Filare version as a quick snapshot.
---

Show current git status and Filare version as a quick snapshot.
Category: meta.

Command to run inside the repo:
```bash
source scripts/agent-setup.sh >/dev/null && bash -lc 'git status -sb && just version'
```
After execution, summarize the outcome succinctly and mention any errors or next steps.
