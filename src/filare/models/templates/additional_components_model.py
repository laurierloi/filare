"""Template model and factory for additional_components.html."""

from __future__ import annotations

from typing import ClassVar, List

from faker import Faker
from pydantic import Field

from filare.models.additional_component import AdditionalComponent, BomEntry, Quantity
from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


def _generate_components(count: int) -> List[AdditionalComponent]:
    components: List[AdditionalComponent] = []
    for idx in range(1, count + 1):
        qty = Quantity(
            number=faker.random_int(min=1, max=9),
            unit=faker.random_element(elements=[None, "pcs", "ea"]),
        )
        entry = BomEntry(
            qty=qty,
            description=faker.sentence(nb_words=3),
            id=f"AC{idx}",
        )
        components.append(AdditionalComponent(bom_entry=entry))
    return components


class AdditionalComponentsTemplateModel(TemplateModel):
    """Context model for rendering additional_components.html."""

    template_name: ClassVar[str] = "additional_components"
    additional_components: List[AdditionalComponent] = Field(
        ..., description="List of additional BOM-style components."
    )


class AdditionalComponentsFactory(TemplateModelFactory):
    """Factory for AdditionalComponentsTemplateModel with faker defaults."""

    class Meta:
        model = AdditionalComponentsTemplateModel

    def __init__(self, count: int = 1, **kwargs):
        if "additional_components" not in kwargs:
            kwargs["additional_components"] = _generate_components(count)
        super().__init__(**kwargs)
