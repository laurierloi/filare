# Fix README link targets

uid: ISS-0016
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

Landing-page links to syntax/tutorial/example docs point to missing paths, producing broken GitHub and docs-site navigation.

## Category

DOCUMENTATION

## Evidence

- README.md:90-94 links to `syntax.md`, `tutorial/readme.md`, and `examples/readme.md` from repository root, but those files live under `docs/` and `tutorial/`, so the GitHub links are broken.
- docs/README.md:81-85 uses the same relative paths, which resolve to non-existent `docs/tutorial/...` and `docs/examples/...` locations when browsing the docs site.

## Suggested Next Steps

1. Update links in both README files to target the actual files (e.g., `docs/syntax.md`, `tutorial/readme.md`, `examples/readme.md`) so they work on GitHub and in the rendered docs.
2. Verify MkDocs navigation still resolves correctly after adjusting paths, adding site-relative links if needed.
3. Add a quick smoke check note (or automated link check reference) to prevent regressions in internal documentation links.
