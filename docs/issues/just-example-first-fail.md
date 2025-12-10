# `just example-first` fails on titlepage generation

uid: ISS-0019
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


## Category

BUG

## Evidence

- Running `source scripts/agent-setup.sh >/dev/null && just example-first` exits with `KeyError: 'template'` while generating the titlepage HTML.
- Stack trace points to `src/filare/render/html.py:572` (`titlepage_metadata["template"]["name"] = "titlepage"`) invoked from `_render_cli` during HTML rendering of `examples/demo01.yml`.
- The extra metadata assembled for the titlepage lacks a `template` key, so `generate_titlepage` attempts to index into a missing dict.

## Steps Taken

- Reproduced with `source scripts/agent-setup.sh >/dev/null && just example-first`.
- Added a template metadata fallback in `generate_titlepage` to always set `template.name = "titlepage"`.
- Updated `_render_cli` to pass harness metadata files when none are provided, so titlepage metadata includes required fields (title/pn/company/address).
- Re-ran `just example-first`; it now completes successfully and writes outputs for `demo01`.

## Fix Summary

- `src/filare/render/html.py`: ensure titlepage metadata has a `template` dict with name forced to `titlepage`.
- `src/filare/cli/render.py`: use harness files as metadata input when no explicit metadata files are passed, preventing missing required Metadata fields.
- `tests/flows/test_shared_bom_and_index.py`: added regression test to cover titlepage generation when only harness metadata is provided (mirrors `just example-first`).

## Status

Resolved (manual verification via `just example-first`; regression test added).

## Remaining Tasks

- None.
