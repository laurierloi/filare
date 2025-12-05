from: docs/research/vendor-parts-ingestion.md

# Octopart Ingestion (Filare-Relevant Categories)

## Status
PROPOSED

## Priority
Low

## Summary
Add an optional Octopart-based ingestion path to fetch parts relevant to Filare (connectors, terminals/crimps, cables, wires, sheathes/coverings, test equipment/tools, terminations), avoiding full-catalog pulls. Map results into the Filare part model with supplier/pricing info where available.

## Motivation
Octopart aggregates manufacturer and distributor data with a stable API; filtering to Filare-relevant categories reduces noise and bandwidth while enriching harness BOMs.

## Affected Users / Fields
- Harness engineers and procurement needing authoritative MPNs/specs/datasheets for Filare parts without per-distributor queries.

## Scope
- Octopart adapter (keyed API) limited to targeted categories and/or manufacturers.
- CLI to search/fetch by MPN or by filtered category (connectors/crimps/cables/wires/sheathes/tools/terminations).
- Mapping to Filare part model (common + type-specific fields); optional supplier/pricing capture in cache.

## Out of Scope
- Pulling non-Filare categories (semiconductors, passives, etc.).
- Embedding pricing in committed design files (keep in cache).

## Requirements
- API key via config/env; optional feature (offline safe).
- Category/keyword filters to restrict to harness-relevant parts.
- Pagination and rate-limit handling; local cache of results.
- Normalization layer to Filare part schema (including supplier offers where allowed).

## Steps
- [ ] Define category filters/queries for Filare scope (connectors, terminals/crimps, cables, wires, sheathes/coverings, tools/test equipment, terminations).
- [ ] Implement Octopart adapter: search by MPN; search by filtered category/keyword; paginate; map fields to Filare part model.
- [ ] Add CLI commands: `parts fetch --mpn ... --source octopart`, `parts search --source octopart --category connectors`.
- [ ] Add caching and rate-limit/backoff; avoid storing pricing in VCS.
- [ ] Document setup (API key), filters, and examples.
- [ ] Add mocked tests with sample Octopart responses and mapping.

## Progress Log
- PROPOSED — Feature defined from parts ingestion research.

## Validation
- Mocked responses for MPN lookup and category search; verify mapping to Filare schema and filter behavior.

## Dependencies / Risks
- Requires Octopart API key and adherence to terms; rate limits apply.
- Category taxonomy may differ; need resilient filters and keyword fallbacks.
