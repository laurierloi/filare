# Vendor and Manufacturer Parts Integration

## Summary
Explores how to represent and integrate manufacturer/supplier parts in Filare so harness BOMs can carry rich metadata (technical attributes, sourcing, pricing, alternates, families). Covers common part types (connectors, terminals/crimps, tools, wires/cables, coverings, labels, protection) and suggests fields to track per type.

## Use Cases for Filare
- Generate procurement-ready BOMs with manufacturer/supplier links, pricing, and approved alternates.
- Validate part compatibility (wire gauge to terminal, connector family to accessories).
- Support service/field teams with consistent part IDs, datasheets, and ordering links.
- Enable future inventory overlays (stock counts, preferred supplier) without breaking schema.

## Technical Evaluation
- Part types to model:
  - Connectors (housings, genders, pin count, family, accessories/back-shells).
  - Terminals/crimps and seals/plugs (wire gauge range, plating, tool spec).
  - Tools (crimp tools, applicators, extraction tools).
  - Wires (single conductor): gauge, insulation, color, stranding, temp rating, voltage rating, roll length, OD, approvals.
  - Cables (bundles): wire count, color map, shield/twist/grouping, impedance/spec (Ethernet, SpaceWire, CameraLink), jacket, bend radius, OD.
  - Coverings: conduit/braid/tape/heat-shrink, ID/OD range, shrink ratio, temp rating.
  - Labels/markers: size, material, printable format.
  - Protection: fuses/breakers inline; boots/backshells; grommets.
  - Families/kits: connector families (D-sub, MicroFit, Deutsch), matched terminals/seals, accessory sets.
- Common fields (core):
  - `category`, `type/subtype`, `family`.
  - `pn`, `mpn`, `manufacturer`, `datasheet_url`, `description`.
  - Supplier entries: `supplier`, `spn`, `url`, `price`, `currency`, `qty_break`, `moq`, `lead_time`.
  - `alternates`: list of equivalent `mpn`/supplier refs with notes.
  - `notes`, `status` (active/EOL/NRND), `lifecycle_source`.
- Technical fields by type:
  - Connectors: `pin_count`, `gender`, `keying`, `mount` (panel/in-line), `termination` (crimp/solder/poke), `accessories` (backshell/boot/cap), `family`, `seal_rating`, `temp_rating`, `current_rating`, `voltage_rating`, `mating_cycles`.
  - Terminals/seals/plugs: `wire_gauge_range`, `material/plating`, `insulation_support`, `crimp_tool`, `extraction_tool`, `seal_size`, `cavity_family`.
  - Tools: `tool_type` (crimp/applicator/extractor), `compatible_families`, `gauge_range`, `die/locator`.
  - Wires: `gauge` (AWG/mm2), `stranding`, `color`, `insulation_material`, `temp_rating`, `voltage_rating`, `outer_diameter`, `roll_length`, `standards` (UL/ISO), `shield` (bool/type/drain).
  - Cables: `wire_count`, `colors`, `twist` (pairing), `shield` (type/coverage/drain), `impedance`, `category/protocol` (Ethernet Cat5e/Cat6, SpaceWire, CameraLink), `jacket_material`, `outer_diameter`, `min_bend_radius`, `length_unit`, `approval`.
  - Coverings: `inner_diameter`, `outer_diameter`, `shrink_ratio`, `temp_rating`, `material`, `color`, `length_unit`.
  - Labels: `size`, `material`, `adhesive`, `print_method`.
  - Protection/accessories: `current_rating` (fuse/breaker), `ingress` (cap/boot), `backshell_thread`, `grommet_size`.
- Data links:
  - URLs: `datasheet_url`, `manufacturer_url`, `supplier_urls` (list with price/qty).
  - Families/aliases: `family`, `series`, `accessories` referencing other part records.
  - Alternates: list with `mpn`, `manufacturer`, `supplier` entry, `notes`.
- Pricing:
  - Optional per supplier: `price`, `currency`, `qty_break`/`moq`, `lead_time`.
  - Keep as informational; avoid computations in core schema.
- Inventory (optional future):
  - Separate overlay: `location`, `on_hand`, `lot`, `expires`, `reserved`; keep out of core part definition to avoid coupling usage with stock.

## Complexity Score (1–5)
3 — Adds structured part metadata and supplier/alternate links; schema extensions and BOM rendering changes are needed but no deep architectural change.

## Maintenance Risk
- Part data changes often (pricing/availability); risk mitigated by treating supplier info as optional and by allowing alternates.
- Families and compatibility tables need maintenance but change slowly.
- URL rot; need permissive handling when links are absent.

## Industry / Business Usage
- OEM and supplier BOMs list MPN, supplier SKU, alternates, pricing breaks, lifecycle status.
- Harness teams track gauge/tool compatibility for crimps and terminals.
- Procurement/service need datasheet links and clear family naming (e.g., D-sub, MicroFit, Deutsch DT/DRC).

## Who Uses It & Why It Works for Them
- Procurement: sourcing links, alternates, pricing.
- Manufacturing/QA: crimp/tool compatibility, gauge ranges, accessories.
- Service: clear part IDs, families, and URLs for replacements.

## Feasibility
- Feasible as optional part metadata extensions and richer `additional_components`/BOM rendering; inventory can stay a separate overlay.

## Required Work
- REWORK tasks: Define part data model (common fields + type-specific attributes); align with existing BOM/additional_components shape.
- FEATURE tasks: Extend schema to accept part metadata and alternates; add supplier list support; display key fields in BOM and HTML outputs; allow part families/aliases.
- TOOLS tasks: Optional part library ingestion (CSV/JSON) and validation for compatibility (gauge vs terminal); optional URL checker.
- DOCUMENTATION tasks: Syntax examples for part metadata, alternates, supplier/pricing fields; guidance on families and accessories.
- COVERAGE tasks: Regression YAMLs with parts spanning connectors, terminals, wires, cables, coverings, and alternates; verify BOM output.

## Recommendation
ADOPT_LATER — Add optional part metadata, supplier/alternate fields, and families, keeping inventory as a future overlay.

## Models (Suggested)
- Core Part Model:
  - `category`, `type/subtype`, `family/series`, `pn/mpn/manufacturer`, `description`, `datasheet_url`, `manufacturer_url`, `status/lifecycle`.
  - Supplier list: `[ {supplier, spn, url, price, currency, qty_break, moq, lead_time} ]`.
  - `alternates`: `[ {mpn, manufacturer, supplier?, spn?, notes} ]`.
  - `notes`.
- Type-specific extensions:
  - Connector: `pin_count`, `gender`, `keying`, `mount`, `termination`, `seal_rating`, `temp_rating`, `current_rating`, `voltage_rating`, `mating_cycles`, `accessories`.
  - Terminal/Seal/Plug: `wire_gauge_range`, `material/plating`, `insulation_support`, `crimp_tool`, `extraction_tool`, `seal_size`, `cavity_family`.
  - Tool: `tool_type`, `compatible_families`, `gauge_range`, `die/locator`.
  - Wire: `gauge`, `stranding`, `color`, `insulation_material`, `temp_rating`, `voltage_rating`, `outer_diameter`, `roll_length`, `standards`, `shield`.
  - Cable: `wire_count`, `colors`, `twist/pairs`, `shield` (type/coverage/drain), `impedance`, `protocol/category`, `jacket_material`, `outer_diameter`, `min_bend_radius`, `length_unit`.
  - Covering: `inner_diameter`, `outer_diameter`, `shrink_ratio`, `temp_rating`, `material`, `color`, `length_unit`.
  - Label: `size`, `material`, `adhesive`, `print_method`.
  - Protection/accessory: `current_rating`, `ingress`, `backshell_thread`, `grommet_size`.
- Correlations:
  - Connectors ↔ terminals/seals via `family/cavity_family`.
  - Terminals ↔ wires via `wire_gauge_range`.
  - Accessories (backshells/boots/grommets) ↔ connectors via `family/thread`.
  - Protocol cables ↔ logical signals via `protocol/category`.

## References
- Typical OEM/Supplier BOM fields (MPN, supplier SKU, lifecycle, alternates, pricing).
- Crimp/terminal selection guides (gauge/tool compatibility).
- Ethernet/SpaceWire/CameraLink cable specs (impedance, shielding, twist).

## Optional Appendix
- Inventory overlay suggestion: keep `inventory` as a separate dataset keyed by part id (location, on_hand, lot, expires) to avoid coupling stock with design files.
