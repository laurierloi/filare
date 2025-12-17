from typing import cast

import pytest

from filare.models.templates import (
    AdditionalComponentsFactory,
    AdditionalComponentsTemplateModel,
)
from filare.render.templates import get_template


def test_additional_components_render_minimal():
    factory = AdditionalComponentsFactory()
    model = cast(AdditionalComponentsTemplateModel, factory())
    first = model.additional_components[0].bom_entry
    desc = first.description
    ident = first.id
    rendered = model.render()

    assert desc in rendered
    assert ident is not None
    assert ident in rendered
    assert str(first.qty.number) in rendered


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
    model = cast(AdditionalComponentsTemplateModel, factory())
    comp = model.additional_components[0]
    desc = comp.bom_entry.description
    comp.bom_entry.id = comp.bom_entry.id if with_id else None
    comp.bom_entry.qty.unit = "pcs" if with_unit else None

    rendered = model.render()

    assert desc in rendered
    if with_id and comp.bom_entry.id:
        assert comp.bom_entry.id in rendered
    else:
        assert "AC" not in rendered or comp.bom_entry.id is None
    if with_unit:
        assert "pcs" in rendered
    else:
        assert "pcs" not in rendered


def test_additional_components_render_multiple():
    factory = AdditionalComponentsFactory()
    model = cast(AdditionalComponentsTemplateModel, factory())
    second = model.additional_components[0].model_copy(deep=True)
    second.bom_entry.id = "AC2"
    second.bom_entry.qty.number = 5
    second.bom_entry.description = "Another part"
    model.additional_components.append(second)
    first_entry = model.additional_components[0].bom_entry
    first_desc = first_entry.description

    rendered = model.render()

    assert first_entry.id is not None
    assert first_entry.id in rendered and "AC2" in rendered
    assert first_desc in rendered and "Another part" in rendered


def test_additional_components_factory_count_and_faker():
    factory = AdditionalComponentsFactory(count=3)
    model = cast(AdditionalComponentsTemplateModel, factory())

    assert len(model.additional_components) == 3
    assert isinstance(model, AdditionalComponentsTemplateModel)
    for idx, comp in enumerate(model.additional_components, start=1):
        assert comp.bom_entry.description
        assert comp.bom_entry.qty.number >= 1
        assert comp.bom_entry.id == f"AC{idx}"
