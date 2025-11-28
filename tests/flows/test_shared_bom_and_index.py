import pathlib

import pytest

from filare.flows.index_pages import build_pdf_bundle, build_titlepage
from filare.flows.shared_bom import build_shared_bom


def test_build_shared_bom_invokes_render(monkeypatch, tmp_path):
    called = {}

    def fake_generate_shared_bom(**kwargs):
        called["args"] = kwargs
        return tmp_path / "shared_bom"

    monkeypatch.setattr(
        "filare.flows.shared_bom.generate_shared_bom", fake_generate_shared_bom
    )
    out = build_shared_bom(
        tmp_path,
        {"bom": "v"},
        use_qty_multipliers=True,
        files=[tmp_path / "a"],
        multiplier_file_name="m.txt",
    )
    assert out == tmp_path / "shared_bom"
    assert called["args"]["use_qty_multipliers"] is True


def test_build_titlepage_uses_metadata(monkeypatch, tmp_path):
    meta = tmp_path / "meta.yml"
    meta.write_text("metadata: {title: t, template: {name: din-6771}}")
    called = {}

    def fake_generate_titlepage(yaml_data, extra_metadata, shared_bom, for_pdf=False):
        called["for_pdf"] = for_pdf
        called["yaml_data"] = yaml_data

    monkeypatch.setattr(
        "filare.flows.index_pages.generate_titlepage", fake_generate_titlepage
    )
    build_titlepage([meta], {"titlepage": tmp_path / "titlepage"}, {"bom": "v"})
    assert called["for_pdf"] is False
    build_titlepage(
        [meta], {"titlepage": tmp_path / "titlepage"}, {"bom": "v"}, for_pdf=True
    )
    assert called["for_pdf"] is True


def test_build_pdf_bundle(monkeypatch, tmp_path):
    html_paths = [tmp_path / "a.html"]
    called = {}

    def fake_generate_pdf_output(paths):
        called["paths"] = paths

    monkeypatch.setattr(
        "filare.flows.index_pages.generate_pdf_output", fake_generate_pdf_output
    )
    build_pdf_bundle(html_paths)
    assert called["paths"] == html_paths
