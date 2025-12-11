---
description: 'Quick CI-like sanity check: tools, lint, fast tests and first example
  build.'
---

Quick CI-like sanity check: tools, lint, fast tests and first example build.
Category: test.

Command to run inside the repo:
```bash
source scripts/agent-setup.sh >/dev/null && bash -lc 'just check-tools && just lint && just test-fast && just example-first'
```
After execution, summarize the outcome succinctly and mention any errors or next steps.
