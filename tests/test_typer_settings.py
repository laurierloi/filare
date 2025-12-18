from filare.settings.typer import TyperSettings, typer_kwargs


def test_typer_settings_defaults():
    settings = TyperSettings()
    assert settings.rich_markup_mode == "rich"
    assert settings.pretty_exceptions_enable is True
    assert settings.pretty_exceptions_show_locals is False
    assert settings.pretty_exceptions_short is False
    assert settings.add_completion is True
    assert settings.no_args_is_help is True


def test_typer_settings_env_override(monkeypatch):
    monkeypatch.setenv("FIL_TYPER_RICH_MARKUP_MODE", "")
    monkeypatch.setenv("FIL_TYPER_PRETTY_EXCEPTIONS_ENABLE", "false")
    monkeypatch.setenv("FIL_TYPER_PRETTY_EXCEPTIONS_SHOW_LOCALS", "true")
    settings = TyperSettings()
    assert settings.rich_markup_mode == ""
    assert settings.pretty_exceptions_enable is False
    assert settings.pretty_exceptions_show_locals is True


def test_typer_kwargs_filters_none(monkeypatch):
    monkeypatch.setenv("FIL_TYPER_RICH_MARKUP_MODE", "")
    kwargs = typer_kwargs()
    # Empty string is allowed; ensure keys with None would be dropped if present.
    assert kwargs["rich_markup_mode"] == ""
    assert "nonexistent" not in kwargs
