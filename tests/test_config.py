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


def test_configure_saves_selected_executable(monkeypatch, tmp_path):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    executable = tmp_path / "ClassicaX.exe"; executable.write_bytes(b"placeholder")
    assert app.configure("x", executable) == executable.resolve()
    assert app.commands()["x"] == [str(executable.resolve())]


def test_portable_x_discovery_with_sibling_directories(monkeypatch, tmp_path):
    portable = tmp_path / "Classica-Homologacao"
    hub = portable / "Hub"
    x = portable / "X"
    hub.mkdir(parents=True)
    x.mkdir()
    binary = x / "ClassicaX.exe"
    binary.write_bytes(b"portable-test")
    monkeypatch.setattr(app.sys, "frozen", True, raising=False)
    monkeypatch.setattr(app.sys, "executable", str(hub / "ClassicaHub.exe"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    assert app.discovered("x") == binary.resolve()


def test_existing_youtube_managed_installation_discovery(monkeypatch, tmp_path):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    first = tmp_path / "Programs" / "Classica" / "versoes" / "Classica-2.2.2"
    second = tmp_path / "Programs" / "Classica" / "versoes" / "Classica-2.2.10"
    for folder in (first, second):
        folder.mkdir(parents=True)
        (folder / "Clássica.exe").write_bytes(b"youtube-test")
    assert app.discovered("youtube") == (second / "Clássica.exe").resolve()
