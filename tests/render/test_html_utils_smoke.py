from filare.render import html_utils


def test_table_tr_td_render():
    table = html_utils.Table(contents=[], border=1, cellborder=1, cellspacing=0)
    row = html_utils.Tr(contents=[])
    row.contents.append(html_utils.Td("cell", align="left", port="p1"))
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
    table.contents.append(html_utils.Tr(html_utils.Td("a")))
    table.contents.append(html_utils.Tr(html_utils.Td("b")))
    rendered = str(table)
    assert rendered.count("<tr>") >= 2
