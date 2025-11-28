from filare.models.connector import GraphicalComponentModel
from filare.models.colors import MultiColor


def test_graphical_component_model_to_dataclass():
    model = GraphicalComponentModel(
        designator="X1",
        type=["Line1", "Line2"],
        color="RD",
        bgcolor="#ffffff",
        bgcolor_title="#eeeeee",
        notes="Note line",
    )
    comp = model.to_graphical_component()
    assert comp.designator == "X1"
    assert isinstance(comp.color, MultiColor)
    assert comp.type.raw.startswith("Line1")
    assert comp.bgcolor.html.lower() in ("#ffffff", "0xffffff")
