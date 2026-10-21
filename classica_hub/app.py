from __future__ import annotations

import json
import os
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


def config_path() -> Path:
    folder = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".local")) / "ClassicaHub"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "modules.json"


def commands() -> dict:
    file = config_path()
    if not file.exists():
        file.write_text(json.dumps({"youtube": [], "x": []}, indent=2), encoding="utf-8")
    try:
        value = json.loads(file.read_text(encoding="utf-8"))
        return {name: value.get(name, []) for name in ("youtube", "x")}
    except json.JSONDecodeError:
        return {"youtube": [], "x": []}


def launch(module: str) -> None:
    command = commands()[module]
    if not isinstance(command, list) or not command or not all(isinstance(x, str) for x in command):
        raise ValueError(f"Configure o comando do módulo {module} em {config_path()}.")
    executable = Path(command[0]).expanduser()
    if not executable.is_absolute() or not executable.is_file():
        raise ValueError(f"Módulo {module} não encontrado: {executable}")
    subprocess.Popen([str(executable), *command[1:]], shell=False, cwd=str(executable.parent))


def main() -> None:
    root = tk.Tk(); root.title("Clássica Hub — ☧ SYSTEMS"); root.geometry("420x230"); root.resizable(False, False)
    tk.Label(root, text="Clássica", font=("Segoe UI", 24, "bold")).pack(pady=(30, 4))
    tk.Label(root, text="Escolha um aplicativo independente").pack(pady=(0, 18))
    def pressed(name):
        try: launch(name)
        except ValueError as exc: messagebox.showerror("Módulo indisponível", str(exc))
    tk.Button(root, text="YouTube", width=28, command=lambda: pressed("youtube")).pack(pady=4)
    tk.Button(root, text="X", width=28, command=lambda: pressed("x")).pack(pady=4)
    tk.Label(root, text="O Hub não atualiza nem altera os módulos.", fg="#586069").pack(pady=15)
    root.mainloop()

if __name__ == "__main__": main()
