from filare.models.colors import MultiColor, SingleColor
from filare.models.connector import GraphicalComponentModel
from filare.models.hypertext import MultilineHypertext


def test_graphical_component_model_to_dataclass():
    model = GraphicalComponentModel(
        designator="X1",
        type=MultilineHypertext.to(["Line1", "Line2"]),
        color=MultiColor(["RD"]),
        bgcolor=SingleColor("#ffffff"),
        bgcolor_title=SingleColor("#eeeeee"),
        notes=MultilineHypertext.to("Note line"),
    )
    comp = model.to_graphical_component()
    assert comp.designator == "X1"
    assert isinstance(comp.color, MultiColor)
    assert comp.type is not None
    assert comp.type.raw.startswith("Line1")
    assert comp.bgcolor is not None
    assert comp.bgcolor.html is not None
    assert comp.bgcolor.html.lower() in ("#ffffff", "0xffffff")
