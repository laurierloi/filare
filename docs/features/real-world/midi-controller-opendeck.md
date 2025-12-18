uid: FEAT-GENERAL-0008
status: BACKLOG
priority: low
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: low
milestone: backlog

# MIDI Controller (OpenDeck) Harness

## Summary

- Provide a small, low-voltage harness example for OpenDeck-based DIY MIDI controllers: encoders, buttons, LEDs, and USB-MIDI interface.

## Source Assets

- OpenDeck hardware reference boards and wiki pin tables (JST headers for inputs/outputs, WS2812 support).
- Community build guides for arcade-button and fader controllers.

## Connectors & Interfaces

- JST-XH/GH headers for digital inputs (buttons/encoders) and LED outputs.
- USB micro/USB-C for MIDI device connection.
- Optional DIN-5 MIDI OUT/THRU ports.
- Power: 5 V from USB; optional external 5–9 V barrel for LED strips.

## Real-World Example

- Active maker community building custom controllers; good small-scale harness to demonstrate Filare without high current.

## Work Outline

- Capture header pin maps for OpenDeck 32u4/STM32 boards.
- Model harness with grouped JST cables and optional DIN-5 breakout.
- Add YAML example and rendering regression.
