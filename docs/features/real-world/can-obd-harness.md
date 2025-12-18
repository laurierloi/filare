uid: FEAT-GENERAL-0002
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: 3d
dependencies: []
risk: medium
milestone: backlog

# CAN / OBD-II Vehicle Harness

## Summary

- Provide a Filare example for an automotive interface harness (OBD-II to CAN/USB accessory), using OpenXC reference design or Speeduino/aftermarket ECU breakouts.

## Source Assets

- OpenXC vehicle interface hardware docs: OBD-II pinout, dual-CAN transceiver mapping, 12 V accessory output, USB/UART.
- Speeduino wiring diagrams for Arduino Mega/Teensy ECUs (injector, ignition, sensors).

## Connectors & Interfaces

- OBD-II 16-pin male/female with J1962 footprint.
- Dual CAN_H/CAN_L pairs, K-line/L-line (optional), 12 V and chassis ground.
- USB or UART header for host connection; optional Molex MicroFit or JST for accessories.

## Real-World Example

- Used by OpenXC fleet telemetry dongles, Speeduino DIY ECUs, and openpilot camera harness adapters; broad car enthusiast and maker communities.

## Work Outline

- Capture standard OBD-II pin map and OpenXC transceiver wiring.
- Model inline harness: OBD-II passthrough + break-out to CAN/USB accessory.
- Add vehicle-specific variant (e.g., Toyota CAN with ignition sense) as YAML sample.
