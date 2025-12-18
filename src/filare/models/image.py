from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

import factory  # type: ignore[reportPrivateImportUsage]
from factory import Factory  # type: ignore[reportPrivateImportUsage]
from factory.declarations import LazyAttribute  # type: ignore[reportPrivateImportUsage]
from faker import Faker  # type: ignore[reportPrivateImportUsage]

from filare.models.colors import FakeSingleColorFactory, SingleColor
from filare.models.hypertext import MultilineHypertext

faker = Faker()


def aspect_ratio(image_src):
    try:
        from PIL import Image

        image = Image.open(image_src)
        if image.width > 0 and image.height > 0:
            return image.width / image.height
        print(f"aspect_ratio(): Invalid image size {image.width} x {image.height}")
    # ModuleNotFoundError and FileNotFoundError are the most expected, but all are handled equally.
    except Exception as error:
        print(f"aspect_ratio(): {type(error).__name__}: {error}")
    return 1  # Assume 1:1 when unable to read actual image size


@dataclass
class Image:
    # Attributes of the image object <img>:
    src: str
    scale: str = ""
    # Attributes of the image cell <td> containing the image:
    width: Union[int, float] = 0
    height: Union[int, float] = 0
    fixedsize: bool = False
    bgcolor: Optional[SingleColor] = None
    # Contents of the text cell <td> just below the image cell:
    caption: Optional[MultilineHypertext] = None
    # See also HTML doc at https://graphviz.org/doc/info/shapes.html#html

    def __post_init__(self):

        self.width = int(self.width)
        self.height = int(self.height)

        if self.bgcolor is not None:
            self.bgcolor = SingleColor(self.bgcolor)

        if not self.fixedsize:
            # Default True if any dimension specified unless self.scale also is specified.
            self.fixedsize = bool(self.width or self.height) and self.scale in [
                "",
                None,
            ]

        if self.scale in [None, ""]:
            if not self.width and not self.height:
                self.scale = "false"
            elif self.width and self.height:
                self.scale = "both"
            else:
                self.scale = "true"  # When only one dimension is specified.

        if self.fixedsize:
            # If only one dimension is specified, compute the other
            # because Graphviz requires both when fixedsize=True.
            if self.height:
                if not self.width:
                    self.width = self.height * aspect_ratio(self.src)
            else:
                if self.width:
                    self.height = self.width / aspect_ratio(self.src)


class FakeImageFactory(Factory):
    """factory_boy factory for Image dataclass."""

    class Meta:
        model = Image

    src = LazyAttribute(lambda _: faker.file_name(extension="png"))
    scale = ""
    width = LazyAttribute(lambda _: faker.random_int(min=1, max=100))
    height = LazyAttribute(lambda _: faker.random_int(min=1, max=100))
    fixedsize = LazyAttribute(lambda _: faker.boolean())
    bgcolor = LazyAttribute(lambda _: FakeSingleColorFactory.create())
    caption = LazyAttribute(lambda _: MultilineHypertext.to(faker.sentence(nb_words=4)))

    @staticmethod
    def create(**kwargs) -> Image:
        return FakeImageFactory.build(**kwargs)
