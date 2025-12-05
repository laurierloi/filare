# Part Ingestion Project Plan

## Goals

- Build an optional, adapter-based part ingestion tool to pull manufacturer/distributor data (MPN, specs, datasheets, lifecycle, pricing/availability, alternates) into Filare’s part model.
- Support region-aware distributor queries and manufacturer detail lookups without breaking offline workflows.
- Provide CLI/automation to fetch/update a local cache, keeping design files free of transient pricing while enabling enriched BOMs.

## Requirements

- Interfaces
  - CLI commands to fetch/update parts by MPN or by query (manufacturer + category).
  - Configurable preferred distributor (Mouser, Digi-Key, Newark/element14) and region (country, currency, language).
  - Optional manufacturer lookups (Molex, Samtec; Belden via distributor) for specs/datasheets when distributor data is insufficient.
  - Output mapped to Filare’s part model (common fields + type-specific attributes) with supplier lists and alternates.
  - Local cache (file/DB) to store fetched data; design files reference stable part IDs.
  - Dry-run and diff/report modes to review changes before applying to caches.
- Behavior
  - Use official APIs (OAuth/API keys); avoid scraping.
  - Graceful handling of missing keys/network: tool is optional; core workflows stay offline-safe.
  - Rate-limit friendly: caching, pagination, backoff/retry.
  - Locale-aware pricing/availability; specs/datasheets captured regardless of locale.
  - Mapping layer normalizes distributor/manufacturer responses into Filare’s schema; preserves source URLs and timestamps.
- Data scope
  - Fields: pn/mpn, manufacturer, description, datasheet URL, lifecycle/rohs/reach, specs (type-specific), suppliers with price/qty/stock/lead/currency, alternates if provided.
  - No bulk redistribution of pricing; store only as local cache; avoid embedding in versioned design files unless configured.
- Security & Config
  - API keys via env/config; never committed.
  - Per-user/per-project config for preferred distributor/region and cache location.

## Phases and Steps

- Phase 0: Foundations
  - Define part model mapping (from ingestion to Filare schema).
  - Specify config format (distributor preference, region, API keys, cache path).
  - Choose cache store (JSON/SQLite) and schema.

- Phase 1: Distributor Adapters (baseline)
  - Implement Mouser adapter (OAuth API): search by MPN, by keyword with manufacturer filter; pagination; map to part model.
  - Implement Digi-Key adapter (OAuth + locale headers): search by MPN/category/manufacturer; map specs, pricing, availability.
  - Implement Newark/element14 adapter (API key + region params): search by MPN/manufacturer/category; map to part model.
  - Add CLI commands: `parts fetch --mpn ...`, `parts search --manufacturer ... --category ...`.
  - Add caching and rate-limit/backoff.

- Phase 2: Manufacturer Adapters (spec-first)
  - Molex adapter (product/details APIs) for specs/datasheets; fallback to distributors for pricing.
  - Samtec adapter for specs/datasheets; optional key.
  - Belden via distributor data (unless official API secured).

- Phase 3: Enrichment & Alternates
  - Normalize alternates/substitutes when provided by APIs; store with source.
  - Add lifecycle/rohs/reach normalization.
  - Optional URL checker for datasheets/manufacturer links.

- Phase 4: Integration with Filare Outputs
  - Provide CLI to export cache entries into Filare-friendly artifacts (e.g., JSON library, YAML snippet).
  - Update docs on linking design YAML to cached part IDs without embedding pricing.
  - Optional BOM enrichment step that merges cached supplier data when generating outputs (behind a flag).

- Phase 5: UX & Ops
  - Add diff/report mode to review cache updates.
  - Add per-source enable/disable flags; graceful degradation when keys/online not present.
  - Provide examples for region selection (country/currency) per distributor.

## Hints and Implementation Notes

- Keep adapters isolated; version their API interactions; mock responses for tests.
- Use a normalization layer to map differing field names into a common part schema.
- Treat pricing as volatile: cache with timestamp; default to omit from committed artifacts.
- Prefer pagination over large page sizes; respect distributor rate limits.
- Make region configurable per command; default to project config.
- Avoid schema churn by keeping the ingestion output a superset mapped onto Filare’s part model; stash extra fields under `source_data` if needed.

## Validation

- Mocked integration tests per adapter (sample responses).
- CLI tests for fetch/search, caching, locale handling, and diff/report.
- Manual spot checks against known MPNs from Molex, Belden, Samtec, and distributor queries.
