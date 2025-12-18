"""Page models used within DocumentRepresentation."""

from enum import Enum
from typing import List, Optional

import factory  # type: ignore[reportPrivateImportUsage]
from factory import Factory  # type: ignore[reportPrivateImportUsage]
from factory.declarations import LazyAttribute  # type: ignore[reportPrivateImportUsage]
from faker import Faker  # type: ignore[reportPrivateImportUsage]
from pydantic import BaseModel, ConfigDict, Field

faker = Faker()


class PageType(Enum):
    title = "title"
    harness = "harness"
    bom = "bom"
    cut = "cut"
    termination = "termination"

    def __str__(self) -> str:
        return self.value


class PageBase(BaseModel):
    """Base page info shared by all page types."""

    type: PageType = Field(..., description="Page type identifier")
    name: Optional[str] = Field(None, description="Logical page name or designator")
    formats: List[str] = Field(
        default_factory=list, description="Requested output formats"
    )

    model_config = ConfigDict(extra="allow")


class HarnessPage(PageBase):
    """Page representing a harness diagram."""

    model_config = ConfigDict(extra="allow")


class BOMPage(PageBase):
    """Page representing a BOM table."""

    include: bool = True

    model_config = ConfigDict(extra="allow")


class CutPage(PageBase):
    """Page representing a wire cut table/diagram."""

    include: bool = False

    model_config = ConfigDict(extra="allow")


class TerminationPage(PageBase):
    """Page representing a termination table/diagram."""

    include: bool = False

    model_config = ConfigDict(extra="allow")


class TitlePage(PageBase):
    """Page representing a title page/front matter."""

    include: bool = True

    model_config = ConfigDict(extra="allow")


class FakePageBaseFactory(Factory):
    """factory_boy factory for PageBase-derived models."""

    class Meta:
        model = PageBase

    type = PageType.harness
    name = LazyAttribute(lambda _: faker.bothify("P-##"))
    formats = LazyAttribute(lambda _: ["svg", "html"])

    @staticmethod
    def create(**kwargs) -> PageBase:
        return FakePageBaseFactory.build(**kwargs)


class FakeHarnessPageFactory(FakePageBaseFactory):
    class Meta:
        model = HarnessPage

    type = PageType.harness


class FakeBOMPageFactory(FakePageBaseFactory):
    class Meta:
        model = BOMPage

    type = LazyAttribute(lambda _: PageType.bom)
    include = True

    @staticmethod
    def create(**kwargs) -> BOMPage:
        return FakeBOMPageFactory.build(type=PageType.bom, **kwargs)


class FakeCutPageFactory(FakePageBaseFactory):
    class Meta:
        model = CutPage

    type = LazyAttribute(lambda _: PageType.cut)
    include = False

    @staticmethod
    def create(**kwargs) -> CutPage:
        return FakeCutPageFactory.build(type=PageType.cut, **kwargs)


class FakeTerminationPageFactory(FakePageBaseFactory):
    class Meta:
        model = TerminationPage

    type = LazyAttribute(lambda _: PageType.termination)
    include = False

    @staticmethod
    def create(**kwargs) -> TerminationPage:
        return FakeTerminationPageFactory.build(type=PageType.termination, **kwargs)


class FakeTitlePageFactory(FakePageBaseFactory):
    class Meta:
        model = TitlePage

    type = LazyAttribute(lambda _: PageType.title)
    include = True

    @staticmethod
    def create(**kwargs) -> TitlePage:
        return FakeTitlePageFactory.build(type=PageType.title, **kwargs)


__all__ = [
    "PageType",
    "PageBase",
    "HarnessPage",
    "BOMPage",
    "CutPage",
    "TerminationPage",
    "TitlePage",
    "FakePageBaseFactory",
    "FakeHarnessPageFactory",
    "FakeBOMPageFactory",
    "FakeCutPageFactory",
    "FakeTerminationPageFactory",
    "FakeTitlePageFactory",
]
