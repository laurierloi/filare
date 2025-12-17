from typing import Any, cast

import pytest

from filare.models.templates import (
    ColorsMacroTemplateModel,
    FakeColorsMacroTemplateFactory,
)
from filare.render.templates import get_template


def _render_legend(legend):
    template = get_template("colors_macro.html")
    module = cast(Any, template.module)
    return module.color_minitable(legend, legend.len)


def test_colors_macro_render_minimal():
    factory = FakeColorsMacroTemplateFactory(count=2)
    model = factory()
    assert isinstance(model, ColorsMacroTemplateModel)

    for legend in model.colors:
        rendered = _render_legend(legend)
        assert legend.colors
        assert legend.colors[0].html is not None
        assert (
            legend.colors[0].html in rendered
            or legend.colors[0].html_padded in rendered
        )


@pytest.mark.parametrize("count", [1, 5, 10])
def test_colors_macro_varied_counts(count):
    model = FakeColorsMacroTemplateFactory(count=count)()
    assert len(model.colors) == count
    for legend in model.colors:
        rendered = _render_legend(legend)
        assert legend.colors
        assert (
            legend.colors[0].html in rendered
            or legend.colors[0].html_padded in rendered
        )


from filare.models.colors import COLOR_CODES


@pytest.mark.parametrize("color_code", list(COLOR_CODES.keys()))
def test_colors_macro_with_color_codes(color_code):
    palette = COLOR_CODES[color_code]
    model = FakeColorsMacroTemplateFactory(count=len(palette), color_code=color_code)()
    assert len(model.colors) == len(palette)
    for legend in model.colors:
        rendered = _render_legend(legend)
        assert legend.colors
        assert (
            legend.colors[0].html in rendered
            or legend.colors[0].html_padded in rendered
        )


@pytest.mark.parametrize("color_code", list(COLOR_CODES.keys())[:2])
def test_colors_macro_palette_wrap(color_code):
    palette = COLOR_CODES[color_code]
    requested = len(palette) + 3  # force wrap beyond palette size
    model = FakeColorsMacroTemplateFactory(
        count=2, color_code=color_code, legend_color_count=requested
    )()
    for legend in model.colors:
        assert legend.len == requested
        assert len(legend.colors) == requested
        rendered = _render_legend(legend)
        assert (
            legend.colors[0].html in rendered
            or legend.colors[0].html_padded in rendered
        )
