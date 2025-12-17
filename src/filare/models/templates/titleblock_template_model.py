"""Template model and factory for titleblock.html."""

from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Optional

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


class TemplateRevisionEntry(BaseModel):
    """Revision list entry for the titleblock."""

    revision: str
    date: str
    name: str
    changelog: str

    model_config = ConfigDict(extra="forbid")


class TemplateAuthorEntry(BaseModel):
    """Author/approver entry for the titleblock."""

    role: str
    date: str
    name: str

    model_config = ConfigDict(extra="forbid")


class TemplateTitleblockMetadata(BaseModel):
    """Metadata referenced by titleblock.html."""

    company: str
    address: str
    title: str
    name: Optional[str] = None
    logo: Optional[str] = None
    revision: str = "A"
    git_status: str = "clean"
    sheet_current: int = 1
    sheet_total: int = 1
    sheet_suffix: str = ""
    authors_list: List[TemplateAuthorEntry] = Field(default_factory=list)
    revisions_list: List[TemplateRevisionEntry] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class TemplateTitleblockOptions(BaseModel):
    """Layout options referenced by titleblock.html."""

    titleblock_row_height: float = 5.0

    model_config = ConfigDict(extra="forbid")


class FakeTemplateRevisionEntryFactory:
    """faker-backed factory for TemplateRevisionEntry."""

    @classmethod
    def create(
        cls, revision: Optional[str] = None, **overrides: Any
    ) -> TemplateRevisionEntry:
        payload: Dict[str, Any] = {
            "revision": revision
            or faker.random_element(elements=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")),
            "date": faker.date(),
            "name": faker.name(),
            "changelog": faker.sentence(nb_words=4),
        }
        payload.update(overrides)
        return TemplateRevisionEntry(**payload)


class FakeTemplateAuthorEntryFactory:
    """faker-backed factory for TemplateAuthorEntry."""

    @classmethod
    def create(
        cls, role: Optional[str] = None, **overrides: Any
    ) -> TemplateAuthorEntry:
        payload: Dict[str, Any] = {
            "role": role
            or faker.random_element(elements=["Created", "Checked", "Approved"]),
            "date": faker.date(),
            "name": faker.name(),
        }
        payload.update(overrides)
        return TemplateAuthorEntry(**payload)


class FakeTemplateTitleblockMetadataFactory:
    """faker-backed factory for TemplateTitleblockMetadata."""

    @classmethod
    def create(
        cls,
        author_count: int = 2,
        revision_count: int = 3,
        logo: Optional[str] = None,
        **overrides: Any,
    ) -> TemplateTitleblockMetadata:
        authors = [FakeTemplateAuthorEntryFactory.create() for _ in range(author_count)]
        revisions = [
            FakeTemplateRevisionEntryFactory.create(revision=chr(ord("A") + idx))
            for idx in range(revision_count)
        ]
        payload: Dict[str, Any] = {
            "company": faker.company(),
            "address": faker.address().replace("\n", ", "),
            "title": faker.sentence(nb_words=3),
            "name": faker.word().title(),
            "logo": logo,
            "revision": revisions[-1].revision if revisions else "A",
            "git_status": faker.random_element(elements=["clean", "dirty"]),
            "sheet_current": 1,
            "sheet_total": faker.random_int(min=1, max=5),
            "sheet_suffix": faker.random_element(elements=["", "A", "B"]),
            "authors_list": authors,
            "revisions_list": revisions,
        }
        payload.update(overrides)
        return TemplateTitleblockMetadata(**payload)


class FakeTemplateTitleblockOptionsFactory:
    """faker-backed factory for TemplateTitleblockOptions."""

    @classmethod
    def create(
        cls, titleblock_row_height: float = 5.0, **overrides: Any
    ) -> TemplateTitleblockOptions:
        payload: Dict[str, Any] = {"titleblock_row_height": titleblock_row_height}
        payload.update(overrides)
        return TemplateTitleblockOptions(**payload)


class TitleblockTemplateModel(TemplateModel):
    """Context model for rendering titleblock.html."""

    template_name: ClassVar[str] = "titleblock"
    metadata: TemplateTitleblockMetadata
    options: TemplateTitleblockOptions = Field(
        default_factory=TemplateTitleblockOptions
    )
    partno: str = "PN-000"

    def to_render_dict(self) -> dict:
        return {
            "template_name": self.template_name,
            "metadata": self.metadata,
            "options": self.options,
            "partno": self.partno,
        }


class FakeTitleblockTemplateFactory(TemplateModelFactory):
    """Factory for TitleblockTemplateModel with faker defaults."""

    class Meta:
        model = TitleblockTemplateModel

    def __init__(
        self,
        author_count: int = 2,
        revision_count: int = 3,
        titleblock_row_height: float = 5.0,
        with_logo: bool = False,
        **kwargs,
    ):
        if "metadata" not in kwargs:
            kwargs["metadata"] = FakeTemplateTitleblockMetadataFactory.create(
                author_count=author_count,
                revision_count=revision_count,
                logo=faker.image_url() if with_logo else None,
            )
        if "options" not in kwargs:
            kwargs["options"] = FakeTemplateTitleblockOptionsFactory.create(
                titleblock_row_height=titleblock_row_height
            )
        if "partno" not in kwargs:
            kwargs["partno"] = faker.bothify(text="PN-####")
        super().__init__(**kwargs)
