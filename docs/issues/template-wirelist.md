# Template: Wire List / Netlist

uid: ISS-0032
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

Add a wire list template that outputs a concise netlist-style table for each connection, useful for technicians and testers. Focus on source/target pins, wire IDs, colors, lengths, and terminations.

## Model

```python
class WireListRow(BaseModel):
    wire_id: str
    from_ref: str        # e.g., connector_a.1
    to_ref: str          # e.g., connector_b.1
    color: Optional[str]
    length: Optional[str]
    source_term: Optional[str]
    target_term: Optional[str]
    note: Optional[str]

class WireListContext(BaseModel):
    rows: List[WireListRow]
    metadata: Metadata
    options: PageOptions
```

## Template Content

- Table columns: Wire ID, From, To, Color, Length, Source Termination, Target Termination, Note.
- Optional grouping by harness/page; print page title/part number in header.
- Printable layout with wrap/ellipsis for long labels; alternate row shading.

## Where Used

- Assembly/test teams needing a compact netlist separate from diagrams.
- CI artifacts for connectivity checks.
