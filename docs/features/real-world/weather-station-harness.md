uid: FEAT-GENERAL-0001
status: BACKLOG
priority: high
owner_role: FEATURE
estimate: 2d
dependencies: []
risk: medium
milestone: backlog

# Weather Station Harness Examples

## Summary

- Deliver a Filare-ready harness example for hobby/educational weather stations, starting with SparkFun Weather Shield + rain/wind sensors, and optionally Solar Pi Weather Station.

## Source Assets

- SparkFun Weather Shield hardware files (Eagle) and Fritzing wiring diagrams; sensor pinouts for RJ11/RJ45 anemometer/rain gauge cables.
- Solar Pi Weather Station README with RJ45 bulkhead wiring to wind/rain/temp sensors.

## Connectors & Interfaces

- RJ11/RJ45 field cables for anemometer, wind vane, rain gauge.
- Qwiic/I²C headers for temp/humidity/pressure sensors.
- Power: 5–12 V DC input, LiPo jack, solar panel input.
- MCU header: Arduino footprint (Uno-style) or Raspberry Pi GPIO (Solar Pi variant).

## Real-World Example

- Community weather station builds logged on SparkFun forums and numerous GitHub hobby projects; aligns with “high-community” simple starter use case.

## Work Outline

- Extract pin tables from SparkFun Eagle schematic.
- Model harness with shield-to-sensor cables and optional solar/battery branch.
- Add regression YAML under `tests/rendering/` and minimal HTML/Graphviz renders in `outputs/`.
