"""Template model and factory for simple.html."""

from __future__ import annotations

from typing import ClassVar, Optional

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


class SimpleTemplateOptions(BaseModel):
    """Simple template rendering options."""

    fontname: str = "Arial"
    bgcolor: str = "#FFFFFF"

    model_config = ConfigDict(extra="forbid")


class SimpleTemplateModel(TemplateModel):
    """Context model for rendering simple.html."""

    template_name: ClassVar[str] = "simple"
    generator: str = "Filare"
    title: str = "Simple Diagram"
    description: str = ""
    diagram: str = "<svg></svg>"
    notes: str = ""
    bom: str = ""
    options: SimpleTemplateOptions = Field(default_factory=SimpleTemplateOptions)
    diagram_container_class: Optional[str] = None
    diagram_container_style: Optional[str] = None


class FakeSimpleTemplateFactory(TemplateModelFactory):
    """Factory for SimpleTemplateModel with faker defaults."""

    class Meta:
        model = SimpleTemplateModel

    def __init__(self, **kwargs):
        if "title" not in kwargs:
            kwargs["title"] = faker.sentence(nb_words=3)
        if "description" not in kwargs:
            kwargs["description"] = faker.paragraph(nb_sentences=2)
        if "diagram" not in kwargs:
            kwargs["diagram"] = "<svg><text>Simple Diagram</text></svg>"
        if "notes" not in kwargs:
            kwargs["notes"] = faker.sentence(nb_words=4)
        if "bom" not in kwargs:
            kwargs["bom"] = "<table><tr><td>BOM</td></tr></table>"
        if "diagram_container_class" not in kwargs:
            kwargs["diagram_container_class"] = faker.random_element(
                elements=[None, "diagram-default", "diagram-compact"]
            )
        if "diagram_container_style" not in kwargs:
            kwargs["diagram_container_style"] = faker.random_element(
                elements=[None, "max-height:50mm;", "max-width:80mm;"]
            )
        super().__init__(**kwargs)
