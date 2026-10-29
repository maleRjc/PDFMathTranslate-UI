#!/bin/zsh
cd "$(dirname "$0")"
if [ -x ".venv/bin/python" ]; then
    exec ".venv/bin/python" -m pdf2zh.desktop_ui "$@"
else
    exec python3 -m pdf2zh.desktop_ui "$@"
fi

