# Paginate titlepage BOM when large

## Category
FEATURE

## Evidence
- The titlepage currently embeds the full BOM on the first page, which overflows when many items are present. There is no automatic pagination to a separate page.

## Suggested Next Steps
- Add a threshold (default 30 rows) to split the titlepage BOM into a dedicated page when the BOM exceeds that size.
- Ensure split BOM pages integrate with existing pagination/lettered suffix behavior and are reflected in the index table.
- Provide a harness option to override the threshold.
- Add regression coverage with a sample exceeding the threshold.
