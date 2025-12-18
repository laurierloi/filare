uid: FEAT-GENERAL-0004
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: 3d
dependencies: []
risk: medium
milestone: backlog

# Industrial Control (RS485 / Modbus) Harness

## Summary

- Create a Filare example for small industrial control panels using open-source PLC hardware (OpenPLC runtime on DIN-rail I/O, or Industrial Shields Arduino/RPi PLCs) with RS485/Modbus field wiring.

## Source Assets

- OpenPLC hardware community designs and wiring guides for digital/analog IO and RS485 links.
- Industrial Shields open-hardware PLC datasheets with pluggable screw-terminal pinouts (24 V IO, dual RS485/RS232, Ethernet).
- OpenDINRail OSHW 24 V I/O module schematics and BOM (Phoenix-style terminals, daisy-chain connector).

## Connectors & Interfaces

- Pluggable screw terminals for 24 V DI/DO/AI, relay outputs.
- RS485 (A/B/GND) trunk with termination/screen connections; optional RS232 and Ethernet.
- Power feed: 24 V DC DIN-rail supply; earth/chassis bonding.

## Real-World Example

- Makers and educators using OpenPLC on Raspberry Pi with RS485 IO blocks; Industrial Shields units deployed in light automation and building controls; OSHW OpenDINRail community builds.

## Work Outline

- Choose a concrete stack: RPi + RS485 HAT + OpenDINRail IO module or Industrial Shields M-Duino.
- Capture pin tables (DI/DO/AI) and RS485 termination harness.
- Provide panel-level YAML with trunk + drops, plus a minimal test in `tests/rendering/`.
