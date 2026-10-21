from __future__ import annotations

import json
import os
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox


MODULES = {"youtube": "Clássica.exe", "x": "ClassicaX.exe"}


def config_path() -> Path:
    folder = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".local")) / "ClassicaHub"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "modules.json"


def commands() -> dict:
    file = config_path()
    if not file.exists():
        save_commands({"youtube": [], "x": []})
    try:
        value = json.loads(file.read_text(encoding="utf-8"))
        return {name: value.get(name, []) for name in MODULES}
    except json.JSONDecodeError:
        return {name: [] for name in MODULES}


def save_commands(value: dict) -> None:
    file = config_path(); temporary = file.with_suffix(".tmp")
    temporary.write_text(json.dumps({name: value.get(name, []) for name in MODULES}, indent=2), encoding="utf-8")
    temporary.replace(file)


def discovered(module: str) -> Path | None:
    base = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".local")) / "Programs"
    names = {"youtube": ("Classica", "Clássica.exe"), "x": ("ClassicaX", "ClassicaX.exe")}
    folder, executable = names[module]
    candidate = base / folder / executable
    return candidate if candidate.is_file() else None


def configure(module: str, executable: str | Path) -> Path:
    path = Path(executable).expanduser().resolve()
    if not path.is_file() or not path.is_absolute():
        raise ValueError("Selecione um executável de módulo existente.")
    value = commands(); value[module] = [str(path)]; save_commands(value)
    return path


def configured_path(module: str) -> Path | None:
    command = commands()[module]
    if isinstance(command, list) and command and isinstance(command[0], str):
        candidate = Path(command[0]).expanduser()
        if candidate.is_absolute() and candidate.is_file():
            return candidate
    return discovered(module)


def launch(module: str) -> None:
    executable = configured_path(module)
    if not executable:
        raise ValueError(f"O módulo {module} ainda não foi localizado.")
    subprocess.Popen([str(executable)], shell=False, cwd=str(executable.parent))


def choose_module(module: str) -> Path | None:
    path = filedialog.askopenfilename(title=f"Localizar {module}", filetypes=[("Aplicativo Windows", "*.exe")])
    return configure(module, path) if path else None


def main() -> None:
    root = tk.Tk(); root.title("Clássica Hub — ☧ SYSTEMS"); root.geometry("470x300"); root.resizable(False, False)
    tk.Label(root, text="Clássica", font=("Segoe UI", 24, "bold")).pack(pady=(24, 2))
    tk.Label(root, text="Escolha, instale ou localize um aplicativo independente.").pack(pady=(0, 12))
    status = tk.StringVar()
    def refresh():
        found = [name for name in MODULES if configured_path(name)]
        status.set("Módulos localizados: " + (", ".join(found) if found else "nenhum"))
    def pressed(name):
        try:
            if not configured_path(name):
                if not choose_module(name): return
            launch(name)
        except ValueError as exc: messagebox.showerror("Módulo indisponível", str(exc))
        finally: refresh()
    def locate(name):
        try: choose_module(name)
        except ValueError as exc: messagebox.showerror("Localização", str(exc))
        finally: refresh()
    tk.Button(root, text="YouTube", width=28, command=lambda: pressed("youtube")).pack(pady=3)
    tk.Button(root, text="X", width=28, command=lambda: pressed("x")).pack(pady=3)
    actions = tk.Frame(root); actions.pack(pady=10)
    tk.Button(actions, text="Localizar YouTube", command=lambda: locate("youtube")).pack(side=tk.LEFT, padx=4)
    tk.Button(actions, text="Localizar X", command=lambda: locate("x")).pack(side=tk.LEFT, padx=4)
    tk.Label(root, textvariable=status, fg="#586069").pack(pady=3)
    tk.Label(root, text="A localização é salva no Hub; módulos não são copiados, atualizados ou alterados.", fg="#586069").pack(pady=4)
    refresh(); root.mainloop()


if __name__ == "__main__":
    main()
