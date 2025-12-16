"""Template model base exports."""

from filare.models.templates.additional_components_model import (
    AdditionalComponentsFactory,
    AdditionalComponentsTemplateModel,
    FakeAdditionalComponentFactory,
)
from filare.models.templates.bom_template_model import (
    BomTemplateModel,
    FakeBomTemplateFactory,
)
from filare.models.templates.cable_template_model import (
    CableTemplateModel,
    FakeCableTemplateFactory,
)
from filare.models.templates.colors_macro_template_model import (
    ColorsMacroTemplateModel,
    FakeColorsMacroTemplateFactory,
)
from filare.models.templates.component_table_template_model import (
    ComponentTableTemplateModel,
    FakeComponentTableTemplateFactory,
)
from filare.models.templates.connector_template_model import (
    ConnectorTemplateModel,
    FakeConnectorTemplateFactory,
)
from filare.models.templates.images_template_model import (
    FakeTemplateImageFactory,
    ImagesTemplateModel,
)
from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

__all__ = [
    "TemplateModel",
    "TemplateModelFactory",
    "AdditionalComponentsFactory",
    "AdditionalComponentsTemplateModel",
    "FakeAdditionalComponentFactory",
    "ConnectorTemplateModel",
    "FakeConnectorTemplateFactory",
    "BomTemplateModel",
    "FakeBomTemplateFactory",
    "CableTemplateModel",
    "FakeCableTemplateFactory",
    "ComponentTableTemplateModel",
    "FakeComponentTableTemplateFactory",
    "ColorsMacroTemplateModel",
    "FakeColorsMacroTemplateFactory",
    "ImagesTemplateModel",
    "FakeTemplateImageFactory",
]
