# DIN Standards Alignment for Filare Drawings

## Summary

Survey relevant DIN/EN ISO drawing standards (e.g., DIN 6771/823, EN ISO 5457, DIN 15/EN ISO 128 line weights, DIN 406/5 title blocks) to identify required elements for wiring/harness documents. Provide a verification matrix mapping each expected element to current Filare support and gaps.

## Use Cases for Filare

- Producing harness documentation that can be filed in engineering change packages requiring DIN/EN ISO compliance (sheet sizes, borders, title blocks, revision stamps).
- Ensuring generated SVG/HTML/PDF can be printed on standardized formats (A0–A4) with correct margins and fold lines.
- Aligning title blocks, revision history, and projection symbols with supplier/manufacturer expectations in Europe (DIN-heavy ecosystems).
- Making line weights, symbol usage, and annotations acceptable for auditors who reference DIN/EN ISO drawing practices.

## Technical Evaluation

- Features expected by DIN/EN ISO drawing standards (core references: EN ISO 5457/DIN 823 for sheet sizes and margins; DIN 6771 for wiring diagrams; EN ISO 7200 for title blocks; EN ISO 128/DIN 15 for line weights; DIN 406 for text fields; DIN 1986/EN 60617 for symbols when electrical is involved):
  - Sheet formats: A0–A4 sizes, orientation, fixed margins, frame/border, folding marks.
  - Title block: document title, drawing number, revision, date, author/checker/approver, scale, sheet count, projection method, company name/address.
  - Revision table: revision identifier, date, description, approvals.
  - Scale and units: metric default, explicit note if non-metric.
  - Projection symbol (first/third angle), surface finish/weight where relevant.
  - Line types/weights: consistent line hierarchy (visible, hidden, center, cutting plane) with minimum weights (e.g., 0.18–0.70 mm) per DIN 15/EN ISO 128.
  - Grid, coordinate references, and legends for symbols/colors.
  - Page numbering: sheet number / total sheets in a consistent field.
  - Notes/metadata: material, environmental class, standards referenced.
  - Folding marks and print-safe areas.
- Strengths in Filare:
  - Uses DIN-derived canvas sizes and margins in examples (e.g., demo files reference DIN 823/6771/EN ISO 5457).
  - Title block and sheet/page numbering features exist (title block templates, pagination issues filed).
  - Color codes and symbol metadata exist via YAML (can be surfaced in legends).
- Weaknesses:
  - No explicit enforcement of title-block fields per EN ISO 7200 (author/approver/scale/projection).
  - Line weights/styles are not parameterized to DIN 15/EN ISO 128.
  - Folding marks and projection symbols are not systematically generated.
  - Revision table support is unclear; no dedicated revision block.
  - Verification tooling against DIN elements is absent.
- Limitations:
  - Some standards are licensed; we rely on public summaries and domain knowledge.
  - Exact numeric margins/line weights must be confirmed against official texts.
- Compatibility:
  - Filare’s templating and output (SVG/HTML) can host these elements without schema breaks; changes likely confined to templates and metadata.
  - No impact on YAML schema unless new fields for title block/projection/revision are added.
- Required integrations:
  - Template updates for title block, revision table, borders/folding marks.
  - Optional lint/check script to assert presence of required fields in outputs.

## Complexity Score (1–5)

3 — Requires coordinated template changes, metadata additions, and rendering updates, but no deep parser or model rewrites.

## Maintenance Risk

- External standards are stable; low churn.
- Filare-side cost is in keeping templates/config aligned and adding verification scripts.
- Risk: partial implementations may be mistaken for compliance; needs clear flags/labels.

## Industry / Business Usage

- European aerospace/rail/automotive suppliers often require DIN/EN ISO-compliant drawings for harness and cable assemblies.
- Contract manufacturers request EN ISO 5457 sheet framing and EN ISO 7200 title blocks to accept documentation packages.
- Compliance improves acceptability in regulated audits and supplier onboarding.

## Who Uses It & Why It Works for Them

- Automotive wiring diagrams commonly follow DIN 72552/6771 conventions (sheet format, symbols, title blocks) to align across OEM/Tier1 suppliers.
- Industrial control panel drawings in the EU adopt EN ISO 5457 sheet formats and EN ISO 7200 title blocks for consistent archival.
- Rail/rolling stock documentation uses DIN-style borders and revision tables to satisfy safety/maintenance traceability.

## Feasibility

- Feasible now by updating templates and adding verification logic; no core engine changes required.

## Required Work

- REWORK tasks:
  - Align title block template to EN ISO 7200 fields (title, drawing number, revision, date, author/checker/approver, scale, projection, sheet/total).
  - Add folding marks and standardized margins per EN ISO 5457/DIN 823.
  - Parameterize line weights/styles to DIN 15/EN ISO 128 (visible/hidden/center lines).
  - Provide projection symbols and legend placement.
- FEATURE tasks:
  - Add revision table support (schema + template).
  - Add optional DIN compliance mode that toggles required fields and warnings.
  - Add folding marks render option for print/plot.
- DOCUMENTATION tasks:
  - Document DIN compliance expectations and how to enable/verify them.
  - Provide examples of DIN-compliant pages.
  - Document limitations where exact DIN tables are approximated.
- TOOLS tasks:
  - Create a validation script that checks rendered SVG/HTML for presence of required blocks/fields.
  - Add a lint for title-block metadata completeness.
- COVERAGE tasks (per required element):
  - Sheet format/margins/folding marks: render a minimal DIN page and assert SVG viewBox/frame sizes and folding mark coordinates.
  - Title block fields (EN ISO 7200): fixture asserting all required fields/text nodes exist with correct labels/ordering in SVG/HTML.
  - Revision table: render with multiple revisions and snapshot the table structure and values.
  - Projection symbol: assert presence of the first/third-angle symbol asset when enabled.
  - Line weights/styles: check SVG stroke widths/class names match configured DIN defaults for visible/hidden/center lines.
  - Legends/standards references: render with legends enabled and assert legend content plus standards reference text.
  - Page numbering and sheet/total: fixture asserting sheet numbering is present and formatted per spec.
  - Scale/units: assert scale/unit text is rendered in the title block.

## Recommendation

**ADOPT_LATER** — Valuable for EU-centric deployments; proceed after defining template changes and validation approach to avoid pseudo-compliance.

## References

- EN ISO 5457 / DIN 823 (sheet sizes, margins, folding marks)
- EN ISO 7200 (title blocks)
- DIN 15 / EN ISO 128 (line weights/styles)
- DIN 406 (text fields)
- DIN 6771 (wiring diagrams practices)
- DIN 72552 (automotive terminal designations) — context for legends/labels

## Optional Appendix

### Verification Matrix (Filare coverage vs DIN expectations)

| Element                              | DIN/EN ISO Expectation                                                                                               | Filare Coverage (current)                                              | Gaps / Follow-up                                                           |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Sheet format (A0–A4, margins, frame) | EN ISO 5457/DIN 823: defined sizes, margins, frames, folding marks                                                   | Examples reference DIN 823/6771/EN ISO 5457 (HTML demos).              | Add explicit frame/margins/folding marks in templates; configurable sizes. |
| Title block fields                   | EN ISO 7200: title, drawing number, revision, date, author/checker/approver, scale, projection, sheet/total, company | Title block templates exist but not strictly EN ISO 7200; fields vary. | Standardize template fields; enforce presence via metadata lint.           |
| Revision table                       | Revision ID/date/description/approvals                                                                               | No dedicated revision table in templates.                              | Add schema + template block; allow multiple revisions.                     |
| Projection symbol                    | First/third-angle symbol + note                                                                                      | Not rendered today.                                                    | Add projection option and symbol asset in template.                        |
| Line weights/styles                  | EN ISO 128/DIN 15: defined weights for visible/hidden/center lines                                                   | Line weights not standardized; ad-hoc in renderers.                    | Parameterize line styles/weights to DIN defaults with overrides.           |
| Units & scale                        | Metric default; scale noted in title block; “NTS” allowed                                                            | Scale/units not consistently surfaced.                                 | Add scale/unit fields to title block; default metric.                      |
| Legends (symbols/colors)             | Reference legend for symbols/colors per sheet set                                                                    | Color codes exist; legends optional.                                   | Provide legend placement option and default content.                       |
| Page numbering                       | Sheet n / total                                                                                                      | Present in pagination features/issues.                                 | Ensure consistent location per EN ISO 7200; add validation.                |
| Folding marks                        | Marks for folding to A4                                                                                              | Not generated.                                                         | Add optional folding marks per EN ISO 5457.                                |
| Standards references                 | List applicable standards on sheet                                                                                   | Not standardized.                                                      | Add metadata field for standards references.                               |

### Notes

- Use `scripts/check_backlog_headers.py` and `just check-backlog-headers` to keep metadata consistent.
- Potential lint: scan rendered SVG for title block fields and folding marks once implemented.
