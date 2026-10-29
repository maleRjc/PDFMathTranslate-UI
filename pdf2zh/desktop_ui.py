#!/usr/bin/env python3
"""Entry point for launching PDFMathTranslate Native Desktop UI."""

from __future__ import annotations

import multiprocessing
import sys

from pdf2zh.desktop.main_window import launch_desktop_ui


def main() -> int:
    multiprocessing.freeze_support()
    # Ignore macOS Finder process serial number argument (-psn_*)
    files = [
        arg
        for arg in sys.argv[1:]
        if not arg.startswith("-") and not arg.startswith("-psn_")
    ]
    return launch_desktop_ui(files=files if files else None)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    sys.exit(main())

