from __future__ import annotations

import logging
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import factory  # type: ignore[reportPrivateImportUsage]
from factory import Factory  # type: ignore[reportPrivateImportUsage]
from factory.declarations import (  # type: ignore[reportPrivateImportUsage]
    LazyAttribute,
    Sequence,
)
from faker import Faker  # type: ignore[reportPrivateImportUsage]
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

USING_PYDANTIC_V1 = False
faker = Faker()


import filare  # for doing filare.__file__
from filare.errors import MetadataValidationError
from filare.models.types import PlainText

# Metadata can contain whatever is needed by the HTML generation/template.
MetadataKeys = PlainText  # Literal['title', 'description', 'notes', ...]


class DocumentInfo(BaseModel):
    """Minimal document identity (title and PN)."""

    title: str
    pn: str

    model_config = {"frozen": True}


class CompanyInfo(BaseModel):
    """Company identity block for title pages."""

    company: str
    address: str

    model_config = {"frozen": True}


class AuthorSignature(BaseModel):
    """Signature block for authors/reviewers with optional date."""

    name: str = ""
    date: Optional[object] = None

    @classmethod
    def model_validate(cls, *args, **kwargs):
        try:
            return super().model_validate(*args, **kwargs)
        except ValidationError as exc:
            raise MetadataValidationError(f"{cls.__name__}: {exc}") from exc

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as exc:
            raise MetadataValidationError(f"{self.__class__.__name__}: {exc}") from exc

    @field_validator("date", mode="before")
    def _coerce_date(cls, value):
        if value is None:
            return None
        if isinstance(value, (datetime, date)):
            return value
        if isinstance(value, str):
            if value.lower() == "n/a":
                logging.debug("AuthorSignature date set to 'n/a'")
                return "n/a"
            if value == "TBD":
                logging.debug("AuthorSignature date set to 'TBD'")
                return "TBD"
            date_format = "%Y-%m-%d"
            try:
                parsed = datetime.strptime(value, date_format)
                logging.debug("AuthorSignature date parsed as %s", parsed)
                return parsed
            except Exception as err:
                raise MetadataValidationError(
                    f'date ({value}) should be parsable with format ({date_format}) or set to "n/a" or "TBD"'
                ) from err
        return value

    model_config = {"frozen": True}


class AuthorRole(AuthorSignature):
    """Author signature enriched with a role label."""

    role: str = ""


class RevisionSignature(AuthorSignature):
    """Signature for a single revision entry with changelog text."""

    changelog: str = ""


class RevisionInfo(RevisionSignature):
    """Revision entry with explicit revision ID."""

    revision: str = ""


class OutputMetadata(BaseModel):
    """Paths/names for output artifacts."""

    output_dir: Path
    output_name: str

    model_config = {"frozen": True}


class SheetMetadata(BaseModel):
    """Sheet numbering metadata for paginated outputs."""

    sheet_total: int
    sheet_current: int
    sheet_name: str
    sheet_suffix: str = ""

    model_config = {"frozen": True}


class PagesMetadata(BaseModel):
    """Metadata needed to render pages and shared assets."""

    titlepage: Path
    output_names: List[str]
    files: List[Union[str, Path]]
    use_qty_multipliers: bool
    multiplier_file_name: str
    pages_notes: Dict[str, str] = Field(default_factory=dict)
    output_dir: Path

    model_config = {"frozen": True}


class PageTemplateTypes(str, Enum):
    simple = "simple"
    din_6771 = "din-6771"
    titlepage = "titlepage"


class SheetSizes(str, Enum):
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"


class Orientations(str, Enum):
    landscape = "landscape"
    portrait = "portrait"


def _attach_default_orientation(values: Dict[str, Any]) -> Dict[str, Any]:
    data = dict(values or {})
    if data.get("orientation") is None:
        size = data.get("sheetsize")
        data["orientation"] = (
            Orientations.portrait if size == SheetSizes.A4 else Orientations.landscape
        )
    return data


class PageTemplateConfig(BaseModel):
    """Configuration for page template, size, and orientation."""

    name: PageTemplateTypes = PageTemplateTypes.din_6771
    sheetsize: SheetSizes = SheetSizes.A3
    orientation: Optional[Orientations] = None
    if USING_PYDANTIC_V1:

        class Config:
            frozen = False

    else:
        model_config = ConfigDict(frozen=False)

    @field_validator("name", mode="before")
    def _coerce_name(cls, value):
        return PageTemplateTypes(value)

    @field_validator("sheetsize", mode="before")
    def _coerce_size(cls, value):
        return SheetSizes(value)

    if not USING_PYDANTIC_V1:

        @model_validator(mode="before")
        def _default_orientation_before(cls, values: Dict[str, Any]) -> Dict[str, Any]:
            return _attach_default_orientation(values)

    else:

        @model_validator  # type: ignore[reportCallIssue]
        def _default_orientation_after(cls, values: Dict[str, Any]) -> Dict[str, Any]:
            return _attach_default_orientation(values)

    def has_bom_reversed(self):
        return self.name == PageTemplateTypes.din_6771

    model_config = {"frozen": True}


# TODO: Metadata is a 'fourre-tout' of metadata right now.
#       Is this the best way to keep it or we should have more segmentation?
#       Maybe we could avoid inheritance, and instead have everything as an arg
#       Then we create a 'from_dict' options, which fills the args even if they
#       are not at the proper depth (if there's no conflict in names)
class Metadata(
    PagesMetadata, OutputMetadata, CompanyInfo, SheetMetadata, DocumentInfo
):  # type: ignore[misc]
    authors: Dict[str, AuthorSignature] = Field(default_factory=dict)
    revisions: Dict[str, RevisionSignature] = Field(default_factory=dict)
    template: PageTemplateConfig = Field(default_factory=PageTemplateConfig)
    git_status: str = ""
    logo: Optional[str] = None

    @property
    def name(self):
        """Return the preferred document name, prefixing PN if provided."""
        if self.pn and self.pn not in self.output_name:
            return f"{self.pn}-{self.output_name}"
        else:
            return self.output_name

    @field_validator("authors", mode="before")
    def _coerce_authors(cls, value):
        if not value:
            return {}
        return {
            key: val if isinstance(val, AuthorSignature) else AuthorSignature(**val)
            for key, val in value.items()
        }

    @field_validator("revisions", mode="before")
    def _coerce_revisions(cls, value):
        if not value:
            return {}
        return {
            key: val if isinstance(val, RevisionSignature) else RevisionSignature(**val)
            for key, val in value.items()
        }

    @property
    def generator(self):
        """Return the generator string (app name/version/URL)."""
        return f"{filare.APP_NAME} {filare.__version__} - {filare.APP_URL}"

    @property
    def authors_list(self):
        """Return authors as a list of AuthorRole instances."""
        _authors_list = []
        for role, author in self.authors.items():
            _authors_list.append(
                AuthorRole(name=author.name, date=author.date, role=role)
            )
        return _authors_list

    @property
    def revisions_list(self):
        """Return revisions as a list of RevisionInfo instances."""
        _revisions_list = []
        for revision, sig in self.revisions.items():
            _revisions_list.append(
                RevisionInfo(
                    revision=revision,
                    name=sig.name,
                    date=sig.date,
                    changelog=sig.changelog,
                )
            )
        return _revisions_list

    @property
    def revision(self):
        """Return the most recent revision string ('' if none)."""
        if not self.revisions_list:
            return ""
        return self.revisions_list[-1].revision

    @property
    def pages_metadata(self):
        return PagesMetadata(
            titlepage=self.titlepage,
            output_names=self.output_names,
            files=self.files,
            use_qty_multipliers=self.use_qty_multipliers,
            multiplier_file_name=self.multiplier_file_name,
            pages_notes=self.pages_notes,
            output_dir=self.output_dir,
        )

    if USING_PYDANTIC_V1:

        class Config:
            frozen = True
            arbitrary_types_allowed = True

    else:
        model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)


class FakeAuthorSignatureFactory(Factory):
    """factory_boy factory for AuthorSignature."""

    class Meta:
        model = AuthorSignature

    name = LazyAttribute(lambda _: faker.name())
    date = LazyAttribute(lambda _: faker.date_object())

    @staticmethod
    def create(**kwargs) -> AuthorSignature:
        return FakeAuthorSignatureFactory.build(**kwargs)


class FakeRevisionSignatureFactory(FakeAuthorSignatureFactory):
    """factory_boy factory for RevisionSignature."""

    class Meta:
        model = RevisionSignature

    changelog = LazyAttribute(lambda _: faker.sentence(nb_words=6))

    @staticmethod
    def create(**kwargs) -> RevisionSignature:
        return FakeRevisionSignatureFactory.build(**kwargs)


class FakeRevisionInfoFactory(FakeRevisionSignatureFactory):
    """factory_boy factory for RevisionInfo."""

    class Meta:
        model = RevisionInfo

    revision = LazyAttribute(lambda _: faker.random_element(["A", "B", "C"]))

    @staticmethod
    def create(**kwargs) -> RevisionInfo:
        return FakeRevisionInfoFactory.build(**kwargs)


class FakeDocumentInfoFactory(Factory):
    """factory_boy factory for DocumentInfo."""

    class Meta:
        model = DocumentInfo

    title = LazyAttribute(lambda _: faker.sentence(nb_words=3))
    pn = LazyAttribute(lambda _: faker.bothify("PN-####"))

    @staticmethod
    def create(**kwargs) -> DocumentInfo:
        return FakeDocumentInfoFactory.build(**kwargs)


class FakeCompanyInfoFactory(Factory):
    """factory_boy factory for CompanyInfo."""

    class Meta:
        model = CompanyInfo

    company = LazyAttribute(lambda _: faker.company())
    address = LazyAttribute(lambda _: faker.address())

    @staticmethod
    def create(**kwargs) -> CompanyInfo:
        return FakeCompanyInfoFactory.build(**kwargs)


class FakePageTemplateConfigFactory(Factory):
    """factory_boy factory for PageTemplateConfig."""

    class Meta:
        model = PageTemplateConfig

    name = LazyAttribute(lambda _: faker.random_element(list(PageTemplateTypes)))
    sheetsize = LazyAttribute(lambda _: faker.random_element(list(SheetSizes)))
    orientation = LazyAttribute(
        lambda _: (
            None
            if faker.boolean(chance_of_getting_true=30)
            else faker.random_element(list(Orientations))
        )
    )

    @staticmethod
    def create(**kwargs) -> PageTemplateConfig:
        return FakePageTemplateConfigFactory.build(**kwargs)


class FakeMetadataFactory(Factory):
    """factory_boy factory for Metadata."""

    class Meta:
        model = Metadata

    title = LazyAttribute(lambda _: faker.sentence(nb_words=3))
    pn = LazyAttribute(lambda _: faker.bothify("PN-####"))
    company = LazyAttribute(lambda _: faker.company())
    address = LazyAttribute(lambda _: faker.address())
    output_dir = LazyAttribute(lambda _: Path("outputs"))
    output_name = LazyAttribute(lambda _: faker.slug())
    sheet_total = 1
    sheet_current = 1
    sheet_name = LazyAttribute(lambda _: faker.word())
    sheet_suffix = ""
    titlepage = LazyAttribute(lambda _: Path("titlepage.svg"))
    output_names = LazyAttribute(lambda obj: [f"{obj.output_name}.svg"])
    files = LazyAttribute(lambda obj: [str(obj.titlepage)])
    use_qty_multipliers = LazyAttribute(lambda _: faker.boolean())
    multiplier_file_name = "multipliers.tsv"
    pages_notes = LazyAttribute(lambda _: {"notes": faker.sentence(nb_words=4)})
    template = LazyAttribute(lambda _: FakePageTemplateConfigFactory.create())
    authors = LazyAttribute(
        lambda _: {
            "created": FakeAuthorSignatureFactory.create(),
            "reviewed": FakeAuthorSignatureFactory.create(),
        }
    )
    revisions = LazyAttribute(
        lambda _: {"A": FakeRevisionSignatureFactory.create(changelog="Initial")}
    )
    git_status = "clean"
    logo = None

    @staticmethod
    def create(**kwargs) -> Metadata:
        return FakeMetadataFactory.build(**kwargs)


__all__ = [
    "DocumentInfo",
    "CompanyInfo",
    "AuthorSignature",
    "AuthorRole",
    "RevisionSignature",
    "RevisionInfo",
    "OutputMetadata",
    "SheetMetadata",
    "PagesMetadata",
    "PageTemplateConfig",
    "PageTemplateTypes",
    "SheetSizes",
    "Orientations",
    "Metadata",
    "FakeAuthorSignatureFactory",
    "FakeRevisionSignatureFactory",
    "FakeRevisionInfoFactory",
    "FakeDocumentInfoFactory",
    "FakeCompanyInfoFactory",
    "FakePageTemplateConfigFactory",
    "FakeMetadataFactory",
]
