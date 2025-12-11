import pytest

from filare.models.templates import CableTemplateModel, FakeCableTemplateFactory
from filare.render.templates import get_template


def test_cable_template_render_minimal():
    factory = FakeCableTemplateFactory(wirecount=2, with_shield=False)
    model = factory()
    assert isinstance(model, CableTemplateModel)

    rendered = get_template("cable.html").render(model.to_render_dict())

    comp = model.component
    assert comp.designator in rendered
    assert str(comp.wirecount) in rendered
    for wire in comp.wire_objects.values():
        assert wire.id in rendered
        assert wire.color.html_padded in rendered


@pytest.mark.render
@pytest.mark.parametrize(
    "wirecount, with_shield",
    [
        (1, False),
        (5, False),
        (10, True),
    ],
)
def test_cable_template_variants(wirecount, with_shield):
    factory = FakeCableTemplateFactory(wirecount=wirecount, with_shield=with_shield)
    model = factory()
    rendered = get_template("cable.html").render(model.to_render_dict())

    comp = model.component
    assert len(comp.wire_objects) >= wirecount
    # Verify first and last wire IDs appear
    first_wire = comp.wire_objects[f"W1"]
    assert first_wire.id in rendered
    last_key = sorted([k for k in comp.wire_objects.keys() if k.startswith("W")])[-1]
    assert comp.wire_objects[last_key].id in rendered
    if with_shield:
        shield_ids = [wid for wid, wire in comp.wire_objects.items() if wire.is_shield]
        assert shield_ids
