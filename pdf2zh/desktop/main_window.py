"""Main Window and Translate Workspace for PDFMathTranslate Native Desktop App."""

from __future__ import annotations

import os
from typing import Any, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pdf2zh import __version__
from pdf2zh.desktop.i18n import (
    UI_LANGUAGES,
    I18nManager,
    get_localized_lang_label,
    tr,
)
from pdf2zh.desktop.metadata import (
    CODE_TO_LANG_LABEL,
    LANG_MAP,
    PROVIDER_METADATA,
    SERVICE_MAP,
    AppSettings,
    get_provider_envs,
    is_provider_configured,
)
from pdf2zh.desktop.pdf_viewer import PdfPreviewWidget, reveal_in_file_manager
from pdf2zh.desktop.settings_pages import (
    AIProvidersPage,
    HelpGuidePage,
    OutputSettingsPage,
    SystemSettingsPage,
    TranslationSettingsPage,
)
from pdf2zh.desktop.workers import TranslationQueueWorker, parse_page_range_string

APP_STYLESHEET = """
QMainWindow, QWidget {
    background-color: #F8FAFC;
    color: #0F172A;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif;
    font-size: 13px;
}

#Sidebar {
    background-color: #0F172A;
    border-right: 1px solid #1E293B;
}

#SidebarTitle {
    color: #F8FAFC;
    font-size: 16px;
    font-weight: 700;
}

#SidebarSubtitle {
    color: #94A3B8;
    font-size: 11px;
}

QPushButton[navBtn="true"] {
    background-color: transparent;
    color: #CBD5E1;
    border: none;
    border-radius: 8px;
    text-align: left;
    padding: 10px 14px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton[navBtn="true"]:hover {
    background-color: #1E293B;
    color: #FFFFFF;
}

QPushButton[navBtn="true"]:checked {
    background-color: #2563EB;
    color: #FFFFFF;
    font-weight: 600;
}

#SidebarStatusCard {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 8px;
}

#CardFrame {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
}

#CardTitle {
    color: #0F172A;
    font-size: 15px;
    font-weight: 700;
    background: transparent;
}

#CardSubtitle {
    color: #64748B;
    font-size: 12px;
    background: transparent;
}

#BadgeLabel {
    background-color: #EFF6FF;
    color: #1D4ED8;
    border: 1px solid #BFDBFE;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 600;
}

#DropZoneFrame {
    background-color: #F8FAFC;
    border: 1.5px dashed #3B82F6;
    border-radius: 10px;
}

QLineEdit, QComboBox, QSpinBox, QPlainTextEdit {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 6px 10px;
    color: #0F172A;
    selection-background-color: #2563EB;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QPlainTextEdit:focus {
    border: 1.5px solid #2563EB;
}

QPushButton {
    background-color: #FFFFFF;
    color: #1E293B;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 6px 12px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #F1F5F9;
    border-color: #94A3B8;
}

QPushButton:disabled {
    background-color: #F1F5F9;
    color: #94A3B8;
    border-color: #E2E8F0;
}

QPushButton#PrimaryButton {
    background-color: #2563EB;
    color: #FFFFFF;
    border: 1px solid #1D4ED8;
    font-weight: 600;
    padding: 8px 16px;
}

QPushButton#PrimaryButton:hover {
    background-color: #1D4ED8;
}

QPushButton#PrimaryButton:disabled {
    background-color: #93C5FD;
    border-color: #93C5FD;
}

QPushButton#DangerButton {
    background-color: #FEE2E2;
    color: #B91C1C;
    border: 1px solid #FECACA;
    font-weight: 600;
}

QPushButton#DangerButton:hover {
    background-color: #FECACA;
}

QPushButton[segButton="true"] {
    border-radius: 6px;
    padding: 5px 12px;
}

QPushButton[segButton="true"]:checked {
    background-color: #2563EB;
    color: #FFFFFF;
    border-color: #1D4ED8;
    font-weight: 600;
}

QListWidget#ProviderList {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    outline: none;
}

QListWidget#ProviderList::item {
    padding: 9px 10px;
    border-bottom: 1px solid #F1F5F9;
    border-radius: 6px;
}

QListWidget#ProviderList::item:selected {
    background-color: #EFF6FF;
    color: #1D4ED8;
    font-weight: 600;
}

QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    gridline-color: #F1F5F9;
    selection-background-color: #EFF6FF;
    selection-color: #1E3A8A;
}

QHeaderView::section {
    background-color: #F8FAFC;
    color: #475569;
    font-weight: 600;
    border: none;
    border-bottom: 1px solid #E2E8F0;
    padding: 6px 8px;
}

QProgressBar {
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    background-color: #F1F5F9;
    text-align: center;
    height: 18px;
    font-weight: 600;
    color: #0F172A;
}

QProgressBar::chunk {
    background-color: #2563EB;
    border-radius: 5px;
}

#PdfScrollArea {
    background-color: #E2E8F0;
    border: 1px solid #CBD5E1;
    border-radius: 10px;
}
"""


class WorkspacePage(QWidget):
    """Main translation workspace with batch queue, quick options, and side-by-side PDF preview."""

    request_open_ai_settings = Signal(str)  # service_key
    request_open_guide = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self._tasks: list[dict[str, Any]] = []
        self._worker: Optional[TranslationQueueWorker] = None
        self._setup_ui()
        self.retranslate_ui()
        self.sync_from_settings()

    def _setup_ui(self) -> None:
        root = QHBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(14)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # Left column: Queue + Quick Options + Controls + Logs
        left_widget = QWidget()
        left_widget.setMinimumWidth(460)
        left_widget.setMaximumWidth(610)
        left_vbox = QVBoxLayout(left_widget)
        left_vbox.setContentsMargins(0, 0, 0, 0)
        left_vbox.setSpacing(12)

        # 1. File Queue Card
        queue_card = QFrame()
        queue_card.setObjectName("CardFrame")
        q_vbox = QVBoxLayout(queue_card)
        q_vbox.setContentsMargins(14, 12, 14, 12)
        q_vbox.setSpacing(8)

        # Dropzone header + add buttons
        drop_banner = QFrame()
        drop_banner.setObjectName("DropZoneFrame")
        drop_layout = QHBoxLayout(drop_banner)
        drop_layout.setContentsMargins(12, 8, 12, 8)
        self.lbl_drop = QLabel()
        self.lbl_drop.setStyleSheet("color: #1D4ED8; font-weight: 600; background: transparent;")
        drop_layout.addWidget(self.lbl_drop, 1)

        self.btn_add_files = QPushButton()
        self.btn_add_files.clicked.connect(self.add_files_dialog)
        self.btn_add_dir = QPushButton()
        self.btn_add_dir.clicked.connect(self.add_folder_dialog)
        self.btn_add_url = QPushButton()
        self.btn_add_url.clicked.connect(self.add_url_dialog)
        self.btn_clear_queue = QPushButton()
        self.btn_clear_queue.clicked.connect(self.clear_queue)

        drop_layout.addWidget(self.btn_add_files)
        drop_layout.addWidget(self.btn_add_dir)
        drop_layout.addWidget(self.btn_add_url)
        drop_layout.addWidget(self.btn_clear_queue)
        q_vbox.addWidget(drop_banner)

        # Task table
        self.table = QTableWidget(0, 4)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(2, 80)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 68)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(145)
        self.table.itemSelectionChanged.connect(self._on_table_selection_changed)
        q_vbox.addWidget(self.table, 1)

        left_vbox.addWidget(queue_card, 1)

        # 2. Quick Translation Options Card
        opt_card = QFrame()
        opt_card.setObjectName("CardFrame")
        opt_vbox = QVBoxLayout(opt_card)
        opt_vbox.setContentsMargins(14, 12, 14, 12)
        opt_vbox.setSpacing(10)

        opt_header = QHBoxLayout()
        self.lbl_opt_title = QLabel()
        self.lbl_opt_title.setObjectName("CardTitle")
        opt_header.addWidget(self.lbl_opt_title)
        opt_header.addStretch(1)
        self.lbl_service_status = QLabel("")
        opt_header.addWidget(self.lbl_service_status)
        opt_vbox.addLayout(opt_header)

        form = QFormLayout()
        form.setSpacing(8)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # Service + Configure Key button
        svc_row = QHBoxLayout()
        self.combo_service = QComboBox()
        self.combo_service.addItems(list(SERVICE_MAP.keys()))
        self.combo_service.currentTextChanged.connect(self._on_service_changed)

        self.btn_cfg_key = QPushButton()
        self.btn_cfg_key.clicked.connect(
            lambda: self.request_open_ai_settings.emit(self.combo_service.currentText())
        )
        svc_row.addWidget(self.combo_service, 1)
        svc_row.addWidget(self.btn_cfg_key)
        self.lbl_ai_service = QLabel()
        form.addRow(self.lbl_ai_service, svc_row)

        # Model override combo
        self.combo_model = QComboBox()
        self.combo_model.setEditable(True)
        self.lbl_model = QLabel()
        form.addRow(self.lbl_model, self.combo_model)

        # Source & Target language row
        lang_row = QHBoxLayout()
        self.combo_lang_from = QComboBox()
        self.btn_swap_lang = QPushButton("⇄")
        self.btn_swap_lang.setFixedWidth(34)
        self.btn_swap_lang.clicked.connect(self._swap_languages)
        self.combo_lang_to = QComboBox()
        for label_zh, code in LANG_MAP.items():
            self.combo_lang_from.addItem(label_zh, code)
            self.combo_lang_to.addItem(label_zh, code)
        lang_row.addWidget(self.combo_lang_from, 1)
        lang_row.addWidget(self.btn_swap_lang)
        lang_row.addWidget(self.combo_lang_to, 1)
        self.lbl_trans_lang = QLabel()
        form.addRow(self.lbl_trans_lang, lang_row)

        # Page range
        page_row = QHBoxLayout()
        self.combo_pages = QComboBox()
        self.combo_pages.addItems(["", "", "", ""])
        self.combo_pages.currentIndexChanged.connect(self._on_page_mode_changed)
        self.edit_pages = QLineEdit()
        self.edit_pages.setVisible(False)
        page_row.addWidget(self.combo_pages, 1)
        page_row.addWidget(self.edit_pages, 1)
        self.lbl_page_range = QLabel()
        form.addRow(self.lbl_page_range, page_row)

        # Engine Mode
        self.combo_mode = QComboBox()
        self.combo_mode.addItem("", "fast")
        self.combo_mode.addItem("", "ultrafast")
        self.combo_mode.addItem("", "babeldoc")
        self.combo_mode.addItem("", "precise")
        self.lbl_engine_mode = QLabel()
        form.addRow(self.lbl_engine_mode, self.combo_mode)

        # Checkboxes row
        chk_row = QHBoxLayout()
        self.chk_mono = QCheckBox()
        self.chk_dual = QCheckBox()
        self.chk_ignore_cache = QCheckBox()
        chk_row.addWidget(self.chk_mono)
        chk_row.addWidget(self.chk_dual)
        chk_row.addWidget(self.chk_ignore_cache)
        chk_row.addStretch(1)
        self.lbl_output_opt = QLabel()
        form.addRow(self.lbl_output_opt, chk_row)

        opt_vbox.addLayout(form)
        left_vbox.addWidget(opt_card)

        # 3. Action & Progress Card
        act_card = QFrame()
        act_card.setObjectName("CardFrame")
        act_vbox = QVBoxLayout(act_card)
        act_vbox.setContentsMargins(14, 12, 14, 12)
        act_vbox.setSpacing(8)

        btn_bar = QHBoxLayout()
        self.btn_start = QPushButton()
        self.btn_start.setObjectName("PrimaryButton")
        self.btn_start.setMinimumHeight(38)
        self.btn_start.clicked.connect(self.start_translation)

        self.btn_stop = QPushButton()
        self.btn_stop.setObjectName("DangerButton")
        self.btn_stop.setMinimumHeight(38)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_translation)

        self.btn_toggle_log = QPushButton()
        self.btn_toggle_log.setCheckable(True)
        self.btn_toggle_log.setMinimumHeight(38)
        self.btn_toggle_log.toggled.connect(self._toggle_log_box)

        self.btn_help_quick = QPushButton()
        self.btn_help_quick.setMinimumHeight(38)
        self.btn_help_quick.clicked.connect(self.request_open_guide.emit)

        btn_bar.addWidget(self.btn_start, 1)
        btn_bar.addWidget(self.btn_stop)
        btn_bar.addWidget(self.btn_toggle_log)
        btn_bar.addWidget(self.btn_help_quick)
        act_vbox.addLayout(btn_bar)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        act_vbox.addWidget(self.progress_bar)

        self.lbl_progress_desc = QLabel()
        self.lbl_progress_desc.setObjectName("CardSubtitle")
        act_vbox.addWidget(self.lbl_progress_desc)

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setMaximumHeight(130)
        self.log_box.setVisible(False)
        self.log_box.setStyleSheet(
            "font-family: Menlo, Monaco, Consolas, monospace; font-size: 11px; "
            "background: #0F172A; color: #E2E8F0; border-radius: 6px; padding: 6px;"
        )
        act_vbox.addWidget(self.log_box)

        left_vbox.addWidget(act_card)

        splitter.addWidget(left_widget)

        # Right column: PDF Previewer
        self.pdf_viewer = PdfPreviewWidget()
        splitter.addWidget(self.pdf_viewer)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        root.addWidget(splitter)

    def retranslate_ui(self) -> None:
        self.lbl_drop.setText(tr("drop_hint"))
        self.btn_add_files.setText(tr("btn_add_file"))
        self.btn_add_dir.setText(tr("btn_add_folder"))
        self.btn_add_url.setText(tr("btn_add_url"))
        self.btn_clear_queue.setText(tr("btn_clear"))

        self.table.setHorizontalHeaderLabels(
            [tr("col_filename"), tr("col_status"), tr("col_progress"), tr("col_time")]
        )
        for row_idx, t in enumerate(self._tasks):
            st = t.get("status", "pending")
            key = {
                "pending": "status_pending",
                "running": "status_running",
                "done": "status_done",
                "failed": "status_failed",
            }.get(st, "status_pending")
            if self.table.item(row_idx, 1):
                self.table.item(row_idx, 1).setText(tr(key))

        self.lbl_opt_title.setText(tr("opt_card_title"))
        self.lbl_ai_service.setText(tr("lbl_ai_service"))
        self.btn_cfg_key.setText(tr("btn_cfg_key"))
        self.btn_cfg_key.setToolTip(tr("tip_cfg_key"))
        self.lbl_model.setText(tr("lbl_model"))
        self.lbl_trans_lang.setText(tr("lbl_trans_lang"))
        self.btn_swap_lang.setToolTip(tr("tip_swap_lang"))
        for i in range(self.combo_lang_from.count()):
            code = self.combo_lang_from.itemData(i)
            if code:
                self.combo_lang_from.setItemText(i, get_localized_lang_label(str(code)))
        for i in range(self.combo_lang_to.count()):
            code = self.combo_lang_to.itemData(i)
            if code:
                self.combo_lang_to.setItemText(i, get_localized_lang_label(str(code)))
        self.lbl_page_range.setText(tr("lbl_page_range"))

        self.combo_pages.setItemText(0, tr("pages_all"))
        self.combo_pages.setItemText(1, tr("pages_first"))
        self.combo_pages.setItemText(2, tr("pages_first5"))
        self.combo_pages.setItemText(3, tr("pages_custom"))
        self.edit_pages.setPlaceholderText(tr("pages_custom_ph"))

        self.lbl_engine_mode.setText(tr("lbl_engine_mode"))
        self.combo_mode.setItemText(0, tr("mode_fast_short"))
        self.combo_mode.setItemText(1, tr("mode_ultrafast_short"))
        self.combo_mode.setItemText(2, tr("mode_babeldoc_short"))
        self.combo_mode.setItemText(3, tr("mode_precise_short"))

        self.lbl_output_opt.setText(tr("lbl_output_opt"))
        self.chk_mono.setText(tr("chk_mono_short"))
        self.chk_dual.setText(tr("chk_dual_short"))
        self.chk_ignore_cache.setText(tr("chk_ignore_cache_short"))

        self.btn_start.setText(tr("btn_start"))
        self.btn_stop.setText(tr("btn_stop"))
        self.btn_toggle_log.setText(tr("btn_log"))
        self.btn_help_quick.setText(tr("btn_help_quick"))

        if not (self._worker and self._worker.isRunning()):
            self.lbl_progress_desc.setText(tr("prog_ready"))

        self._on_service_changed(self.combo_service.currentText())
        self.pdf_viewer.retranslate_ui()

    # --- Drag & Drop Support ---
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        for url in event.mimeData().urls():
            local_path = url.toLocalFile()
            if not local_path:
                continue
            if os.path.isdir(local_path):
                self._add_directory_files(local_path)
            elif local_path.lower().endswith((".pdf", ".doc", ".docx")):
                self._append_task(local_path)

    # --- Queue Management ---
    def add_files_dialog(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
            self,
            tr("menu_add_files"),
            "",
            "Documents (*.pdf *.doc *.docx);;PDF Files (*.pdf);;All Files (*)",
        )
        for f in files:
            self._append_task(f)

    def add_folder_dialog(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, tr("menu_add_folder"))
        if folder:
            self._add_directory_files(folder)

    def _add_directory_files(self, folder: str) -> None:
        added = 0
        for root_dir, _, files in os.walk(folder):
            for fname in sorted(files):
                if fname.lower().endswith((".pdf", ".doc", ".docx")) and not fname.lower().endswith(
                    ("-mono.pdf", "-dual.pdf")
                ):
                    self._append_task(os.path.join(root_dir, fname))
                    added += 1
        if added == 0:
            QMessageBox.information(self, "Info", tr("msg_no_pdf_in_dir"))

    def add_url_dialog(self) -> None:
        url, ok = QInputDialog.getText(
            self,
            tr("dlg_add_url_title"),
            tr("dlg_add_url_label"),
        )
        if ok and url.strip():
            self._append_task(url.strip())

    def _append_task(self, path: str) -> None:
        for existing in self._tasks:
            if existing["path"] == path:
                return
        row = self.table.rowCount()
        self.table.insertRow(row)

        display_name = os.path.basename(path) or path
        item_name = QTableWidgetItem(display_name)
        item_name.setToolTip(path)
        item_status = QTableWidgetItem(tr("status_pending"))
        item_prog = QTableWidgetItem("0%")
        item_time = QTableWidgetItem("-")

        self.table.setItem(row, 0, item_name)
        self.table.setItem(row, 1, item_status)
        self.table.setItem(row, 2, item_prog)
        self.table.setItem(row, 3, item_time)

        task_info = {
            "row": row,
            "path": path,
            "mono": "",
            "dual": "",
            "status": "pending",
        }
        self._tasks.append(task_info)

        if self.table.rowCount() == 1:
            self.table.selectRow(0)

    def clear_queue(self) -> None:
        if self._worker and self._worker.isRunning():
            QMessageBox.warning(self, "Warning", tr("msg_stop_first"))
            return
        self.table.setRowCount(0)
        self._tasks.clear()
        self.pdf_viewer.set_document_group()

    def _on_table_selection_changed(self) -> None:
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return
        idx = rows[0].row()
        if 0 <= idx < len(self._tasks):
            t = self._tasks[idx]
            prefer = "dual" if t["dual"] else ("mono" if t["mono"] else "orig")
            self.pdf_viewer.set_document_group(
                orig_path=t["path"],
                mono_path=t["mono"],
                dual_path=t["dual"],
                prefer_variant=prefer,
            )

    # --- Options Synchronization ---
    def sync_from_settings(self) -> None:
        default_svc = AppSettings.get("PDF2ZH_DEFAULT_SERVICE", "Bing")
        if default_svc in SERVICE_MAP:
            self.combo_service.setCurrentText(default_svc)
        self._on_service_changed(self.combo_service.currentText())

        lang_from_code = AppSettings.get("PDF2ZH_LANG_FROM_CODE", "en")
        lang_to_code = AppSettings.get("PDF2ZH_LANG_TO_CODE", "zh")
        idx_from = self.combo_lang_from.findData(lang_from_code)
        if idx_from >= 0:
            self.combo_lang_from.setCurrentIndex(idx_from)
        idx_to = self.combo_lang_to.findData(lang_to_code)
        if idx_to >= 0:
            self.combo_lang_to.setCurrentIndex(idx_to)

        mode = AppSettings.get("PDF2ZH_DEFAULT_MODE", "fast")
        idx = self.combo_mode.findData(mode)
        if idx >= 0:
            self.combo_mode.setCurrentIndex(idx)

        self.chk_mono.setChecked(bool(AppSettings.get("PDF2ZH_GEN_MONO", True)))
        self.chk_dual.setChecked(bool(AppSettings.get("PDF2ZH_GEN_DUAL", True)))
        self.chk_ignore_cache.setChecked(bool(AppSettings.get("PDF2ZH_IGNORE_CACHE", False)))

    def _on_service_changed(self, service_key: str) -> None:
        if not service_key or service_key not in SERVICE_MAP:
            return
        ready, status_text = is_provider_configured(service_key)
        if ready:
            self.lbl_service_status.setText(f"🟢 {status_text}")
            self.lbl_service_status.setStyleSheet("color: #15803D; font-weight: 600;")
        else:
            self.lbl_service_status.setText(f"⚠️ {status_text}")
            self.lbl_service_status.setStyleSheet("color: #D97706; font-weight: 600;")

        envs = get_provider_envs(service_key)
        meta = PROVIDER_METADATA.get(service_key, {})
        suggested = list(meta.get("models", []))

        configured_model = ""
        for k, v in envs.items():
            if k.upper().endswith("MODEL") and v:
                configured_model = v
                break

        self.combo_model.blockSignals(True)
        self.combo_model.clear()
        if configured_model and configured_model not in suggested:
            suggested.insert(0, configured_model)
        if suggested:
            self.combo_model.addItems(suggested)
            self.combo_model.setCurrentText(configured_model or suggested[0])
            self.combo_model.setEnabled(True)
        else:
            self.combo_model.addItem(tr("model_default_none"))
            self.combo_model.setEnabled(False)
        self.combo_model.blockSignals(False)

    def _swap_languages(self) -> None:
        idx_a = self.combo_lang_from.currentIndex()
        idx_b = self.combo_lang_to.currentIndex()
        self.combo_lang_from.setCurrentIndex(idx_b)
        self.combo_lang_to.setCurrentIndex(idx_a)

    def _on_page_mode_changed(self, idx: int) -> None:
        self.edit_pages.setVisible(idx == 3)

    def _toggle_log_box(self, checked: bool) -> None:
        self.log_box.setVisible(checked)

    # --- Start / Stop Translation ---
    def start_translation(self) -> None:
        if not self._tasks:
            QMessageBox.information(self, "Info", tr("msg_no_files"))
            return

        service_key = self.combo_service.currentText()
        ready, _ = is_provider_configured(service_key)
        if not ready:
            ans = QMessageBox.question(
                self,
                tr("msg_unconfigured_title"),
                tr("msg_unconfigured_body", svc=service_key),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if ans == QMessageBox.StandardButton.Yes:
                self.request_open_ai_settings.emit(service_key)
            return

        if not self.chk_mono.isChecked() and not self.chk_dual.isChecked():
            self.chk_dual.setChecked(True)

        # Parse pages
        page_idx = self.combo_pages.currentIndex()
        pages: Optional[list[int]] = None
        raw_pages_str = ""
        if page_idx == 1:
            pages = [0]
            raw_pages_str = "1"
        elif page_idx == 2:
            pages = list(range(0, 5))
            raw_pages_str = "1-5"
        elif page_idx == 3:
            try:
                raw_pages_str = self.edit_pages.text().strip()
                pages = parse_page_range_string(raw_pages_str)
            except Exception as exc:
                QMessageBox.warning(self, "Error", str(exc))
                return

        model_override = (
            self.combo_model.currentText().strip() if self.combo_model.isEnabled() else ""
        )
        use_custom_prompt = bool(AppSettings.get("PDF2ZH_USE_CUSTOM_PROMPT", False))
        custom_prompt = (
            str(AppSettings.get("PDF2ZH_CUSTOM_PROMPT", "")).strip()
            if use_custom_prompt
            else ""
        )

        options = {
            "service_key": service_key,
            "model_override": model_override,
            "lang_in": self.combo_lang_from.currentData()
            or LANG_MAP.get(self.combo_lang_from.currentText(), "en"),
            "lang_out": self.combo_lang_to.currentData()
            or LANG_MAP.get(self.combo_lang_to.currentText(), "zh"),
            "mode": self.combo_mode.currentData(),
            "pages": pages,
            "raw_pages_str": raw_pages_str,
            "threads": int(AppSettings.get("PDF2ZH_THREADS", 4)),
            "vfont": str(AppSettings.get("PDF2ZH_VFONT", "")),
            "vchar": str(AppSettings.get("PDF2ZH_VCHAR", "")),
            "prompt": custom_prompt,
            "skip_subset_fonts": bool(AppSettings.get("PDF2ZH_SKIP_SUBSET_FONTS", False)),
            "compatible": bool(AppSettings.get("PDF2ZH_COMPATIBLE_PDFA", False)),
            "ignore_cache": self.chk_ignore_cache.isChecked(),
            "gen_mono": self.chk_mono.isChecked(),
            "gen_dual": self.chk_dual.isChecked(),
            "output_dir": str(AppSettings.get("PDF2ZH_OUTPUT_DIR", "")),
            "save_next_to_source": bool(AppSettings.get("PDF2ZH_SAVE_NEXT_TO_SOURCE", True)),
        }

        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.progress_bar.setValue(0)
        self.log_box.clear()

        self._worker = TranslationQueueWorker(self._tasks, options, self)
        self._worker.task_started.connect(self._on_task_started)
        self._worker.task_progress.connect(self._on_task_progress)
        self._worker.task_finished.connect(self._on_task_finished)
        self._worker.task_failed.connect(self._on_task_failed)
        self._worker.log_message.connect(self._append_log)
        self._worker.queue_finished.connect(self._on_queue_finished)
        self._worker.start()

    def stop_translation(self) -> None:
        if self._worker and self._worker.isRunning():
            self.lbl_progress_desc.setText(tr("prog_stopping"))
            self._worker.cancel()

    def _on_task_started(self, row: int, path: str) -> None:
        if 0 <= row < len(self._tasks):
            self._tasks[row]["status"] = "running"
        self.table.item(row, 1).setText(tr("status_running"))
        self.table.item(row, 2).setText("1%")
        self.lbl_progress_desc.setText(tr("prog_processing", name=os.path.basename(path)))
        self.table.selectRow(row)

    def _on_task_progress(self, row: int, pct: int, desc: str) -> None:
        self.table.item(row, 2).setText(f"{pct}%")
        self.progress_bar.setValue(pct)
        self.lbl_progress_desc.setText(desc)

    def _on_task_finished(
        self, row: int, mono_path: str, dual_path: str, elapsed: float
    ) -> None:
        self.table.item(row, 1).setText(tr("status_done"))
        self.table.item(row, 2).setText("100%")
        self.table.item(row, 3).setText(f"{elapsed:.1f}s")

        if 0 <= row < len(self._tasks):
            self._tasks[row]["mono"] = mono_path
            self._tasks[row]["dual"] = dual_path
            self._tasks[row]["status"] = "done"

        if bool(AppSettings.get("PDF2ZH_AUTO_PREVIEW", True)):
            prefer = "dual" if dual_path else "mono"
            self.pdf_viewer.set_document_group(
                orig_path=self._tasks[row]["path"],
                mono_path=mono_path,
                dual_path=dual_path,
                prefer_variant=prefer,
            )

    def _on_task_failed(self, row: int, error_msg: str) -> None:
        if 0 <= row < len(self._tasks):
            self._tasks[row]["status"] = "failed"
        self.table.item(row, 1).setText(tr("status_failed"))
        self.table.item(row, 1).setToolTip(error_msg)
        self.lbl_progress_desc.setText(tr("prog_error", err=error_msg[:90]))
        self.btn_toggle_log.setChecked(True)

    def _on_queue_finished(self) -> None:
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.progress_bar.setValue(100)
        self.lbl_progress_desc.setText(tr("prog_all_done"))

        if bool(AppSettings.get("PDF2ZH_AUTO_OPEN_DIR", False)) and self._tasks:
            last = self._tasks[-1]
            target = last.get("dual") or last.get("mono") or last.get("path")
            if target and os.path.exists(target):
                reveal_in_file_manager(target)

    def _append_log(self, msg: str) -> None:
        self.log_box.appendPlainText(msg)


class MainWindow(QMainWindow):
    """Top-level desktop window for PDFMathTranslate with sidebar navigation, multi-language switcher, and user guide."""

    def __init__(self, initial_files: Optional[list[str]] = None):
        super().__init__()
        self.resize(1340, 850)
        self.setMinimumSize(1020, 680)
        self.setStyleSheet(APP_STYLESHEET)

        AppSettings.apply_runtime_settings()
        self._setup_ui()
        self._setup_menubar()
        self.retranslate_ui()

        if initial_files:
            for f in initial_files:
                if os.path.exists(f):
                    self.page_workspace._append_task(f)

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        main_hbox = QHBoxLayout(central)
        main_hbox.setContentsMargins(0, 0, 0, 0)
        main_hbox.setSpacing(0)

        # Left Navigation Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(232)
        sb_vbox = QVBoxLayout(sidebar)
        sb_vbox.setContentsMargins(14, 20, 14, 16)
        sb_vbox.setSpacing(6)

        lbl_brand = QLabel("📘 PDFMathTranslate")
        lbl_brand.setObjectName("SidebarTitle")
        lbl_ver = QLabel(f"Desktop UI · v{__version__}")
        lbl_ver.setObjectName("SidebarSubtitle")
        sb_vbox.addWidget(lbl_brand)
        sb_vbox.addWidget(lbl_ver)
        sb_vbox.addSpacing(12)

        self._nav_group = QButtonGroup(self)
        self._nav_group.setExclusive(True)

        self._nav_keys = [
            "nav_workspace",
            "nav_ai_keys",
            "nav_trans_settings",
            "nav_output_settings",
            "nav_system_settings",
            "nav_user_guide",
        ]
        self._nav_buttons: list[QPushButton] = []
        for idx, _ in enumerate(self._nav_keys):
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setProperty("navBtn", True)
            if idx == 0:
                btn.setChecked(True)
            self._nav_group.addButton(btn, idx)
            self._nav_buttons.append(btn)
            sb_vbox.addWidget(btn)

        sb_vbox.addStretch(1)

        # UI Language Switcher Card in Sidebar
        lang_card = QFrame()
        lang_card.setObjectName("SidebarStatusCard")
        lc_hbox = QHBoxLayout(lang_card)
        lc_hbox.setContentsMargins(10, 7, 10, 7)
        lc_hbox.setSpacing(6)
        self.lbl_ui_lang = QLabel()
        self.lbl_ui_lang.setStyleSheet("color: #CBD5E1; font-size: 12px; font-weight: 600;")
        self.combo_ui_lang = QComboBox()
        for code, name in UI_LANGUAGES.items():
            self.combo_ui_lang.addItem(name, code)
        curr_ui_lang = I18nManager.get_lang()
        idx_lang = self.combo_ui_lang.findData(curr_ui_lang)
        if idx_lang >= 0:
            self.combo_ui_lang.setCurrentIndex(idx_lang)
        self.combo_ui_lang.currentIndexChanged.connect(self._on_ui_language_changed)

        lc_hbox.addWidget(self.lbl_ui_lang)
        lc_hbox.addWidget(self.combo_ui_lang, 1)
        sb_vbox.addWidget(lang_card)

        # Bottom summary card in sidebar
        status_card = QFrame()
        status_card.setObjectName("SidebarStatusCard")
        sc_vbox = QVBoxLayout(status_card)
        sc_vbox.setContentsMargins(10, 10, 10, 10)
        sc_vbox.setSpacing(4)
        self.lbl_sb_service = QLabel("")
        self.lbl_sb_service.setStyleSheet("color: #E2E8F0; font-size: 11px; font-weight: 600;")
        self.lbl_sb_mode = QLabel("")
        self.lbl_sb_mode.setStyleSheet("color: #94A3B8; font-size: 11px;")
        self.lbl_sb_proxy = QLabel("")
        self.lbl_sb_proxy.setStyleSheet("color: #94A3B8; font-size: 11px;")
        sc_vbox.addWidget(self.lbl_sb_service)
        sc_vbox.addWidget(self.lbl_sb_mode)
        sc_vbox.addWidget(self.lbl_sb_proxy)
        sb_vbox.addWidget(status_card)

        main_hbox.addWidget(sidebar)

        # Stacked Content Area (6 pages)
        self.stack = QStackedWidget()
        self.page_workspace = WorkspacePage(self)
        self.page_ai_providers = AIProvidersPage(self)
        self.page_translation_settings = TranslationSettingsPage(self)
        self.page_output_settings = OutputSettingsPage(self)
        self.page_system_settings = SystemSettingsPage(self)
        self.page_user_guide = HelpGuidePage(self)

        self.stack.addWidget(self.page_workspace)
        self.stack.addWidget(self.page_ai_providers)
        self.stack.addWidget(self.page_translation_settings)
        self.stack.addWidget(self.page_output_settings)
        self.stack.addWidget(self.page_system_settings)
        self.stack.addWidget(self.page_user_guide)

        main_hbox.addWidget(self.stack, 1)

        # Connect navigation & signals
        self._nav_group.idClicked.connect(self.switch_page)
        self.page_workspace.request_open_ai_settings.connect(self.open_ai_provider_config)
        self.page_workspace.request_open_guide.connect(lambda: self.switch_page(5))
        self.page_user_guide.navigate_requested.connect(self.switch_page)

        self.page_ai_providers.settings_changed.connect(self._on_any_settings_changed)
        self.page_translation_settings.settings_changed.connect(self._on_any_settings_changed)
        self.page_output_settings.settings_changed.connect(self._on_any_settings_changed)
        self.page_system_settings.settings_changed.connect(self._on_any_settings_changed)

        # Status bar
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)

    def _setup_menubar(self) -> None:
        menubar = self.menuBar()
        self.file_menu = menubar.addMenu("")

        self.act_open = QAction("", self)
        self.act_open.setShortcut("Ctrl+O")
        self.act_open.triggered.connect(self.page_workspace.add_files_dialog)
        self.file_menu.addAction(self.act_open)

        self.act_folder = QAction("", self)
        self.act_folder.triggered.connect(self.page_workspace.add_folder_dialog)
        self.file_menu.addAction(self.act_folder)

        self.file_menu.addSeparator()
        self.act_settings = QAction("", self)
        self.act_settings.setShortcut("Ctrl+,")
        self.act_settings.triggered.connect(lambda: self.switch_page(1))
        self.file_menu.addAction(self.act_settings)

        self.help_menu = menubar.addMenu("")
        self.act_guide = QAction("", self)
        self.act_guide.setShortcut("F1")
        self.act_guide.triggered.connect(lambda: self.switch_page(5))
        self.help_menu.addAction(self.act_guide)

    def _on_ui_language_changed(self, idx: int) -> None:
        lang_code = self.combo_ui_lang.itemData(idx)
        if lang_code:
            I18nManager.set_lang(lang_code)
            self.retranslate_ui()

    def retranslate_ui(self) -> None:
        self.setWindowTitle(tr("window_title", version=__version__))
        for idx, key in enumerate(self._nav_keys):
            self._nav_buttons[idx].setText(tr(key))

        self.lbl_ui_lang.setText(tr("ui_lang_label"))
        self.file_menu.setTitle(tr("menu_file"))
        self.act_open.setText(tr("menu_add_files"))
        self.act_folder.setText(tr("menu_add_folder"))
        self.act_settings.setText(tr("menu_settings"))
        self.help_menu.setTitle(tr("menu_help"))
        self.act_guide.setText(tr("menu_open_guide"))

        self.page_workspace.retranslate_ui()
        self.page_ai_providers.retranslate_ui()
        self.page_translation_settings.retranslate_ui()
        self.page_output_settings.retranslate_ui()
        self.page_system_settings.retranslate_ui()
        self.page_user_guide.retranslate_ui()

        self._refresh_sidebar_summary()
        self.statusBar().showMessage(
            tr("status_config_path", path=AppSettings.config_file_path())
        )

    def switch_page(self, index: int) -> None:
        if 0 <= index < self.stack.count():
            self.stack.setCurrentIndex(index)
            self._nav_buttons[index].setChecked(True)
            if index == 4:
                self.page_system_settings.refresh_cache_stats()

    def open_ai_provider_config(self, service_key: str) -> None:
        self.switch_page(1)
        for i in range(self.page_ai_providers.provider_list.count()):
            item = self.page_ai_providers.provider_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == service_key:
                self.page_ai_providers.provider_list.setCurrentRow(i)
                break

    def _on_any_settings_changed(self) -> None:
        self.page_workspace.sync_from_settings()
        self._refresh_sidebar_summary()

    def _refresh_sidebar_summary(self) -> None:
        svc = AppSettings.get("PDF2ZH_DEFAULT_SERVICE", "Bing")
        mode = AppSettings.get("PDF2ZH_DEFAULT_MODE", "fast")
        threads = AppSettings.get("PDF2ZH_THREADS", 4)
        proxy_on = bool(AppSettings.get("PDF2ZH_PROXY_ENABLED", False))
        self.lbl_sb_service.setText(tr("sb_default_service", svc=svc))
        self.lbl_sb_mode.setText(tr("sb_default_mode", mode=mode, threads=threads))
        self.lbl_sb_proxy.setText(tr("sb_proxy_on") if proxy_on else tr("sb_proxy_off"))


def launch_desktop_ui(files: Optional[list[str]] = None) -> int:
    """Launch the native PySide6 desktop application."""
    app = QApplication.instance() or QApplication([])
    app.setApplicationName("PDFMathTranslate")
    app.setApplicationDisplayName("PDFMathTranslate")
    app.setOrganizationName("PDFMathTranslate")

    win = MainWindow(initial_files=files)
    win.show()
    return app.exec()
