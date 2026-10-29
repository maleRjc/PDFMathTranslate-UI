#!/usr/bin/env python3
"""Entry point for launching PDFMathTranslate Native Desktop UI."""

from __future__ import annotations

import sys
from pdf2zh.desktop.main_window import launch_desktop_ui


def main() -> int:
    files = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    return launch_desktop_ui(files=files if files else None)


if __name__ == "__main__":
    sys.exit(main())

