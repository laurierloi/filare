# Vendor Parts Ingestion (Manufacturers & Distributors)

## Summary

Explores how Filare could automatically gather part data from manufacturers (Molex, Belden, Samtec) and distributors (Mouser, Digi-Key, Newark), with options to select distributor site/region. Covers data sources, access patterns, and considerations for common manufacturers.

## Use Cases for Filare

- Enrich BOMs with live metadata (MPN, specs, datasheet URL, lifecycle) without manual entry.
- Pull supplier-specific pricing/availability for selected regions or channels.
- Offer alternates and family links from upstream catalogs.

## Technical Evaluation

- Manufacturers:
  - Molex: Public APIs and part pages; `services.ips.molex.com` API used by their site; datasheets on `www.molex.com`; parametric search endpoints; CSV exports via MyMolex (account).
  - Belden: Product catalog with specs and datasheets; APIs are limited; scraping risks TOS; better via distributor data for Belden SKUs.
  - Samtec: `api.samtec.com` and `samtec.com/api` endpoints for product specs and parametric filters; often require API key; datasheets on product pages.
- Distributors (preferred for availability/pricing):
  - Mouser: Official REST API (OAuth) with product search/details, pricing, availability, lifecycle; region parameter (e.g., `countryCode`).
  - Digi-Key: REST API with OAuth (Client Credentials + Signed requests) for product search, pricing, availability, lifecycle; supports region via locale and currency parameters.
  - Newark (element14): APIs vary by region (Newark/Farnell/element14); REST product search/details with API key; region selection via domain (newark.com/us, farnell.com/uk) and `country`/`currency` params.
- Access patterns:
  - Prefer official REST APIs (Mouser, Digi-Key, Newark/element14, Samtec, Molex) to avoid scraping and TOS issues.
  - Use manufacturer pages for datasheet URLs when distributor data lacks them.
  - Cache part metadata locally to reduce rate-limit impact and avoid hammering APIs.
- Region selection:
  - Mouser: `countryCode` and `currency` in API request.
  - Digi-Key: `X-DIGIKEY-Locale` (country, language, currency) headers.
  - Newark/Farnell/element14: domain + `country`/`currency` params.
  - Store preferred distributor/region in Filare config to choose which API and locale to call.
- Common fields obtainable:
  - MPN, manufacturer, descriptions, lifecycle, RoHS/REACH, datasheet URL.
  - Electrical/mechanical specs (pin count, gauge range, impedance, shield, temp rating).
  - Pricing by quantity break, currency, MOQ, lead time; stock/availability.
  - Suggested alternates (some distributors return substitutes).
- Data freshness and licensing:
  - APIs often require terms acceptance; usage may be rate-limited and intended for sourcing, not bulk redistribution.
  - Avoid storing bulk distributor pricing in public artifacts; fetch on demand or cache privately.

## Complexity Score (1–5)

4 — Requires API authentication flows, per-distributor schemas, caching, locale handling, and error/rate-limit management.

## Maintenance Risk

- APIs change and may need re-registration/keys; keep adapters versioned and optional.
- Regional differences (domains, currencies) can break naive clients; test per locale.
- Scraping is fragile; favor official APIs.

## Industry / Business Usage

- Procurement and PLM tools integrate distributor APIs (Mouser/Digi-Key) for pricing and stock; engineering teams pull specs from manufacturer APIs (Samtec/Molex) for parametric selection.

## Who Uses It & Why It Works for Them

- Procurement: needs pricing/availability in the correct region/currency.
  +- Engineering: needs specs, datasheets, and lifecycle direct from manufacturer.
- Service: needs reliable links to datasheets and replacement alternates.

## Feasibility

- Feasible if kept optional and adapter-based (per distributor/manufacturer), with config for region and API keys; avoid mandatory network calls for core Filare use.

## Required Work

- REWORK tasks: Define part ingestion abstraction (adapters per source) and caching strategy; config for preferred distributor/region.
- FEATURE tasks: Implement adapters for Mouser, Digi-Key, Newark (distributors); Molex/Samtec manufacturer detail endpoints; optional Belden via distributor data; map responses into Filare part model; allow alternates from API where present.
- TOOLS tasks: CLI to fetch/refresh part metadata into local cache; API key management; retry/rate-limit handling.
- DOCUMENTATION tasks: Setup guides for API keys, region selection, and usage examples; note TOS and caching practices.
- COVERAGE tasks: Mocked integration tests per adapter; fixtures for sample API responses; ensure locale handling.

## Recommendation

ADOPT_LATER — Build optional adapters for major distributors/manufacturers with region-aware requests and caching; keep network and API keys optional so core flows remain offline-safe.

## Models (Ingestion)

- Config:
  - `preferred_distributor` (mouser|digikey|newark/element14|none), `region` (country, currency, language), API keys per source.
  - Fallback order for lookups (manufacturer first, then distributor, or vice versa).
- Adapter output (mapped to Filare part model):
  - `mpn`, `manufacturer`, `description`, `datasheet_url`, `lifecycle`, `rohs/reach`.
  - Specs (as provided: pin count, gauge range, impedance, temp rating, etc.).
  - `suppliers`: list with price breaks, currency, stock, lead time, URL, supplier SKU.
  - `alternates`: when returned by API.

## Sources and Notes

- Molex: product API (`services.ips.molex.com`), datasheets on `www.molex.com`; may need account/key.
- Samtec: `api.samtec.com` (keyed); product details and parametric filters.
- Belden: limited API; rely on distributor data when possible; use datasheet links from manufacturer site if needed.
- Mouser: official REST API (OAuth); supports country/currency; returns pricing, availability, lifecycle, datasheet.
- Digi-Key: REST API (OAuth + signed); locale headers; returns pricing, availability, lifecycle, specs.
- Newark/element14/Farnell: REST product API (API key); region via domain/country/currency; returns pricing, availability, datasheet, alternates.

## Optional Appendix

- Region handling examples:
  - Mouser: `countryCode=CA`/`US`, `currency=USD/CAD`.
  - Digi-Key: `X-DIGIKEY-Locale: {Country: CA, Language: en, Currency: CAD}`.
  - Newark vs Farnell vs element14: switch domain and set `country=US/UK/SG`, `currency=USD/GBP/SGD`.
