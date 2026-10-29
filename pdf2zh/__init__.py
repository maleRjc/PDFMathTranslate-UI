import logging
import os
import sys
from typing import Any


class _NullWriter:
    """Safe dummy writer for GUI environments (e.g. pythonw) where stdout/stderr are None."""

    def write(self, s: Any) -> int:
        return len(s) if s else 0

    def flush(self) -> None:
        pass

    def isatty(self) -> bool:
        return False


def ensure_valid_std_streams() -> None:
    """Ensure sys.stdin, sys.stdout, and sys.stderr are valid stream objects with .write()/.read()."""
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        if stream is None or not hasattr(stream, "write"):
            try:
                setattr(sys, name, open(os.devnull, "w", encoding="utf-8"))
            except Exception:
                setattr(sys, name, _NullWriter())
    if sys.stdin is None or not hasattr(sys.stdin, "read"):
        try:
            sys.stdin = open(os.devnull, "r", encoding="utf-8")
        except Exception:
            import io

            sys.stdin = io.StringIO("")


ensure_valid_std_streams()

log = logging.getLogger(__name__)

__version__ = "1.9.12"
__author__ = "Byaidu"
__all__ = [
    "translate",
    "translate_stream",
    "translate_document_outlines",
    "translate_pdf_file_outlines",
    "ensure_valid_std_streams",
]


def __getattr__(name):
    if name in {
        "translate",
        "translate_stream",
        "translate_document_outlines",
        "translate_pdf_file_outlines",
    }:
        import pdf2zh.high_level as _hl

        return getattr(_hl, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

