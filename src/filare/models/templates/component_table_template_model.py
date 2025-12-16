"""Template model and factory for component_table.html."""

from __future__ import annotations

from typing import ClassVar, List, Optional, Union

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from filare.models.additional_component import (
    AdditionalComponent,
    FakeAdditionalComponentFactory,
)
from filare.models.hypertext import FakeMultilineHypertextFactory, MultilineHypertext
from filare.models.partnumber import (
    FakePartNumberInfoListFactory,
    PartNumberInfo,
    PartnumberInfoList,
)
from filare.models.templates.images_template_model import (
    FakeTemplateImageFactory,
    TemplateImage,
)
from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


class TemplateComponent(BaseModel):
    """Component context used by component_table.html."""

    designator: str
    partnumbers: Optional[Union[PartNumberInfo, PartnumberInfoList]] = None
    additional_components: List[AdditionalComponent] = Field(default_factory=list)
    notes: Optional[MultilineHypertext] = None
    image: Optional[TemplateImage] = None

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)


class ComponentTableTemplateModel(TemplateModel):
    """Context model for rendering component_table.html."""

    template_name: ClassVar[str] = "component_table"
    component: TemplateComponent

    def to_render_dict(self) -> dict:
        return {"template_name": self.template_name, "component": self.component}


class FakeComponentTableTemplateFactory(TemplateModelFactory):
    """Factory for ComponentTableTemplateModel with faker defaults."""

    class Meta:
        model = ComponentTableTemplateModel

    def __init__(
        self,
        with_partnumbers: bool = True,
        partnumber_count: int = 2,
        with_notes: bool = True,
        with_image: bool = False,
        additional_component_count: int = 0,
        **kwargs,
    ):
        if "component" not in kwargs:
            partnumbers: Optional[Union[PartNumberInfo, PartnumberInfoList]] = None
            if with_partnumbers:
                pn_list = FakePartNumberInfoListFactory.create(count=partnumber_count)
                if partnumber_count > 1:
                    shared_manufacturer = pn_list.pn_list[0].manufacturer
                    for pn in pn_list.pn_list:
                        pn.manufacturer = shared_manufacturer
                    partnumbers = pn_list
                else:
                    partnumbers = pn_list.pn_list[0]
            notes = (
                FakeMultilineHypertextFactory.create(lines=2, words_per_line=4)
                if with_notes
                else None
            )
            image = (
                FakeTemplateImageFactory.create(fixedsize=True) if with_image else None
            )
            additional_components: List[AdditionalComponent] = []
            if additional_component_count:
                additional_components = [
                    FakeAdditionalComponentFactory.create()
                    for _ in range(additional_component_count)
                ]
            kwargs["component"] = TemplateComponent(
                designator="J1",
                partnumbers=partnumbers,
                additional_components=additional_components,
                notes=notes,
                image=image,
            )
        super().__init__(**kwargs)
