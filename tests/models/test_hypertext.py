from filare.models.hypertext import MultilineHypertext


def test_multiline_hypertext_to_and_clean():
    h = MultilineHypertext.to(["line1", "line2"])
    assert isinstance(h, MultilineHypertext)
    assert "line1<br>line2" in h.raw or "line1<br/>line2" in h.raw
    assert "<br" in h.clean


def test_multiline_hypertext_bool_and_repr():
    h = MultilineHypertext.to("text")
    assert not h.is_empty()
    assert "text" in repr(h)
    empty = MultilineHypertext.to(None)
    assert empty.is_empty()
