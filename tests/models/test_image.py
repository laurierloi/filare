from filare.models.image import Image


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
