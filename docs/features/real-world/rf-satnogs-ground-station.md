uid: FEAT-GENERAL-0005
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: 3d
dependencies: []
risk: medium
milestone: backlog

# RF Ground Station (SatNOGS) Harness

## Summary

- Build a Filare example for a SatNOGS-style ground station: rotator motors, limit switches, RF front-end (LNA/filters), SDR, and control electronics with outdoor/indoor split.

## Source Assets

- SatNOGS rotator hardware docs (CERN OHL) with stepper/driver wiring, limit switch connectors, and BOM.
- SatNOGS RF front-end (LNA/filter) and RTL-SDR cabling guides.
- Network deployment guides showing mast-mounted vs. shack-mounted component wiring.

## Connectors & Interfaces

- Stepper motor drivers to NEMA steppers (4-wire per motor); limit switch wiring.
- Coax runs (SMA/N-type) from antenna to LNA/filter to SDR.
- Power: 12–24 V DC feed to rotator drivers; optional PoE for Raspberry Pi.
- Control: USB to RTL-SDR; GPIO or RS485 between controller and rotator drivers.

## Real-World Example

- Hundreds of SatNOGS community ground stations worldwide publishing observations; open hardware + open data ecosystem.

## Work Outline

- Capture rotator wiring (az/el steppers, limit switches) and power distribution.
- Model coax + DC separation and shielding callouts.
- Provide mast/shack split harness YAML and rendering test.
