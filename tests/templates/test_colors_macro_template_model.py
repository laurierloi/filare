from filare.models.templates import ColorsMacroTemplateModel, FakeColorsMacroTemplateFactory
from filare.render.templates import get_template


def _render_legend(legend):
    template = get_template("colors_macro.html")
    module = template.module
    return module.color_minitable(legend, legend.len)


def test_colors_macro_render_minimal():
    factory = FakeColorsMacroTemplateFactory(count=2)
    model = factory()
    assert isinstance(model, ColorsMacroTemplateModel)

    for legend in model.colors:
        rendered = _render_legend(legend)
        assert legend.hex in rendered


def test_colors_macro_varied_counts():
    for count in (1, 5, 10):
        model = FakeColorsMacroTemplateFactory(count=count)()
        assert len(model.colors) == count
        for legend in model.colors:
            rendered = _render_legend(legend)
            assert legend.hex in rendered
