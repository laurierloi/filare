from typing import ClassVar

import pytest

from pydantic import ValidationError

from filare.models.templates.template_model import TemplateModel, TemplateModelFactory


def test_template_model_to_render_dict_minimal():
    model = TemplateModel()
    assert model.to_render_dict() == {"template_name": "template"}


@pytest.mark.render
@pytest.mark.parametrize("template_name", ["alpha", "beta"])
def test_template_model_factory_variants(template_name):
    CustomTemplate = type(
        "CustomTemplate",
        (TemplateModel,),
        {"template_name": template_name},
    )

    CustomTemplateFactory = type(
        "CustomTemplateFactory",
        (TemplateModelFactory,),
        {"Meta": type("Meta", (), {"model": CustomTemplate})},
    )

    model = CustomTemplateFactory()
    payload = model.to_render_dict()

    assert payload["template_name"] == template_name


def test_template_model_forbids_extra():
    with pytest.raises(ValidationError):
        TemplateModel(**{"template_name": "x", "extra": "nope"})
