uid: FEAT-GENERAL-0007
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: 3d
dependencies: []
risk: medium
milestone: backlog

# Drone Autopilot (PX4/ArduPilot) Harness

## Summary

- Create a Filare harness for a typical Pixhawk-class flight controller with power module, ESC/servo rails, GPS/compass, telemetry radio, and RC receiver.

## Source Assets

- PX4 and ArduPilot wiring quick-start docs (Pixhawk 4/6/6X pinouts, power module schematics).
- Airframe reference builds (quadrotor/VTOL) with labeled connectors.

## Connectors & Interfaces

- Servo rail (PWM) to 4–8 ESCs/servos via 3-pin JST-GH headers.
- Power module XT60/XT90 in/out with current/voltage sense to FC power port.
- GPS/compass via JST-GH (UART + I²C); telemetry radio over UART/USB; RC input (SBUS/PPM).
- Optional CAN (UAVCAN) peripheral bus for smart ESCs/sensors.

## Real-World Example

- Widely used in hobby and professional drones; large PX4/ArduPilot communities and vendor ecosystems (Holybro, CUAV).

## Work Outline

- Use Pixhawk 4 pinout as baseline; include battery→power-module→PDB/ESC path and signal harness.
- Provide quadrotor YAML plus variant enabling UAVCAN peripherals.
- Add rendering test in `tests/rendering/`.
