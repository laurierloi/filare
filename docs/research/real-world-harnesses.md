# Real-World Harness References (research snapshot — 2025-12-18)

Goal: identify open-source hardware/software projects with wiring harnesses or cabling layouts that Filare could model as reference examples. Each entry lists where harness assets live, license, and signs of community size.

## Automotive / Mobility

- **Speeduino (DIY ECU, cars & motorcycles)** — Open-source Arduino-based ECU with published schematics/PCB and loom pin-outs in the repo wiki; GPL-2.0, 600+ forks and ~1k installs claimed. Harnesses: wiring diagrams in `wiki` and community PCB/BOMs (e.g., PCBWay build). citeturn3search5turn3search3
- **OpenXC Vehicle Interface (Ford reference dongle)** — CC BY 4.0 hardware design plus firmware under BSD-style license; documentation includes full connector pin-out for OBD-II, dual CAN, 12V accessory output. Good fit for Filare CAN/automotive examples and bus (OBD-II) harnesses. citeturn4search0turn4search10
- **openpilot (Comma.ai driver-assist)** — MIT-licensed ADAS stack supporting 325+ car models and 10k+ users; requires car-specific “harness” cables that map OEM camera/ECU connectors to the comma device (pin-outs documented per vehicle). citeturn3search17

## Marine / Boats

- **pypilot (sailboat autopilot)** — GPLv3 free software with Raspberry Pi-based controller; docs show mounting and connector layout for IMU, motor controller, and NMEA0183/Seatalk wiring. Community: 260+ GitHub stars, active OpenCPN plugin users. citeturn8search3turn6view0turn3search11

## Aviation / Drones

- **PX4 Autopilot** — BSD-3 open-source flight stack with airframe-specific wiring diagrams (power distribution, servo buses, telemetry, GPS). Broad community via Dronecode and many vehicle types (fixed-wing, VTOL, rover, boat). citeturn3search13
- **ArduPilot** — GPLv3 autopilot covering aircraft/rover/boat; abundant community wiring examples for Pixhawk-class harnesses (power, RC, telemetry). citeturn3search14

## RF / Ground Stations

- **SatNOGS Ground Station** — Software GPLv3+/AGPL + hardware under CERN OHL; OSHWA-certified rotator with BOM and cabling for stepper drivers, LNAs, SDR, and rotor control. Global open network with public observation data (CC BY-SA). Harness diagrams in rotator docs. citeturn3search12turn3search10turn3search7turn3search4

## Data Center / Computers

- **Open Compute Project – Open Rack (ORv2/ORv3)** — Open specifications (OCPHL) for 21” racks with rear busbar power harnessing, blind-mate power shelves, and cable-routing rules; specs and CAD hosted on OCP wiki. Candidate for Filare to showcase high-power busbar + DC cable assemblies. citeturn4search8turn4search11

## Musical / Audio Systems

- **OpenDeck (modular MIDI controllers)** — Apache-2.0 firmware plus open hardware reference boards; wiring uses JST headers for encoders/LEDs/pots with YAML-like board descriptors. Good small-scale harness example (USB + low-voltage signal bundles). citeturn4search3

## Weather Stations / Raspberry Pi & Arduino

- **SparkFun Weather Shield** — Open-source Arduino shield with Eagle hardware files and Fritzing wiring examples; sensors plug via RJ11/RJ45 to anemometer/rain gauge, making a tidy environmental harness reference. License in repo (SparkFun open-source hardware). citeturn9view0
- **Solar Pi Weather Station** — GPL-2.0 Raspberry Pi design using RJ45 bulkhead connectors to field sensors (wind, rain, temp); detailed wiring in README. citeturn5search2

## Industrial Control / ICS

- **OpenPLC (IEC 61131-3 runtime + community hardware builds)** — MIT-licensed PLC runtime used on Raspberry Pi/Arduino/netPI; community publishes wiring for digital/analog I/O and RS485/Modbus links. Active forum and academic users. citeturn0search0turn0search8turn0search5
- **Industrial Shields Arduino/Raspberry PLCs** — Open-source-hardware DIN-rail PLCs with pluggable screw terminals for 24 V IO, dual RS485/RS232, Modbus RTU/TCP, Ethernet; documentation and datasheets list connector pinouts. Large maker/industrial community and commercial support. citeturn0search1turn0search3turn0search7
- **OpenDINRail I/O module** — OSHW DIN-rail 24 V input/output board with side connector for daisy-chaining modules; screw-terminal rows for field wiring and isolations. Community PCB on PCBWay links to GitHub with schematics/BOM. citeturn0search4

## Notes for Filare adoption

- Prioritize **CAN/OBD-II** (OpenXC, Speeduino, openpilot) and **RF ground-station** (SatNOGS) examples—they feature multi-connector harnesses, shielding, and power-signal separation that map cleanly to Filare schema.
- Use **SparkFun/Weather** and **OpenDeck** as compact starter examples: low-voltage, few connectors, clear licenses, and published PCB + cabling images.
- For heavy-power scenarios, an **OCP Open Rack** example would demonstrate busbar + branch-circuit modeling, expanding Filare to data-center audiences.
