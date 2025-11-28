import os

from filare.settings import FilareSettings, settings


def test_settings_default_engine_none(monkeypatch):
    monkeypatch.delenv("WV_GRAPHVIZ_ENGINE", raising=False)
    s = FilareSettings()
    assert s.graphviz_engine is None


def test_settings_engine_override(monkeypatch):
    monkeypatch.setenv("WV_GRAPHVIZ_ENGINE", "neato")
    s = FilareSettings()
    assert s.graphviz_engine == "neato"


def test_filare_settings_alias_points_to_filare():
    assert FilareSettings is settings.__class__
