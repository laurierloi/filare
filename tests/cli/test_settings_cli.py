import yaml
from typer.testing import CliRunner

from filare.cli import cli
from filare.settings import SettingsStore


def test_settings_path_creates_files(monkeypatch, tmp_path):
    runner = CliRunner()
    monkeypatch.setenv("FIL_CONFIG_PATH", str(tmp_path / "cfg"))

    result = runner.invoke(cli, ["settings", "path", "--create"])
    assert result.exit_code == 0, result.output

    store = SettingsStore()
    user_path = store.path_for_scope("user")
    project_path = store.path_for_scope("project")

    assert user_path.exists()
    assert project_path.exists()
    assert f"user: {user_path}" in result.output
    assert f"project: {project_path}" in result.output


def test_settings_set_show_and_priority(monkeypatch, tmp_path):
    runner = CliRunner()
    monkeypatch.setenv("FIL_CONFIG_PATH", str(tmp_path / "cfg"))

    # Set a config value via CLI (config scope)
    set_result = runner.invoke(
        cli,
        ["settings", "set", "graphviz_engine", "dot", "--scope", "user"],
    )
    assert set_result.exit_code == 0, set_result.output

    # Project override should win over user
    project_result = runner.invoke(
        cli,
        ["settings", "set", "graphviz_engine", "neato", "--scope", "project"],
    )
    assert project_result.exit_code == 0, project_result.output

    show_config = runner.invoke(
        cli,
        ["settings", "show", "--format", "yaml"],
    )
    assert show_config.exit_code == 0, show_config.output
    data = yaml.safe_load(show_config.output)
    assert data["graphviz_engine"] == "neato"
    assert data["config_dir"] == str(tmp_path / "cfg")

    # ENV should override config
    monkeypatch.setenv("WV_GRAPHVIZ_ENGINE", "circo")
    show_env = runner.invoke(
        cli,
        ["settings", "show", "--format", "yaml"],
    )
    assert show_env.exit_code == 0, show_env.output
    env_data = yaml.safe_load(show_env.output)
    assert env_data["graphviz_engine"] == "circo"
    assert env_data["config_dir"] == str(tmp_path / "cfg")


def test_settings_list_append_and_reset(monkeypatch, tmp_path):
    runner = CliRunner()
    monkeypatch.setenv("FIL_CONFIG_PATH", str(tmp_path / "cfg"))

    result_append = runner.invoke(
        cli,
        [
            "settings",
            "set",
            "formats",
            "html,png",
            "--type",
            "list",
            "--append",
        ],
    )
    assert result_append.exit_code == 0, result_append.output

    # Disallow setting config_dir via CLI to avoid desync with active base dir
    result_config_dir = runner.invoke(
        cli,
        [
            "settings",
            "set",
            "config_dir",
            "foo",
        ],
    )
    assert result_config_dir.exit_code != 0
    assert "config_dir is managed" in result_config_dir.output

    show_result = runner.invoke(
        cli,
        ["settings", "show", "--format", "yaml", "--include-defaults"],
    )
    assert show_result.exit_code == 0, show_result.output
    data = yaml.safe_load(show_result.output)
    assert data["formats"] == ["html", "png"]

    reset_result = runner.invoke(
        cli,
        ["settings", "reset", "--yes"],
    )
    assert reset_result.exit_code == 0, reset_result.output

    store = SettingsStore()
    user_data = store.load_scope("user")
    assert user_data == {}
