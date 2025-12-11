import pytest

from filare.models.templates import AdditionalComponentsFactory
from filare.render.templates import get_template


def test_additional_components_render_minimal():
    factory = AdditionalComponentsFactory()
    model = factory()
    rendered = get_template("additional_components.html").render(model.to_render_dict())

    assert "Extra part" in rendered
    assert "AC1" in rendered
    assert "1" in rendered


@pytest.mark.render
@pytest.mark.parametrize(
    "with_id, with_unit",
    [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ],
)
def test_additional_components_render_variants(with_id, with_unit):
    factory = AdditionalComponentsFactory()
    model = factory()
    comp = model.additional_components[0]
    comp.bom_entry.id = "Z1" if with_id else None
    comp.bom_entry.qty.unit = "pcs" if with_unit else None

    rendered = get_template("additional_components.html").render(model.to_render_dict())

    assert "Extra part" in rendered
    if with_id:
        assert "Z1" in rendered
    else:
        assert "Z1" not in rendered
    if with_unit:
        assert "pcs" in rendered
    else:
        assert "pcs" not in rendered
