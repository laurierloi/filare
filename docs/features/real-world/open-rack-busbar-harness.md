uid: FEAT-GENERAL-0003
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: 4d
dependencies: []
risk: medium
milestone: backlog

# Open Rack Busbar / Power Shelf Harness

## Summary

- Model a high-power data-center harness based on the Open Compute Project (Open Rack ORv2/ORv3) rear 12 V busbars feeding power shelves and server sleds.

## Source Assets

- OCP Open Rack specifications (busbar geometry, blind-mate connectors, power shelf cabling rules) and CAD hosted on the OCP wiki.
- Example ORv2 power shelf harness diagrams from community builds and vendor design guides.

## Connectors & Interfaces

- Rear 12 V DC busbars with finger-safe contacts; blind-mate server sled connectors.
- DC branch cables to power shelves (often Molex Extreme Guardian-style or similar high-current connectors).
- Sense/PMBus telemetry cabling to power shelves and BMC.

## Real-World Example

- Deployed in OCP data centers and lab racks; open specs enable community/academic builds and vendor-neutral interoperability.

## Work Outline

- Extract connector stack-up and pin/current tables from ORv2/ORv3 spec.
- Model rack-level busbar plus a power-shelf harness with sense lines.
- Provide simplified YAML variant for labs using 48 V conversion (if documented).
