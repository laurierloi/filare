from filare.models.image import FakeImageFactory, Image


def test_image_defaults_and_flags(tmp_path):
    img = Image(src="pic.png", scale="both", fixedsize=True)
    assert img.src == "pic.png"
    assert img.scale == "both"
    assert img.fixedsize is True


def test_image_eq_and_str():
    a = Image(src="a.png")
    b = Image(src="a.png")
    c = Image(src="b.png")
    assert a == b
    assert a != c
    assert "a.png" in str(a)


def test_image_fixedsize_and_scale_inference(monkeypatch, tmp_path):
    # width with fixedsize triggers height calc via aspect_ratio
    src = tmp_path / "img.png"
    src.write_text("content")
    monkeypatch.setattr("filare.models.image.aspect_ratio", lambda _src: 2)
    img = Image(src=str(src), width=4, height=0, fixedsize=True, scale="")
    assert img.height == 2  # computed from aspect ratio
    assert img.scale in ("true", "both")


def test_image_aspect_ratio_error_path(tmp_path):
    # missing file triggers exception handling and returns default ratio
    assert Image(src="missing.png").scale in ("false", "true", "both")
    from filare.models.image import aspect_ratio

    assert aspect_ratio(tmp_path / "nope.png") == 1


def test_image_scale_both_when_dimensions_given(tmp_path):
    img = Image(src=str(tmp_path / "x.png"), width=2, height=3, scale="")
    assert img.scale == "both"


def test_fake_image_factory_defaults():
    img = FakeImageFactory.create()
    assert img.src.endswith(".png")
    assert isinstance(img.bgcolor, object)
    assert img.caption is None or img.caption.raw
