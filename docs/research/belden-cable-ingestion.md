# Belden Cable Part Number and Specs Ingestion

## Summary

Outlines how to gather Belden cable part numbers and specifications at scale. Direct Belden APIs are not documented in this environment, so the recommended path is to use official distributor APIs (Mouser, Digi-Key, Newark/element14) filtered to Belden cables. Provides curl examples and notes for confirming Belden-first endpoints when available.

## Use Cases for Filare

- Populate a catalog of Belden cables with part numbers, electrical/mechanical specs, and datasheets.
- Feed Filare’s part model with trusted data without manual entry.
- Optionally keep pricing/availability from distributors alongside specs.

## Technical Evaluation

- Direct Belden endpoints: Public API documentation is not available here. Belden’s site exposes product pages and search, but using undocumented endpoints risks breakage and TOS violations. Prefer documented sources.
- Distributor APIs (documented, stable):
  - Mouser: REST API with OAuth; supports manufacturer filter and category filters (e.g., “Wire & Cable”).
  - Digi-Key: REST API with OAuth + locale headers; supports manufacturer filter and family/category for cable.
  - Newark/element14/Farnell: REST product API with API key; region via domain/params; supports manufacturer filtering.
- Data returned (per distributor):
  - MPN (Belden part number), manufacturer (Belden), description, datasheet URL, key specs (gauge, conductor count, shielding, jacket, OD, impedance), lifecycle, RoHS/REACH, pricing/availability.
- Strategy:
  - Use distributor APIs to bulk list all Belden cable SKUs via manufacturer + category filters.
  - Paginate through results; cache locally.
  - If a Belden-official feed/API is found, map it into the same ingestion adapter, but keep distributor path as baseline.

## Complexity Score (1–5)

3 — Requires API auth, pagination, filtering, and mapping to Filare’s part model; avoids scraping risk.

## Maintenance Risk

- Distributor APIs are stable but may change auth/version; keys and rate limits apply.
- Belden direct endpoints (if used) could be undocumented; mitigate by relying on distributors first.

## Industry / Business Usage

- PLM/ERP and sourcing tools commonly pull manufacturer data from distributor APIs for completeness and availability.

## Who Uses It & Why It Works for Them

- Procurement/engineering: need authoritative part numbers/specs plus availability/pricing for Belden cables.
- QA/Service: need datasheets and consistent IDs for replacements.

## Feasibility

- Feasible now via distributor APIs; add optional Belden-first adapter if official docs/keys are available.

## Required Work

- REWORK tasks: Define ingestion adapter interface and mapping to Filare’s part model for cables (gauge, conductor count, shield, impedance, OD, jacket, approvals).
- FEATURE tasks: Implement distributor adapters (Mouser, Digi-Key, Newark) with manufacturer/category filters for Belden cables; pagination; caching.
- TOOLS tasks: CLI to fetch/update Belden cable catalog; handle locale selection per distributor.
- DOCUMENTATION tasks: How to obtain API keys, set region, and run ingest; mapping of fields to Filare part schema.
- COVERAGE tasks: Mocked tests with sample API responses; ensure filters and pagination work; validate field mapping.

## Recommendation

ADOPT_LATER — Start with distributor APIs (Mouser/Digi-Key/Newark) to enumerate Belden cables; add Belden-official adapter only if documented endpoints/keys are secured.

## References

- Mouser API docs (product search).
- Digi-Key API docs (product search).
- Newark/element14/Farnell product API docs.
- Belden product catalog (for manual verification of MPNs/specs).

## Optional Appendix

- Mouser (Belden cables; assumes `MOUSER_API_KEY`):

  ```bash
  curl -X POST "https://api.mouser.com/api/v1/search/partnumber?apiKey=${MOUSER_API_KEY}" \
    -H "Content-Type: application/json" \
    -d '{
      "SearchByKeywordRequest": {
        "keyword": "Belden cable",
        "records": 50,
        "startingRecord": 0,
        "searchOptions": "string",
        "searchWithYourSignUpLanguage": "EN"
      }
    }'
  ```

  For full enumeration, use the keyword `"Belden"` with a category filter if supported (e.g., `"Wire & Cable"`) and paginate `startingRecord`.

- Digi-Key (Belden manufacturer filter; assumes OAuth access token and locale):

  ```bash
  curl -X GET "https://api.digikey.com/Search/v3/Products" \
    -H "Content-Type: application/json" \
    -H "X-DIGIKEY-Client-Id: ${DIGIKEY_CLIENT_ID}" \
    -H "Authorization: Bearer ${DIGIKEY_TOKEN}" \
    -H "X-DIGIKEY-Locale: {\"Country\":\"US\",\"Language\":\"en\",\"Currency\":\"USD\"}" \
    --data-urlencode "manufacturer=Belden" \
    --data-urlencode "category=Wire & Cable" \
    --data-urlencode "page=0" \
    --data-urlencode "pageSize=50"
  ```

  Adjust `page/pageSize` to iterate through all results; set locale for desired region/currency.

- Newark/element14 (manufacturer filter; assumes API key and region):
  ```bash
  curl "https://api.element14.com/catalog/products" \
    --get \
    --data-urlencode "term=manu:Belden" \
    --data-urlencode "category=wire%20and%20cable" \
    --data-urlencode "results=50" \
    --data-urlencode "offset=0" \
    --data-urlencode "callInfo.apiKey=${NEWARK_API_KEY}" \
    --data-urlencode "storeInfo.country=US" \
    --data-urlencode "storeInfo.language=en" \
    --data-urlencode "storeInfo.currency=USD"
  ```
  Increment `offset` for pagination; switch `country/currency` for region choice.
