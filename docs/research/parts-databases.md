# Parts Databases and Catalog Sources

## Summary
Survey of existing parts databases that could feed a Filare part-ingestion tool. Focus on sources with downloadable or API-accessible data, plus tool-specific catalogs that may require manual export/conversion. Notes include access steps and licensing considerations.

## Candidates
- **EPLAN Data Portal**
  - Content: Electrical/mechanical parts (connectors, relays, cables, etc.) with rich metadata and symbols/macros.
  - Access: Requires EPLAN account and license; exports typically via EPLAN (XML/EDZ); conversion to Filare would need a script to map EPLAN fields to Filare part model.
  - Notes: Licensing restrictive; use for internal conversions only.
- **TraceParts**
  - Content: 3D models and metadata for many manufacturers (including connectors, hardware).
  - Access: Free account; downloads in STEP/IGES + CSV where available. Batch download may require manual selection; API access is limited and may need commercial agreement.
  - Conversion: Use CSV/Excel exports (where provided) to map into Filare; 3D models optional for mechanical references.
- **Octopart**
  - Content: Aggregated distributor/manufacturer data (specs, datasheets, offers).
  - Access: Official REST API (API key); supports manufacturer/distributor filters; JSON responses.
  - Conversion: Direct mapping to Filare part model via an adapter; honor API terms and rate limits.
- **SnapEDA**
  - Content: ECAD symbols/footprints and basic part metadata.
  - Access: Free account; API available (partner/commercial); web downloads per part.
  - Conversion: Use API (if permitted) or CSV export (via BOM upload) to pull metadata; beware TOS for bulk use.
- **Ultra Librarian**
  - Content: ECAD models and parametric data for many parts.
  - Access: Account required; downloads per part; API is commercial.
  - Conversion: Possible via BOM upload/export; scripting required; check licensing for redistribution.
- **ComponentSearchEngine / SamacSys**
  - Content: ECAD models and parametrics.
  - Access: Free/paid; some APIs for partners; otherwise per-part download.
  - Conversion: Similar to Ultra Librarian; use BOM upload workflow to extract CSV when allowed.
- **Mouser / Digi-Key / Newark APIs**
  - Content: Distributor catalogs with specs, datasheets, pricing/availability.
  - Access: Official APIs with keys/OAuth; region selectable.
  - Conversion: Best fit for automated ingestion; map JSON to Filare part schema; cache locally.
- **Altium 365 Manufacturer Part Search (MPS)**
  - Content: Aggregated part data and supplier links.
  - Access: Within Altium ecosystem; no open API for bulk external use.
  - Conversion: Not recommended unless using Altium server-side exports; licensing constraints.
- **KiCad libraries with linked parametrics**
  - Content: Symbols/footprints; limited parametric data.
  - Access: Git repositories; open source.
  - Conversion: Good for footprints, but parametrics thin; supplement with distributor APIs.
- **Open Parts Libraries (e.g., PartKeepr datasets, open BOM repos)**
  - Content: Community-curated parts with varying quality.
  - Access: Public repos/exports.
  - Conversion: Feasible via CSV/JSON import; validate field quality manually.

## Manual Steps / Access Notes
- EPLAN: Export EDZ/XML from licensed EPLAN session; run a converter to map fields (MPN, manufacturer, description, electrical/mechanical specs) to Filare part model; remove proprietary symbol data unless permitted.
- TraceParts: Use account to filter by manufacturer/category; download CSV if available; otherwise scrape with caution (check TOS). Map parametrics; link STEP as optional mechanical reference.
- Octopart: Obtain API key; use REST queries filtered by manufacturer/category; cache responses to respect rate limits/TOS.
- SnapEDA/Ultra Librarian/ComponentSearchEngine: If API access granted, pull parametrics; otherwise use BOM upload/export workflows to obtain CSVs; check licensing for bulk/redistribution.
- Distributor APIs (Mouser/Digi-Key/Newark): Obtain keys; select region/currency; paginate results; cache locally; prefer these for specs/datasheets/pricing.
- Open libraries: Pull CSV/JSON; clean/normalize fields; supplement with trusted sources for missing specs.

## Recommendation
- Primary automated sources: Distributor APIs (Mouser/Digi-Key/Newark) and Octopart API (if licensed).
- Secondary/manual sources: EPLAN exports (for internal use), TraceParts CSV, SnapEDA/Ultra Librarian via permitted exports.
- Always respect TOS/licensing; keep ingestion adapters optional and cache results locally.
