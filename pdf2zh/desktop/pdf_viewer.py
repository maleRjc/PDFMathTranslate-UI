"""High-DPI native PDF preview widget powered by PyMuPDF and PySide6."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import pymupdf
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices, QImage, QPixmap
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from pdf2zh.desktop.i18n import tr


def open_file_externally(path: str) -> None:
    if not path or not os.path.exists(path):
        return
    QDesktopServices.openUrl(QUrl.fromLocalFile(path))


def reveal_in_file_manager(path: str) -> None:
    if not path or not os.path.exists(path):
        return
    p = str(Path(path).resolve())
    if sys.platform == "darwin":
        subprocess.Popen(["open", "-R", p])
    elif sys.platform.startswith("win"):
        subprocess.Popen(["explorer", f"/select,{p}"])
    else:
        subprocess.Popen(["xdg-open", str(Path(p).parent)])


class PdfPreviewWidget(QWidget):
    """Embedded PDF viewer supporting Original, Mono, and Dual translated files."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._paths: dict[str, str] = {
            "orig": "",
            "mono": "",
            "dual": "",
        }
        self._active_mode: str = "orig"
        self._doc: Optional[pymupdf.Document] = None
        self._current_page: int = 0
        self._zoom: float = 1.25

        self._setup_ui()
        self.retranslate_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Toolbar
        toolbar = QFrame()
        toolbar.setObjectName("CardFrame")
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(10, 6, 10, 6)
        tb_layout.setSpacing(6)

        # Document variant buttons (Original / Mono / Dual)
        self._mode_group = QButtonGroup(self)
        self._mode_group.setExclusive(True)

        self.btn_orig = QPushButton()
        self.btn_orig.setCheckable(True)
        self.btn_orig.setChecked(True)
        self.btn_orig.setProperty("segButton", True)

        self.btn_mono = QPushButton()
        self.btn_mono.setCheckable(True)
        self.btn_mono.setEnabled(False)
        self.btn_mono.setProperty("segButton", True)

        self.btn_dual = QPushButton()
        self.btn_dual.setCheckable(True)
        self.btn_dual.setEnabled(False)
        self.btn_dual.setProperty("segButton", True)

        self._mode_group.addButton(self.btn_orig, 0)
        self._mode_group.addButton(self.btn_mono, 1)
        self._mode_group.addButton(self.btn_dual, 2)

        self.btn_orig.clicked.connect(lambda: self.switch_variant("orig"))
        self.btn_mono.clicked.connect(lambda: self.switch_variant("mono"))
        self.btn_dual.clicked.connect(lambda: self.switch_variant("dual"))

        tb_layout.addWidget(self.btn_orig)
        tb_layout.addWidget(self.btn_mono)
        tb_layout.addWidget(self.btn_dual)

        tb_layout.addStretch(1)

        # Page navigation
        self.btn_prev = QPushButton("◀")
        self.btn_prev.setFixedWidth(32)
        self.btn_prev.clicked.connect(self.prev_page)

        self.spin_page = QSpinBox()
        self.spin_page.setMinimum(1)
        self.spin_page.setMaximum(1)
        self.spin_page.setFixedWidth(64)
        self.spin_page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_page.valueChanged.connect(self._on_page_spin_changed)

        self.lbl_total_pages = QLabel("/ 0")

        self.btn_next = QPushButton("▶")
        self.btn_next.setFixedWidth(32)
        self.btn_next.clicked.connect(self.next_page)

        tb_layout.addWidget(self.btn_prev)
        tb_layout.addWidget(self.spin_page)
        tb_layout.addWidget(self.lbl_total_pages)
        tb_layout.addWidget(self.btn_next)

        tb_layout.addStretch(1)

        # Zoom controls
        self.btn_zoom_out = QPushButton("－")
        self.btn_zoom_out.setFixedWidth(30)
        self.btn_zoom_out.clicked.connect(lambda: self.adjust_zoom(-0.2))

        self.lbl_zoom = QLabel("125%")
        self.lbl_zoom.setFixedWidth(46)
        self.lbl_zoom.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_zoom_in = QPushButton("＋")
        self.btn_zoom_in.setFixedWidth(30)
        self.btn_zoom_in.clicked.connect(lambda: self.adjust_zoom(0.2))

        self.btn_open_ext = QPushButton()
        self.btn_open_ext.clicked.connect(self.open_current_external)

        self.btn_reveal = QPushButton()
        self.btn_reveal.clicked.connect(self.reveal_current_file)

        tb_layout.addWidget(self.btn_zoom_out)
        tb_layout.addWidget(self.lbl_zoom)
        tb_layout.addWidget(self.btn_zoom_in)
        tb_layout.addWidget(self.btn_open_ext)
        tb_layout.addWidget(self.btn_reveal)

        layout.addWidget(toolbar)

        # Scroll area for PDF page rendering
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setObjectName("PdfScrollArea")

        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_label.setStyleSheet("color: #64748B; font-size: 14px; padding: 40px;")
        self.scroll_area.setWidget(self.page_label)

        layout.addWidget(self.scroll_area, 1)

    def retranslate_ui(self) -> None:
        self.btn_orig.setText(tr("pdf_orig"))
        self.btn_mono.setText(tr("pdf_mono"))
        self.btn_dual.setText(tr("pdf_dual"))
        count = self._doc.page_count if self._doc else 0
        self.lbl_total_pages.setText(tr("pdf_total_pages", count=count))
        self.btn_open_ext.setText(tr("pdf_open_ext"))
        self.btn_open_ext.setToolTip(tr("pdf_open_ext_tip"))
        self.btn_reveal.setText(tr("pdf_reveal"))
        self.btn_reveal.setToolTip(tr("pdf_reveal_tip"))
        if self._doc is None:
            self.page_label.setText(tr("pdf_empty_hint"))

    def set_document_group(
        self,
        orig_path: str = "",
        mono_path: str = "",
        dual_path: str = "",
        prefer_variant: str = "orig",
    ) -> None:
        self._paths["orig"] = orig_path if (orig_path and os.path.exists(orig_path)) else ""
        self._paths["mono"] = mono_path if (mono_path and os.path.exists(mono_path)) else ""
        self._paths["dual"] = dual_path if (dual_path and os.path.exists(dual_path)) else ""

        self.btn_orig.setEnabled(bool(self._paths["orig"]))
        self.btn_mono.setEnabled(bool(self._paths["mono"]))
        self.btn_dual.setEnabled(bool(self._paths["dual"]))

        target = prefer_variant
        if not self._paths.get(target):
            for candidate in ("dual", "mono", "orig"):
                if self._paths.get(candidate):
                    target = candidate
                    break
        self.switch_variant(target)

    def switch_variant(self, variant: str) -> None:
        self._active_mode = variant
        if variant == "orig":
            self.btn_orig.setChecked(True)
        elif variant == "mono":
            self.btn_mono.setChecked(True)
        elif variant == "dual":
            self.btn_dual.setChecked(True)

        file_path = self._paths.get(variant, "")
        self._load_pdf_file(file_path)

    def _load_pdf_file(self, file_path: str) -> None:
        if self._doc is not None:
            try:
                self._doc.close()
            except Exception:
                pass
            self._doc = None

        if not file_path or not os.path.exists(file_path) or not file_path.lower().endswith(".pdf"):
            self.spin_page.blockSignals(True)
            self.spin_page.setMinimum(1)
            self.spin_page.setMaximum(1)
            self.spin_page.setValue(1)
            self.spin_page.blockSignals(False)
            self.lbl_total_pages.setText(tr("pdf_total_pages", count=0))
            self.page_label.setPixmap(QPixmap())
            self.page_label.setText(tr("pdf_empty_hint"))
            return

        try:
            self._doc = pymupdf.open(file_path)
            count = max(1, self._doc.page_count)
            self._current_page = 0
            self.spin_page.blockSignals(True)
            self.spin_page.setMinimum(1)
            self.spin_page.setMaximum(count)
            self.spin_page.setValue(1)
            self.spin_page.blockSignals(False)
            self.lbl_total_pages.setText(tr("pdf_total_pages", count=count))
            self._render_current_page()
        except Exception as exc:
            self.page_label.setPixmap(QPixmap())
            self.page_label.setText(tr("pdf_err_load", err=exc))

    def _render_current_page(self) -> None:
        if self._doc is None or self._doc.page_count == 0:
            return
        page_idx = max(0, min(self._current_page, self._doc.page_count - 1))
        try:
            page = self._doc[page_idx]
            dpr = self.devicePixelRatioF() or 2.0
            scale = self._zoom * dpr
            mat = pymupdf.Matrix(scale, scale)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            qimg = QImage(
                pix.samples,
                pix.width,
                pix.height,
                pix.stride,
                QImage.Format.Format_RGB888,
            ).copy()
            qpix = QPixmap.fromImage(qimg)
            qpix.setDevicePixelRatio(dpr)
            self.page_label.setText("")
            self.page_label.setPixmap(qpix)
        except Exception as exc:
            self.page_label.setPixmap(QPixmap())
            self.page_label.setText(tr("pdf_err_load", err=exc))

    def prev_page(self) -> None:
        if self._doc and self._current_page > 0:
            self._current_page -= 1
            self.spin_page.blockSignals(True)
            self.spin_page.setValue(self._current_page + 1)
            self.spin_page.blockSignals(False)
            self._render_current_page()

    def next_page(self) -> None:
        if self._doc and self._current_page + 1 < self._doc.page_count:
            self._current_page += 1
            self.spin_page.blockSignals(True)
            self.spin_page.setValue(self._current_page + 1)
            self.spin_page.blockSignals(False)
            self._render_current_page()

    def _on_page_spin_changed(self, val: int) -> None:
        if self._doc:
            self._current_page = max(0, min(val - 1, self._doc.page_count - 1))
            self._render_current_page()

    def adjust_zoom(self, delta: float) -> None:
        self._zoom = max(0.5, min(3.0, round(self._zoom + delta, 2)))
        self.lbl_zoom.setText(f"{int(self._zoom * 100)}%")
        self._render_current_page()

    def current_file_path(self) -> str:
        return self._paths.get(self._active_mode, "") or self._paths.get("orig", "")

    def open_current_external(self) -> None:
        open_file_externally(self.current_file_path())

    def reveal_current_file(self) -> None:
        reveal_in_file_manager(self.current_file_path())
