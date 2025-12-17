"""Template model and factory for simple-connector.html."""

from __future__ import annotations

from typing import ClassVar

from filare.models.hypertext import MultilineHypertext
from filare.models.templates.connector_template_model import (
    FakeTemplateConnectorPinFactory,
    FakeTemplateMultiColorFactory,
    TemplateConnectorComponent,
)
from filare.models.templates.template_model import TemplateModel, TemplateModelFactory


class SimpleConnectorTemplateModel(TemplateModel):
    """Context model for rendering simple-connector.html."""

    template_name: ClassVar[str] = "simple-connector"
    component: TemplateConnectorComponent

    def to_render_dict(self) -> dict:
        return {"template_name": self.template_name, "component": self.component}


class FakeSimpleConnectorTemplateFactory(TemplateModelFactory):
    """Factory for SimpleConnectorTemplateModel with faker defaults."""

    class Meta:
        model = SimpleConnectorTemplateModel

    def __init__(self, show_color: bool = True, **kwargs):
        if "component" not in kwargs:
            pin = FakeTemplateConnectorPinFactory.create(idx=0)
            kwargs["component"] = TemplateConnectorComponent(
                designator="P1",
                type=MultilineHypertext.to("Simple Connector"),
                subtype=MultilineHypertext.to(""),
                color=(
                    FakeTemplateMultiColorFactory.create(colors=["RD"])
                    if show_color
                    else None
                ),
                show_pincount=True,
                pincount=1,
                ports_left=True,
                ports_right=False,
                has_pincolors=show_color,
                pins=[pin],
                partnumbers=None,
            )
        super().__init__(**kwargs)
