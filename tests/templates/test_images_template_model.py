import pytest

from filare.models.templates import FakeImagesTemplateFactory, ImagesTemplateModel
from filare.render.templates import get_template


def test_images_template_render_minimal():
    model = FakeImagesTemplateFactory(fixedsize=False, with_caption=True)()
    assert isinstance(model, ImagesTemplateModel)

    rendered = get_template("images.html").render(model.to_render_dict())

    assert model.image.src in rendered
    assert str(model.image.scale) in rendered
    assert model.image.caption in rendered


@pytest.mark.render
def test_images_template_fixedsize_variant():
    model = FakeImagesTemplateFactory(fixedsize=True, with_caption=False)()
    rendered = get_template("images.html").render(model.to_render_dict())

    assert str(model.image.width) in rendered
    assert str(model.image.height) in rendered
    assert model.image.caption is None
    assert "No Image Defined" not in rendered


def test_images_template_none_image():
    rendered = get_template("images.html").render(
        {"template_name": "images", "image": None}
    )
    assert "No Image Defined" in rendered
