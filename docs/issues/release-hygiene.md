# Release and publishing hygiene

## Category

DOCUMENTATION

## Evidence

- TODO.md lists: ensure PyPI metadata is complete; create icon/style; ensure package release on PyPI and GitHub; github.io page operational; add documentation generator for GH Pages; publish/package only on version tags.
- RefactorPlan step 6: document tag-triggered release workflow, semantic-release changelog generation, and GH/PyPI token notes.

## Expected Outcome

- Clear, documented release process covering semantic-release triggers, tag-only publishing, and GH Pages deployment.
- Up-to-date PyPI metadata and branding assets (icon/style).
- GH Pages/Docs build flow documented and verified.

## Proposed Next Steps

1. Audit current release pipeline (semantic-release config, GH Actions) and document tag-based publishing and token requirements.
2. Verify PyPI project metadata; add missing fields if any (long description, project URLs, classifiers).
3. Confirm GH Pages/docs build flow (mkdocs) and document operator steps.
4. Decide on icon/style assets and include branding guidance.
5. Update TODO.md/tasks lists with links to this issue and mark items covered once done.

## Related Items

- RefactorPlan step 6.
- TODO.md release/branding items.
