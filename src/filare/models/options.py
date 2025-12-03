from typing import List, Optional

from pydantic.v1 import BaseModel, Field, root_validator, validator

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
    notes_width: str = "100mm"

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
    _pad: int = 0
    _template_paths: List = Field(default_factory=list)
    _image_paths: List = Field(default_factory=list)

    @validator(
        "bgcolor",
        "bgcolor_node",
        "bgcolor_connector",
        "bgcolor_cable",
        "bgcolor_bundle",
        pre=True,
    )
    def _to_single_color(cls, value):
        return value if isinstance(value, SingleColor) else SingleColor(inp=value)

    @root_validator
    def _fill_missing_colors(cls, values):
        values["bgcolor_node"] = values.get("bgcolor_node") or values.get("bgcolor")
        values["bgcolor_connector"] = values.get("bgcolor_connector") or values.get(
            "bgcolor_node"
        )
        values["bgcolor_cable"] = values.get("bgcolor_cable") or values.get(
            "bgcolor_node"
        )
        values["bgcolor_bundle"] = values.get("bgcolor_bundle") or values.get(
            "bgcolor_cable"
        )
        return values

    @validator(
        "bom_rows",
        "titleblock_rows",
        pre=True,
    )
    def _coerce_int(cls, value):
        if isinstance(value, list):
            return len(value)
        return int(value)

    @validator(
        "bom_row_height",
        "titleblock_row_height",
        "index_table_row_height",
        pre=True,
    )
    def _coerce_float(cls, value):
        return float(value)

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True
        underscore_attrs_are_private = True


def get_page_options(parsed_data, page_name: str):
    """Get the page options

    uses: the page\'s options   -> general options -> default options
        ('{page_name}_options') ->    ('options')  -> {}
    """
    page_options_name = f"{page_name}_options"
    if page_options_name in parsed_data:
        return PageOptions(**parsed_data[page_options_name])
    return PageOptions(**parsed_data.get("options", {}))
