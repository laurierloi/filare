# filare ex command for example builds

uid: FEAT-CLI-0016
status: IN_PROGRESS
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

Expose the existing `src/filare/tools/build_examples.py` workflow as a first-class subcommand under the main Filare CLI (`filare ex`). The command should mirror the current tool flags (action, groups, output-dir) so CI and local users can build or clean example outputs without invoking the script directly.
