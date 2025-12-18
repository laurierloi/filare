import logging
from typing import List, Literal, Optional

import factory  # type: ignore[reportPrivateImportUsage]
from factory import Factory  # type: ignore[reportPrivateImportUsage]
from factory.declarations import LazyAttribute  # type: ignore[reportPrivateImportUsage]
from faker import Faker  # type: ignore[reportPrivateImportUsage]
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from filare.models.colors import ColorOutputMode, FakeSingleColorFactory, SingleColor
from filare.models.types import PlainText

faker = Faker()


class ImportedSVGOptions(BaseModel):
    src: str
    width: Optional[str] = None
    height: Optional[str] = None
    align: Literal["left", "center", "right"] = "center"
    offset_x: str = "0"
    offset_y: str = "0"
    preserve_aspect_ratio: bool = True

    @field_validator("src", "width", "height", "offset_x", "offset_y", mode="before")
    def _coerce_str(cls, value):
        return str(value).strip() if value is not None else value

    model_config = ConfigDict(extra="forbid")


class PageOptions(BaseModel):
    # formatting toggles
    show_bom: bool = True
    bom_updated_position: str = ""
    show_index_table: bool = True
    index_table_on_right: bool = True
    index_table_updated_position: str = ""
    show_notes: bool = True
    notes_on_right: bool = True
    notes_width: str = "180mm"
    split_bom_page: bool = False
    split_notes_page: bool = False
    split_index_page: bool = False
    bom_rows_per_page: Optional[int] = None
    bom_force_single_page: bool = False
    table_page_suffix_letters: bool = True
    cut_rows_per_page: Optional[int] = None
    termination_rows_per_page: Optional[int] = None

    # diagram colors
    bgcolor: SingleColor = Field(default_factory=lambda: SingleColor(inp="WH"))
    bgcolor_node: SingleColor = Field(default_factory=lambda: SingleColor(inp="WH"))
    bgcolor_connector: Optional[SingleColor] = None
    bgcolor_cable: Optional[SingleColor] = None
    bgcolor_bundle: Optional[SingleColor] = None
    color_output_mode: ColorOutputMode = ColorOutputMode.EN_UPPER

    # dimensions
    bom_rows: int = 0
    titleblock_rows: int = 9
    bom_row_height: float = 4.25
    titleblock_row_height: float = 4.25
    index_table_row_height: float = 4.25

    # misc
    fontname: PlainText = "arial"
    mini_bom_mode: bool = True
    template_separator: str = "."
    for_pdf: bool = False
    pad: int = 0
    template_paths: List = Field(default_factory=list)
    image_paths: List = Field(default_factory=list)
    include_bom: bool = True
    include_cut_diagram: bool = False
    include_termination_diagram: bool = False
    diagram_svg: Optional[ImportedSVGOptions] = None

    @field_validator(
        "bgcolor",
        "bgcolor_node",
        "bgcolor_connector",
        "bgcolor_cable",
        "bgcolor_bundle",
        mode="before",
    )
    def _to_single_color(cls, value):
        return value if isinstance(value, SingleColor) else SingleColor(inp=value)

    @model_validator(mode="after")
    def _fill_missing_colors(self):
        self.bgcolor_node = self.bgcolor_node or self.bgcolor
        self.bgcolor_connector = self.bgcolor_connector or self.bgcolor_node
        self.bgcolor_cable = self.bgcolor_cable or self.bgcolor_node
        self.bgcolor_bundle = self.bgcolor_bundle or self.bgcolor_cable
        return self

    @field_validator(
        "bom_rows",
        "titleblock_rows",
        mode="before",
    )
    def _coerce_int(cls, value):
        if isinstance(value, list):
            return len(value)
        return int(value)

    @field_validator(
        "bom_rows_per_page",
        "cut_rows_per_page",
        "termination_rows_per_page",
        mode="before",
    )
    def _coerce_optional_int(cls, value):
        if value in (None, ""):
            return None
        return int(value)

    @model_validator(mode="after")
    def _normalize_row_counts(self):
        """Normalize row count fields to ints when provided as strings."""
        for field in (
            "bom_rows_per_page",
            "cut_rows_per_page",
            "termination_rows_per_page",
        ):
            value = getattr(self, field)
            if isinstance(value, str):
                try:
                    setattr(self, field, int(value))
                except ValueError:
                    logging.warning(
                        "Page option %s=%r is not numeric; defaulting to automatic pagination. "
                        "Set an integer to control rows per page.",
                        field,
                        value,
                    )
                    setattr(self, field, None)
        return self

    @field_validator(
        "bom_row_height",
        "titleblock_row_height",
        "index_table_row_height",
        mode="before",
    )
    def _coerce_float(cls, value):
        return float(value)

    @field_validator("diagram_svg", mode="before")
    def _coerce_diagram_svg(cls, value):
        if not value:
            return None
        if isinstance(value, ImportedSVGOptions):
            return value
        if isinstance(value, str):
            return {"src": value}
        return value

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


def get_page_options(parsed_data, page_name: str):
    """Resolve page-specific options with sensible fallbacks.

    Precedence: `{page_name}_options` -> `options` -> defaults.

    Args:
        parsed_data: Parsed YAML dict for the harness.
        page_name: Page type name (e.g., "harness", "title").

    Returns:
        PageOptions instance combining specific and global overrides.
    """
    page_options_name = f"{page_name}_options"
    if page_options_name in parsed_data:
        return PageOptions(**parsed_data[page_options_name])
    return PageOptions(**parsed_data.get("options", {}))


class FakeImportedSVGOptionsFactory(Factory):
    """factory_boy factory for ImportedSVGOptions."""

    class Meta:
        model = ImportedSVGOptions

    src = LazyAttribute(lambda _: faker.file_path(extension="svg"))
    width = LazyAttribute(lambda _: faker.random_element(["10", "20", None]))
    height = LazyAttribute(lambda _: faker.random_element(["10", "15", None]))
    align = LazyAttribute(lambda _: faker.random_element(["left", "center", "right"]))
    offset_x = "0"
    offset_y = "0"
    preserve_aspect_ratio = True

    @staticmethod
    def create(**kwargs) -> ImportedSVGOptions:
        return FakeImportedSVGOptionsFactory.build(**kwargs)


class FakePageOptionsFactory(Factory):
    """factory_boy factory for PageOptions."""

    class Meta:
        model = PageOptions

    class Params:
        with_svg = False
        with_bg = True

    show_bom = True
    bom_updated_position = ""
    show_index_table = True
    index_table_on_right = True
    index_table_updated_position = ""
    show_notes = True
    notes_on_right = LazyAttribute(lambda _: faker.boolean())
    notes_width = "180mm"
    split_bom_page = False
    split_notes_page = False
    split_index_page = False
    bom_rows_per_page = None
    bom_force_single_page = False
    table_page_suffix_letters = True
    cut_rows_per_page = None
    termination_rows_per_page = None
    bgcolor = LazyAttribute(lambda obj: FakeSingleColorFactory.create())
    bgcolor_node = LazyAttribute(lambda obj: obj.bgcolor)
    bgcolor_connector = LazyAttribute(lambda obj: obj.bgcolor_node)
    bgcolor_cable = LazyAttribute(lambda obj: obj.bgcolor_node)
    bgcolor_bundle = LazyAttribute(lambda obj: obj.bgcolor_cable)
    color_output_mode = ColorOutputMode.EN_UPPER
    bom_rows = 0
    titleblock_rows = 9
    bom_row_height = LazyAttribute(
        lambda _: float(faker.pyfloat(left_digits=2, right_digits=2, positive=True))
    )
    titleblock_row_height = LazyAttribute(
        lambda _: float(faker.pyfloat(left_digits=2, right_digits=2, positive=True))
    )
    index_table_row_height = LazyAttribute(
        lambda _: float(faker.pyfloat(left_digits=2, right_digits=2, positive=True))
    )
    fontname = LazyAttribute(lambda _: faker.word())
    mini_bom_mode = LazyAttribute(lambda _: faker.boolean())
    template_separator = "."
    for_pdf = LazyAttribute(lambda _: faker.boolean())
    pad = 0
    template_paths = LazyAttribute(lambda _: ["templates"])
    image_paths = LazyAttribute(lambda _: ["images"])
    include_bom = True
    include_cut_diagram = LazyAttribute(lambda _: faker.boolean())
    include_termination_diagram = LazyAttribute(lambda _: faker.boolean())
    diagram_svg = LazyAttribute(
        lambda obj: FakeImportedSVGOptionsFactory.create() if obj.with_svg else None
    )

    @staticmethod
    def create(**kwargs) -> PageOptions:
        return FakePageOptionsFactory.build(**kwargs)


__all__ = [
    "ImportedSVGOptions",
    "PageOptions",
    "get_page_options",
    "FakeImportedSVGOptionsFactory",
    "FakePageOptionsFactory",
]
