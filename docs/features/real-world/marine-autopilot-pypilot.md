uid: FEAT-GENERAL-0006
status: BACKLOG
priority: low
owner_role: FEATURE
estimate: 2d
dependencies: []
risk: medium
milestone: backlog

# Marine Autopilot (pypilot) Harness

## Summary

- Provide a sailboat autopilot harness example based on pypilot: IMU, motor controller, tiller drive, NMEA0183/Seatalk, and power distribution.

## Source Assets

- pypilot hardware guides showing IMU, H-bridge/motor driver wiring, and Seatalk/NMEA connections.
- Community build logs on OpenCPN forums and GitHub forks.

## Connectors & Interfaces

- IMU sensor (I²C/SPI) to Raspberry Pi controller.
- H-bridge to DC motor/tiller drive (2-wire high current) with clutch output.
- NMEA0183/Seatalk serial lines (differential/one-wire) to boat instruments.
- Power: 12 V DC boat supply with fuse block; optional rudder feedback potentiometer analog wiring.

## Real-World Example

- Used on small sailboats by cruisers; modest but active community (~260+ stars, forum users) and fits low-voltage + mixed-signal harnessing.

## Work Outline

- Capture IMU + motor driver wiring and Seatalk/NMEA pin maps.
- Model fused distribution block, motor pair, and serial spurs.
- Add YAML example and rendering regression.
