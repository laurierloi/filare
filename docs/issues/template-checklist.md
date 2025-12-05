# Template: Assembly/Test Checklist

## Category

UI — Importance: Medium

## Proposal

Add a checklist template for assembly or test steps tied to a harness. Provides step descriptions, expected results, and pass/fail/notes columns for technicians.

## Model

```python
class ChecklistItem(BaseModel):
    step: int
    description: str
    expected: Optional[str]
    tools: Optional[str]
    note: Optional[str]

class ChecklistContext(BaseModel):
    title: str
    metadata: Metadata
    items: List[ChecklistItem]
    options: PageOptions
```

## Template Content

- Header with part number, revision, title, and optional harness/page name.
- Table columns: Step, Description, Expected, Tools, Result (checkbox), Notes.
- Space for technician initials/date at bottom.
- Printable spacing and alternating row shading for readability.

## Where Used

- Assembly and verification workflows accompanying diagrams/BOMs.
- QA signoff packages requiring step-by-step confirmation.
