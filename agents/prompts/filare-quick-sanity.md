---
description: 'Run a minimal Filare sanity: example build, overlap check, BOM check.'
---

Run a minimal Filare sanity: example build, overlap check, BOM check.
Category: filare.

Command to run inside the repo:
```bash
source scripts/agent-setup.sh >/dev/null && bash -lc 'just example-first && just check-overlap && just bom-check'
```
After execution, summarize the outcome succinctly and mention any errors or next steps.
