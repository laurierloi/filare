# Template: Approvals / Signoff Page

uid: ISS-0021
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Category

UI — Importance: High

## Proposal

Add an approvals/signoff template for engineering release packets. The page captures designer/reviewer (and optional approver) signatures with dates and comments, without diagrams/BOM.

## Model

```python
class ApprovalSlot(BaseModel):
    role: str           # e.g., Designer, Reviewer, Approver
    name: Optional[str]
    date: Optional[str]
    comment: Optional[str]
    signature: Optional[str]  # path/URL to image or base64 data URI

class ApprovalPageContext(BaseModel):
    metadata: Metadata        # part number, revision, title, company
    approvals: List[ApprovalSlot]  # at least Designer + Reviewer
    notes: Optional[str]      # optional release note/summary
    options: PageOptions      # fonts/colors/page size
```

## Template Content

- Based on `page.html` sizing, with no diagram/BOM.
- Header showing part number, revision, title, and company.
- Two or three signature blocks (Designer, Reviewer, optional Approver) with printed name, date, comment, and signature image placeholder line if no image provided.
- Optional notes section for release rationale or scope.

## Where Used

- Release/QA packages requiring explicit signoff from designer and reviewer.
- Front-matter page in bundled PDFs for compliance workflows.
