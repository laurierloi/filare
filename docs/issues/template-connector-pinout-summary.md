# Template: Connector Pinout Summary
## Category
UI — Importance: High
## Proposal
Add a connector pinout summary template that lists each connector with its pins, functions, colors, and mating info, aggregated on a single page.
## Model
```python
class PinInfo(BaseModel):
    pin: str
    signal: Optional[str]
    color: Optional[str]
    gauge: Optional[str]
    termination: Optional[str]

class ConnectorSummary(BaseModel):
    name: str           # designator (e.g., J1)
    description: Optional[str]
    part_number: Optional[str]
    mate: Optional[str]
    pins: List[PinInfo]

class ConnectorPinoutContext(BaseModel):
    connectors: List[ConnectorSummary]
    metadata: Metadata
    options: PageOptions
```
## Template Content
- Table per connector: header with name/description/PN/mate; pin table with Pin, Signal, Color, Gauge, Termination columns.
- Optional compact multi-connector layout for A4/A3; alternating row shading for readability.
## Where Used
- Technician reference sheet for wiring/testing without full diagrams.
- QA packs needing quick pin/function lookup.
