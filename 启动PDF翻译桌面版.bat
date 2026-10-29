@echo off
chcp 65001 >nul
cd /d "%~dp0"

if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" -m pdf2zh.desktop_ui %*
) else if exist ".venv\Scripts\python.exe" (
    start "" ".venv\Scripts\python.exe" -m pdf2zh.desktop_ui %*
) else (
    start "" python -m pdf2zh.desktop_ui %*
)
