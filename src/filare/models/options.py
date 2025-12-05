from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from filare.models.colors import ColorOutputMode, SingleColor
from filare.models.types import PlainText


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
        for field in ("bom_rows_per_page", "cut_rows_per_page", "termination_rows_per_page"):
            value = getattr(self, field)
            if isinstance(value, str):
                try:
                    setattr(self, field, int(value))
                except ValueError:
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

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


def get_page_options(parsed_data, page_name: str):
    """Get the page options

    uses: the page\'s options   -> general options -> default options
        ('{page_name}_options') ->    ('options')  -> {}
    """
    page_options_name = f"{page_name}_options"
    if page_options_name in parsed_data:
        return PageOptions(**parsed_data[page_options_name])
    return PageOptions(**parsed_data.get("options", {}))
