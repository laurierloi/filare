import pytest

from filare.models.templates import AdditionalComponentsFactory
from filare.render.templates import get_template


def test_additional_components_render_minimal():
    factory = AdditionalComponentsFactory()
    model = factory()
    desc = model.additional_components[0].bom_entry.description
    rendered = get_template("additional_components.html").render(model.to_render_dict())

    assert desc in rendered
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
    desc = comp.bom_entry.description
    comp.bom_entry.id = "Z1" if with_id else None
    comp.bom_entry.qty.unit = "pcs" if with_unit else None

    rendered = get_template("additional_components.html").render(model.to_render_dict())

    assert desc in rendered
    if with_id:
        assert "Z1" in rendered
    else:
        assert "Z1" not in rendered
    if with_unit:
        assert "pcs" in rendered
    else:
        assert "pcs" not in rendered


def test_additional_components_render_multiple():
    factory = AdditionalComponentsFactory()
    model = factory()
    second = model.additional_components[0].model_copy(deep=True)
    second.bom_entry.id = "AC2"
    second.bom_entry.qty.number = 5
    second.bom_entry.description = "Another part"
    model.additional_components.append(second)
    first_desc = model.additional_components[0].bom_entry.description

    rendered = get_template("additional_components.html").render(model.to_render_dict())

    assert "AC1" in rendered and "AC2" in rendered
    assert first_desc in rendered and "Another part" in rendered


def test_additional_components_factory_count_and_faker():
    factory = AdditionalComponentsFactory(count=3)
    model = factory()

    assert len(model.additional_components) == 3
    for idx, comp in enumerate(model.additional_components, start=1):
        assert comp.bom_entry.description
        assert comp.bom_entry.qty.number >= 1
        assert comp.bom_entry.id == f"AC{idx}"
