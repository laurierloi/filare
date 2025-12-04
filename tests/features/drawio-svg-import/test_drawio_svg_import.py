from pathlib import Path

from filare.flows.build_harness import _resolve_diagram_svg
from filare.models.harness import Harness
from filare.models.notes import Notes
from filare.models.options import ImportedSVGOptions, PageOptions


def test_resolves_imported_svg_path(tmp_path):
    svg_path = tmp_path / "drawio.svg"
    svg_path.write_text("<svg/>")
    options = PageOptions(diagram_svg={"src": "drawio.svg"})

    _resolve_diagram_svg(options, [tmp_path])

    assert Path(options.diagram_svg.src) == svg_path


def test_imported_svg_is_embedded_in_outputs(tmp_path, basic_metadata, basic_page_options):
    class DummyGraph:
        def __init__(self, content: str):
            self.format = "svg"
            self._content = content

        def render(self, filename, view=False, cleanup=True):
            Path(f"{filename}.{self.format}").write_text(self._content)
            return str(filename)

    asset = tmp_path / "asset.png"
    asset.write_bytes(b"pngbytes")
    svg_src = tmp_path / "diagram.svg"
    svg_src.write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="120px" height="60px">
  <g>
    <rect width="120" height="60" fill="#eeeeee" />
    <image xlink:href="asset.png" width="10" height="10" x="5" y="5" />
  </g>
</svg>
"""
    )
    options: PageOptions = basic_page_options
    options.diagram_svg = ImportedSVGOptions(
        src=str(svg_src), width="80%", align="left", offset_x="5mm"
    )
    harness = Harness(metadata=basic_metadata, options=options, notes=Notes([]))
    harness._graph = DummyGraph("<svg id='generated'></svg>")

    harness.output(filename=tmp_path / "out", fmt=("html", "svg"))

    svg_output = (tmp_path / "out.svg").read_text()
    assert "<?xml" not in svg_output
    assert "<!DOCTYPE" not in svg_output
    assert "data:image/png;base64" in svg_output
    assert "width: 80%" in svg_output

    html_output = (tmp_path / "out.html").read_text()
    assert "diagram-has-import" in html_output
    assert "justify-content: flex-start" in html_output
    assert "diagram-import" in html_output
    assert "translate(5mm" in html_output
