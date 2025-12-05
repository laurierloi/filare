# Template: Label Sheet (Wire/Connector Tags)
## Category
UI
## Proposal
Add a label-sheet template to generate printable tags for wires/connectors. Users can print adhesive labels with designator, pin, color, and optional QR/shortcode.
## Model
```python
class LabelEntry(BaseModel):
    ref: str            # e.g., W1, J2-3
    text: str           # display text (pin/function)
    color: Optional[str]
    qty: int = 1
    qr: Optional[str]   # data to encode (optional)

class LabelSheetContext(BaseModel):
    labels: List[LabelEntry]
    metadata: Metadata
    options: PageOptions
    columns: int = 3         # grid columns
    rows: int = 8            # grid rows
    cell_width_mm: float = 60
    cell_height_mm: float = 20
```
## Template Content
- Grid layout with configurable rows/columns and cell dimensions.
- Each cell shows ref, text, color swatch, optional QR/shortcode block.
- Minimal borders for cutting; supports repeating labels per `qty`.
## Where Used
- Printing wire/connector markers for assembly.
- Providing quick ID stickers for QA/testing.
