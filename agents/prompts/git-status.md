---
description: '---- Operator interaction ----  ----------------------------------------------------
  REVIEW COMMAND (interactive) ----------------------------------------------------
  Usage: just review agent_role="FIXER" task_id="42"  Optional: diff_base="origin/beta"  Example:
  just review \ agent_role="FEATURE" \ task_id="88" \ diff_base="origin/main"   ----------------------------------------------------
  GET STRUCTURED REVIEW (agent-friendly, read-only) ----------------------------------------------------
  Usage: just get-structured-review agent_role="FIXER" task_id="42"  This prints the
  contents of: outputs/review/<agent_role>-<task_id>-<step_index>/ in a structured
  format the agent can parse.   ---- Git ----'
---

---- Operator interaction ----  ---------------------------------------------------- REVIEW COMMAND (interactive) ---------------------------------------------------- Usage: just review agent_role="FIXER" task_id="42"  Optional: diff_base="origin/beta"  Example: just review \ agent_role="FEATURE" \ task_id="88" \ diff_base="origin/main"   ---------------------------------------------------- GET STRUCTURED REVIEW (agent-friendly, read-only) ---------------------------------------------------- Usage: just get-structured-review agent_role="FIXER" task_id="42"  This prints the contents of: outputs/review/<agent_role>-<task_id>-<step_index>/ in a structured format the agent can parse.   ---- Git ----
Category: lint.

Command to run inside the repo:
```bash
source scripts/agent-setup.sh >/dev/null && just git-status
```
After execution, summarize the outcome succinctly and mention any errors or next steps.
