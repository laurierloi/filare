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
from filare.models.templates.cut_table_template_model import (
    CutTableTemplateModel,
    FakeCutTableTemplateFactory,
)
from filare.models.templates.cut_template_model import (
    CutTemplateModel,
    FakeCutTemplateFactory,
)
from filare.models.templates.din_6771_template_model import (
    Din6771TemplateModel,
    FakeDin6771TemplateFactory,
)
from filare.models.templates.images_template_model import (
    FakeImagesTemplateFactory,
    FakeTemplateImageFactory,
    ImagesTemplateModel,
)
from filare.models.templates.index_table_template_model import (
    FakeIndexTableTemplateFactory,
    IndexTableTemplateModel,
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
    "CutTableTemplateModel",
    "FakeCutTableTemplateFactory",
    "CutTemplateModel",
    "FakeCutTemplateFactory",
    "Din6771TemplateModel",
    "FakeDin6771TemplateFactory",
    "ImagesTemplateModel",
    "FakeImagesTemplateFactory",
    "FakeTemplateImageFactory",
    "IndexTableTemplateModel",
    "FakeIndexTableTemplateFactory",
]
