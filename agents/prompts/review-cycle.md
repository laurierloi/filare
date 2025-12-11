---
description: Run interactive human review, then print the structured review so the
  agent can consume it in the next step. Intended for orchestrator/human use.
argument-hint: AGENT_ROLE="<value>" TASK_ID="<value>"
---

Run interactive human review, then print the structured review so the agent can consume it in the next step. Intended for orchestrator/human use.
Category: project_management.
Marked unsafe for automatic agents — confirm before running.

Command to run inside the repo:
```bash
source scripts/agent-setup.sh >/dev/null && bash -lc 'just review agent_role="$AGENT_ROLE" task_id="$TASK_ID" && just get-structured-review agent_role="$AGENT_ROLE" task_id="$TASK_ID"'
```

Provide the required arguments when invoking the slash command, e.g.:
/prompts:review-cycle AGENT_ROLE="..." TASK_ID="..."
After execution, summarize the outcome succinctly and mention any errors or next steps.
