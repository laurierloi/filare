# Template: Diagram Grid Border (Lettered)

uid: ISS-0033
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Category

UI — Importance: Medium

## Proposal

Add an optional lettered/numbered grid border around diagram pages so users can pinpoint locations (standard drawing practice). Grid labels (A, B, C… on one axis; 1, 2, 3… on the other) should overlay margins without obscuring diagrams.

## Model

```python
class GridBorderOptions(BaseModel):
    enabled: bool = True
    columns: int = 4     # number of vertical divisions (A, B, C, D…)
    rows: int = 4        # number of horizontal divisions (1, 2, 3, 4…)
    offset_mm: float = 5 # margin offset from frame
    font_size_mm: float = 3
    color: str = "#000"

class GridBorderContext(BaseModel):
    metadata: Metadata
    options: PageOptions
    grid: GridBorderOptions
```

## Template Content

- Overlay around `page.html`/`harness` diagrams: small labels on top/bottom (letters) and left/right (numbers) positioned in the margin.
- Non-intrusive CSS so diagrams remain unchanged; labels sit outside the frame border.
- Configurable divisions, font size, and color via `grid` options; default 4x4 grid.

## Where Used

- Harness diagrams for technicians/reviewers who need to reference locations (“See A3 for issue”).
- Printed/PDF outputs where standard drawing grids are expected.
