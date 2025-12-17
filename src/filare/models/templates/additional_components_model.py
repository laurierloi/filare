"""Template model and factory for additional_components.html."""

from __future__ import annotations

from typing import ClassVar, List

from pydantic import Field

from filare.models.additional_component import (
    AdditionalComponent,
    FakeAdditionalComponentFactory,
)
from filare.models.templates.template_model import TemplateModel, TemplateModelFactory


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
            components = []
            for idx in range(1, count + 1):
                comp = FakeAdditionalComponentFactory.create(bom_entry_id=f"AC{idx}")
                components.append(comp)
            kwargs["additional_components"] = components
        super().__init__(**kwargs)
