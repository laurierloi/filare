# Template: Notes/Changelog Page
## Category
UI
## Proposal
Add a notes-only/changelog template to capture release notes, approvals, and revision history without diagrams or BOM. Provides a clean page for managers/QA signoff.
## Model
```python
class ChangeLogEntry(BaseModel):
    revision: str
    date: str
    author: str
    summary: str

class NotesPageContext(BaseModel):
    title: str
    metadata: Metadata  # for part number/company/revision
    notes: List[str]    # bullet notes or paragraphs
    changelog: List[ChangeLogEntry]
    options: PageOptions  # fonts/colors/page size
```
## Template Content
- Based on `page.html` sizing; removes diagram/BOM blocks.
- Sections: Title header (from metadata/title), Notes list, Changelog table (Rev/Date/Author/Summary), optional approvals/signatures row.
- Uses shared CSS tokens for spacing to align with other pages.
## Where Used
- Release packages where a narrative or signoff page is required alongside harness diagrams.
- QA/manager review packets; front-matter in PDF bundles.
