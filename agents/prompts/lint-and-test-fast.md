---
description: Run linting and fast tests together for quick feedback.
---

Run linting and fast tests together for quick feedback.
Category: test.

Command to run inside the repo:
```bash
source scripts/agent-setup.sh >/dev/null && bash -lc 'just lint && just test-fast'
```
After execution, summarize the outcome succinctly and mention any errors or next steps.
