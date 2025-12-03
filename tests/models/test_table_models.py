from filare.models.table_models import TableCell, TableRow


def test_table_cell_defaults():
    cell = TableCell()
    assert cell.value == ""
    assert cell.css_class is None


def test_table_row_values_property():
    cells = [TableCell(value="a"), TableCell(value="b", css_class="bold")]
    row = TableRow(cells=cells)
    assert row.values == ["a", "b"]
