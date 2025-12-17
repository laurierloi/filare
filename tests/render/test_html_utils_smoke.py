from filare.render import html_utils


def test_table_tr_td_render():
    table = html_utils.Table(contents=[], border=1, cellborder=1, cellspacing=0)
    row = html_utils.Tr(contents=[])
    assert row.contents is not None
    row.contents.append(html_utils.Td("cell", align="left", port="p1"))
    assert table.contents is not None
    table.contents.append(row)
    rendered = str(table)
    assert "<table" in rendered
    assert "cell" in rendered
    assert 'port="p1"' in rendered


def test_img_render_and_defaults():
    img = html_utils.Img(src="pic.png", scale="true", fixedsize=True)
    rendered = str(img)
    assert "pic.png" in rendered
    assert 'scale="true"' in rendered
    assert 'fixedsize="True"' in rendered or 'fixedsize="true"' in rendered


def test_table_adds_multiple_rows():
    table = html_utils.Table(contents=[])
    assert table.contents is not None
    table.contents.append(html_utils.Tr(html_utils.Td("a")))
    table.contents.append(html_utils.Tr(html_utils.Td("b")))
    rendered = str(table)
    assert rendered.count("<tr>") >= 2


def test_html_utils_custom_attrs_and_defaults():
    img = html_utils.Img(src="pic.png")
    assert "pic.png" in str(img)
    # Td defaults colspan/rowspan to None and omits when falsey
    td = html_utils.Td("x", colspan=None, rowspan=None, align="center")
    assert 'colspan="' not in str(td)
    # Table renders attributes passed via kwargs
    table = html_utils.Table(contents=[td], border=0, cellpadding=2)
    rendered = str(table)
    assert 'cellpadding="2"' in rendered


def test_html_utils_update_and_empty_tags():
    td = html_utils.Td(contents=None, delete_if_empty=True)
    assert str(td) == ""
    td.update_attribs(colspan=2)
    assert 'colspan="2"' in str(td.__class__("val", colspan=2))
