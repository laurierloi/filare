"""Model and factory for additional_components.html."""

from __future__ import annotations

from typing import ClassVar, List, Optional

from faker import Faker
from pydantic import BaseModel, Field

from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


class Quantity(BaseModel):
    number: int = Field(..., description="Quantity number for the component.")
    unit: Optional[str] = Field(default=None, description="Optional quantity unit.")


class BomEntry(BaseModel):
    qty: Quantity
    description: str = Field(..., description="Description of the additional component.")
    id: Optional[str] = Field(default=None, description="Optional component identifier.")


class AdditionalComponent(BaseModel):
    bom_entry: BomEntry


def _default_additional_components() -> List[AdditionalComponent]:
    qty = Quantity(number=1, unit=None)
    entry = BomEntry(qty=qty, description="Extra part", id="AC1")
    return [AdditionalComponent(bom_entry=entry)]


class AdditionalComponentsModel(TemplateModel):
    """Context model for rendering additional_components.html."""

    template_name: ClassVar[str] = "additional_components"
    additional_components: List[AdditionalComponent] = Field(
        ..., description="List of additional BOM-style components."
    )


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


class AdditionalComponentsFactory(TemplateModelFactory):
    """Factory for AdditionalComponentsModel with minimal defaults."""

    class Meta:
        model = AdditionalComponentsModel

    def __init__(self, count: int = 1, **kwargs):
        if "additional_components" not in kwargs:
            kwargs["additional_components"] = _generate_components(count)
        super().__init__(**kwargs)
