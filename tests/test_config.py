import json
import pytest
from classica_hub import app


def test_commands_initializes_isolated_config(monkeypatch, tmp_path):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert app.commands() == {"youtube": [], "x": []}
    assert json.loads((tmp_path / "ClassicaHub" / "modules.json").read_text()) == {"youtube": [], "x": []}


def test_launch_rejects_relative_executable(monkeypatch):
    monkeypatch.setattr(app, "commands", lambda: {"youtube": ["Classica.exe"], "x": []})
    with pytest.raises(ValueError):
        app.launch("youtube")
