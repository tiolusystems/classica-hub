import json
from pathlib import Path
from classica_hub import app


def test_commands_initializes_isolated_config(monkeypatch, tmp_path):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert app.commands() == {"youtube": [], "x": []}
    assert json.loads((tmp_path / "ClassicaHub" / "modules.json").read_text()) == {"youtube": [], "x": []}
