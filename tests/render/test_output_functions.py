from pathlib import Path

from filare.render.output import embed_svg_images, embed_svg_images_file, get_mime_subtype


def test_embed_svg_images_inlines_data(tmp_path):
    img = tmp_path / "img.png"
    img.write_bytes(b"pngdata")
    svg = f'<svg><image xlink:href="  {img.name}  "></image></svg>'
    result = embed_svg_images(svg, tmp_path)
    assert "data:image/png;base64" in result


def test_embed_svg_images_file_overwrites(tmp_path):
    svg_file = tmp_path / "test.svg"
    svg_file.write_text('<svg><image xlink:href="img.png"></image></svg>')
    img = tmp_path / "img.png"
    img.write_bytes(b"pngdata")
    embed_svg_images_file(svg_file)
    assert svg_file.read_text().startswith("<svg>")


def test_get_mime_subtype_replacements():
    assert get_mime_subtype("file.jpg") == "jpeg"
    assert get_mime_subtype(Path("file.tif")) == "tiff"
