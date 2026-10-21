param([string]$Python = "python")
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
& $Python -m PyInstaller --noconfirm --clean --onedir --name ClassicaHub scripts\hub_entry.py
