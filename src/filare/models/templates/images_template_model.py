"""Template model and factory for images.html."""

from __future__ import annotations

from typing import ClassVar, Optional

from faker import Faker
from pydantic import BaseModel, ConfigDict

from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


class TemplateImage(BaseModel):
    """Image payload accepted by images.html."""

    src: str
    scale: str = "true"
    width: int = 0
    height: int = 0
    fixedsize: bool = False
    caption: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class FakeTemplateImageFactory:
    """faker-backed factory for TemplateImage."""

    @classmethod
    def create(
        cls, fixedsize: bool = False, with_caption: bool = True, **overrides: object
    ) -> TemplateImage:
        payload = {
            "src": "image.png",
            "scale": "true",
            "width": 120 if fixedsize else 0,
            "height": 80 if fixedsize else 0,
            "fixedsize": fixedsize,
            "caption": faker.sentence(nb_words=3) if with_caption else None,
        }
        payload.update(overrides)
        return TemplateImage(**payload)


class ImagesTemplateModel(TemplateModel):
    """Context model for rendering images.html."""

    template_name: ClassVar[str] = "images"
    image: Optional[TemplateImage] = None


class FakeImagesTemplateFactory(TemplateModelFactory):
    """Factory for ImagesTemplateModel with faker defaults."""

    class Meta:
        model = ImagesTemplateModel

    def __init__(self, fixedsize: bool = False, with_caption: bool = True, **kwargs):
        if "image" not in kwargs:
            kwargs["image"] = FakeTemplateImageFactory.create(
                fixedsize=fixedsize, with_caption=with_caption
            )
        super().__init__(**kwargs)
