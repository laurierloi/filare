# Hide `None` labels for unlabeled pins

uid: ISS-0009
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Category

FIXER

## Evidence

- Running `uv run filare run examples/basic/basic01.yml -f hs -o outputs/tmp-basic01` (with an existing output dir) shows unlabeled pins rendered with the literal `None` in the connector table when `pinlabels` are omitted.
- In `src/filare/models/dataclasses.py:372-386`, missing `pinlabels` leave `PinClass.label` as `None`.
- The Graphviz template `src/filare/templates/connector.html:21-23` renders `{{ pin.label }}` directly, so `None` is printed when no label is present.

## Expected Behavior

Unlabeled pins should display only their pin numbers; no literal `None` should appear in the diagram. When no label exists, the pin number should take the full row width where the label would normally appear.

## Actual Behavior

Graphviz connector tables display `None` in the label column for pins without labels.

## Impact

Diagrams for connectors without pin names look broken/confusing; users think the tool is exposing internal `None` values.

## Hypotheses

Hypothesis A
Template renders `pin.label` directly; when it is `None`, Jinja prints `None`.

How to investigate:
Inspect `src/filare/templates/connector.html` and render a connector with unlabeled pins to confirm the literal `None` text appears.

Investigation results:
`connector.html` line 21-23 renders `{{ pin.label }}` with a fixed colspan, so falsy/None values are emitted verbatim. Rendering connectors without `pinlabels` would surface the literal `None`.

Is it relevant?
Yes—root cause for the `None` text.

Does it fix?
No by itself, but changing the template to guard `pin.label` fixes the rendering.

Are there side effects?
Minimal; template change only affects unlabeled pins.

Should another issue be created from this?
No.

Hypothesis B
`PinClass` initialization stores `label=None` instead of an empty string, so downstream renderers don’t have a safe default.

How to investigate:
Trace `PinClass` creation in `src/filare/models/dataclasses.py` for connectors without `pinlabels`; confirm resulting `label` field and any fallback logic.

Investigation results:
`PinClass` is built at `dataclasses.py:372-386`; `label=str(pin_label) if pin_label is not None else None` leaves `label=None` when no label is provided. There is no fallback to pin id in the rendering path.

Is it relevant?
Yes—it feeds the template with `None`.

Does it fix?
Not alone; needs either normalization to empty string or template fallback; opting for template fallback.

Are there side effects?
Changing the stored label could alter other label-dependent flows; safer to handle in template for display.

Should another issue be created from this?
No.

Hypothesis C
Graph rendering expects label cells even when labels are absent; the template may need to widen the pin-number cell (colspan) when labels are missing to avoid empty/None columns.

How to investigate:
Review how connector rows are structured in the template (ports + label + color cells) and experiment with conditional colspan adjustments when `pin.label` is falsy.

Investigation results:
Connector rows allocate a two-column label area (`colspan="2"`) regardless of whether a label exists. Without a label, those columns show `None`/blank. Adjusting colspan and content to use `pin.id` when `pin.label` is falsy will meet the “pin number takes all columns” requirement.

Is it relevant?
Yes—ties directly to the requested layout change.

Does it fix?
Yes, with a template conditional to swap label text for pin number and adjust colspan.

Are there side effects?
Low risk; keeps column structure consistent while improving unlabeled pins.

Should another issue be created from this?
No.

## Resolution

- Implemented template fallback: when `pin.label` is falsy, the connector row now spans the label/color columns with the pin number instead of printing `None`.
- Added regression test `tests/render/test_graphviz_smoke.py::test_connector_template_uses_pin_number_when_label_missing` to assert unlabeled pins omit `None` and render the pin number across the row.

Tests:

- `PYTHONPATH=src uv run pytest tests/render/test_graphviz_smoke.py`
