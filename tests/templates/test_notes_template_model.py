import pytest

from filare.models.templates import FakeNotesTemplateFactory, NotesTemplateModel
from filare.render.templates import get_template


def test_notes_template_render_minimal():
    model = FakeNotesTemplateFactory()()
    assert isinstance(model, NotesTemplateModel)

    rendered = get_template("notes.html").render(model.to_render_dict())

    assert "Notes:" in rendered
    assert model.notes.clean in rendered
    assert (
        str(model.options.titleblock_rows) in rendered
        or model.options.notes_width in rendered
    )


@pytest.mark.render
@pytest.mark.parametrize(
    "show_bom,notes_on_right,notes_width,titleblock_rows,bom_rows,bom_row_height",
    [
        (False, False, "80mm", 3, 0, 5.0),
        (True, False, "90mm", 4, 2, 6.0),
        (False, True, "100mm", 2, 0, 5.0),
        (True, True, "120mm", 5, 3, 4.0),
    ],
)
def test_notes_template_option_effects(
    show_bom, notes_on_right, notes_width, titleblock_rows, bom_rows, bom_row_height
):
    model = FakeNotesTemplateFactory(
        options={
            "show_bom": show_bom,
            "notes_on_right": notes_on_right,
            "notes_width": notes_width,
            "titleblock_rows": titleblock_rows,
            "bom_rows": bom_rows,
            "bom_row_height": bom_row_height,
        }
    )()
    rendered = get_template("notes.html").render(model.to_render_dict())

    assert notes_width in rendered
    if show_bom and not notes_on_right:
        assert str(bom_rows) in rendered
        # The style block includes computed bottom offset; ensure bom influence is reflected
        bom_bottom = (bom_rows + 2) * bom_row_height
        assert (
            f"{bom_row_height}" in rendered
            or f"{bom_bottom}" in rendered
            or f"bottom: {bom_bottom}" in rendered
            or f"bottom: {bom_bottom:.1f}" in rendered
        )
    elif show_bom:
        # When notes_on_right is True, template uses titleblock-based bottom calculation
        assert str(titleblock_rows) in rendered
    if notes_on_right:
        assert "right: 10mm" in rendered
    else:
        assert "left: 0" in rendered or "left: 0;" in rendered
