# Template: Procurement BOM (minimal layout)
uid: ISS-0022
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

Add a procurement-focused BOM template that outputs a clean table (no title block/diagram) for purchasing teams. Keep page size flexible (A4/A3), with optional grouping by supplier.

## Model

```python
class ProcurementBomRow(BaseModel):
    line: int
    part_number: str
    description: str
    quantity: float
    unit: str = "ea"
    supplier: Optional[str]
    supplier_pn: Optional[str]
    reference: Optional[str]  # harness/page reference

class ProcurementBomContext(BaseModel):
    rows: List[ProcurementBomRow]
    metadata: Metadata  # for title/part numbers
    options: PageOptions  # for fonts/colors
```

## Template Content

- Page wrapper reuses `page.html` base sizing but hides diagram/titleblock.
- Simple table: columns for Line, Part Number, Description, Qty, Unit, Supplier, Supplier PN, Reference.
- Optional grouping by supplier (toggle flag in context).
- Summary footer (total unique parts, total quantity).

## Where Used

- Standalone export for purchasing/procurement handoff.
- CI artifact when `formats` includes a procurement flag (e.g., `B`).
