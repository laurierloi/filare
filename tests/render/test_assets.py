import base64
from pathlib import Path

from filare.render import assets


def test_get_mime_subtype_normalizes():
    assert assets.get_mime_subtype("image.JPG") == "jpeg"
    assert assets.get_mime_subtype("foo.tif") == "tiff"
    assert assets.get_mime_subtype("bar.png") == "png"


def test_embed_svg_images_inlines_data(tmp_path):
    # Create a tiny PNG
    png_path = tmp_path / "dot.png"
    png_bytes = base64.b64decode(
        b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAwAB/lf8dwAAAABJRU5ErkJggg=="
    )
    png_path.write_bytes(png_bytes)

    svg = f'<svg><image xlink:href="{png_path.name}" /></svg>'
    inlined = assets.embed_svg_images(svg, tmp_path)
    assert "data:image/png;base64" in inlined
    assert png_path.name not in inlined


def test_embed_svg_images_file_overwrite(tmp_path):
    svg_path = tmp_path / "img.svg"
    png_path = tmp_path / "dot.png"
    png_bytes = base64.b64decode(
        b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAwAB/lf8dwAAAABJRU5ErkJggg=="
    )
    png_path.write_bytes(png_bytes)
    svg_path.write_text(f'<svg><image xlink:href="{png_path.name}" /></svg>')

    assets.embed_svg_images_file(svg_path, overwrite=True)
    # Original name should now contain data URI
    new_content = svg_path.read_text()
    assert "data:image/png;base64" in new_content
