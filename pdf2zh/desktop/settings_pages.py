"""Settings pages and User Guide page for PDFMathTranslate Desktop UI:
1. AI Providers & API Keys
2. Translation & Layout Settings
3. Output & Task Management Settings
4. System & Advanced Settings
5. User Guide & Help Page
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QSplitter,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from pdf2zh.config import ConfigManager
from pdf2zh.desktop.i18n import (
    I18nManager,
    get_localized_category,
    get_localized_field_label,
    get_localized_lang_label,
    get_localized_provider_desc,
    get_user_guide_html,
    tr,
)
from pdf2zh.desktop.metadata import (
    CODE_TO_LANG_LABEL,
    DEFAULT_PROMPT_TEMPLATE,
    ENV_FIELD_INFO,
    LANG_MAP,
    PROVIDER_METADATA,
    SERVICE_MAP,
    AppSettings,
    get_provider_envs,
    is_provider_configured,
    is_secret_field,
    save_provider_envs,
)
from pdf2zh.desktop.pdf_viewer import reveal_in_file_manager
from pdf2zh.desktop.workers import ConnectionTestWorker


def _create_card(title: str = "", subtitle: str = "") -> tuple[QFrame, QVBoxLayout, QLabel, QLabel]:
    card = QFrame()
    card.setObjectName("CardFrame")
    vbox = QVBoxLayout(card)
    vbox.setContentsMargins(20, 18, 20, 18)
    vbox.setSpacing(12)

    lbl_title = QLabel(title)
    lbl_title.setObjectName("CardTitle")
    vbox.addWidget(lbl_title)

    lbl_sub = QLabel(subtitle)
    lbl_sub.setObjectName("CardSubtitle")
    lbl_sub.setWordWrap(True)
    vbox.addWidget(lbl_sub)

    return card, vbox, lbl_title, lbl_sub


class AIProvidersPage(QWidget):
    """Master-detail page for configuring all AI / translation providers and API keys."""

    settings_changed = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._current_service: str = ""
        self._field_widgets: dict[str, QWidget] = {}
        self._test_worker: Optional[ConnectionTestWorker] = None
        self._setup_ui()
        self.retranslate_ui()
        self._populate_provider_list()

    def _setup_ui(self) -> None:
        root = QHBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # Left column: Search + Provider List
        left_panel = QFrame()
        left_panel.setObjectName("CardFrame")
        left_panel.setMinimumWidth(275)
        left_panel.setMaximumWidth(340)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(12, 14, 12, 14)
        left_layout.setSpacing(10)

        self.lbl_list_title = QLabel()
        self.lbl_list_title.setObjectName("CardTitle")
        left_layout.addWidget(self.lbl_list_title)

        self.search_input = QLineEdit()
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self._filter_provider_list)
        left_layout.addWidget(self.search_input)

        self.provider_list = QListWidget()
        self.provider_list.setObjectName("ProviderList")
        self.provider_list.currentItemChanged.connect(self._on_provider_selected)
        left_layout.addWidget(self.provider_list, 1)

        splitter.addWidget(left_panel)

        # Right column: Provider Configuration Form
        right_panel = QFrame()
        right_panel.setObjectName("CardFrame")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(24, 20, 24, 20)
        right_layout.setSpacing(14)

        # Header area
        header_row = QHBoxLayout()
        self.lbl_provider_name = QLabel()
        self.lbl_provider_name.setStyleSheet("font-size: 20px; font-weight: 700; color: #0F172A;")
        self.lbl_category_badge = QLabel("")
        self.lbl_category_badge.setObjectName("BadgeLabel")

        header_row.addWidget(self.lbl_provider_name)
        header_row.addWidget(self.lbl_category_badge)
        header_row.addStretch(1)

        self.btn_open_doc = QPushButton()
        self.btn_open_doc.setVisible(False)
        self.btn_open_doc.clicked.connect(self._open_provider_url)
        header_row.addWidget(self.btn_open_doc)

        right_layout.addLayout(header_row)

        self.lbl_provider_desc = QLabel("")
        self.lbl_provider_desc.setObjectName("CardSubtitle")
        self.lbl_provider_desc.setWordWrap(True)
        right_layout.addWidget(self.lbl_provider_desc)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #E2E8F0;")
        right_layout.addWidget(line)

        # Dynamic fields container inside scroll area
        self.form_scroll = QScrollArea()
        self.form_scroll.setWidgetResizable(True)
        self.form_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.form_container = QWidget()
        self.form_layout = QFormLayout(self.form_container)
        self.form_layout.setContentsMargins(4, 8, 8, 8)
        self.form_layout.setSpacing(14)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.form_scroll.setWidget(self.form_container)

        right_layout.addWidget(self.form_scroll, 1)

        # Test result banner
        self.lbl_test_result = QLabel("")
        self.lbl_test_result.setWordWrap(True)
        self.lbl_test_result.setVisible(False)
        self.lbl_test_result.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        right_layout.addWidget(self.lbl_test_result)

        # Bottom action buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.btn_save = QPushButton()
        self.btn_save.setObjectName("PrimaryButton")
        self.btn_save.clicked.connect(self.save_current_provider)

        self.btn_test = QPushButton()
        self.btn_test.clicked.connect(self.test_current_provider)

        self.btn_set_default = QPushButton()
        self.btn_set_default.clicked.connect(self.set_as_default_provider)

        self.btn_reset_provider = QPushButton()
        self.btn_reset_provider.clicked.connect(self.reset_current_provider)

        btn_row.addWidget(self.btn_save)
        btn_row.addWidget(self.btn_test)
        btn_row.addWidget(self.btn_set_default)
        btn_row.addStretch(1)
        btn_row.addWidget(self.btn_reset_provider)

        right_layout.addLayout(btn_row)

        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        root.addWidget(splitter)

    def retranslate_ui(self) -> None:
        self.lbl_list_title.setText(tr("ai_list_title"))
        self.search_input.setPlaceholderText(tr("ai_search_ph"))
        self.btn_open_doc.setText(tr("ai_btn_doc"))
        self.btn_save.setText(tr("ai_btn_save"))
        self.btn_test.setText(tr("ai_btn_test"))
        self.btn_set_default.setText(tr("ai_btn_set_default"))
        self.btn_reset_provider.setText(tr("ai_btn_reset"))
        self._populate_provider_list()
        if self._current_service:
            self._load_provider_form(self._current_service)

    def _populate_provider_list(self) -> None:
        current_key = self._current_service or AppSettings.get("PDF2ZH_DEFAULT_SERVICE", "Bing")
        default_svc = AppSettings.get("PDF2ZH_DEFAULT_SERVICE", "Bing")

        self.provider_list.blockSignals(True)
        self.provider_list.clear()

        selected_row = 0
        for idx, service_key in enumerate(SERVICE_MAP.keys()):
            ready, status_text = is_provider_configured(service_key)
            meta = PROVIDER_METADATA.get(service_key, {})
            cat = get_localized_category(meta.get("category", ""))
            prefix = "⭐ " if service_key == default_svc else ""
            badge = "🟢" if ready else "⚪"
            display = f"{badge} {prefix}{service_key}\n     [{cat}] · {status_text}"

            item = QListWidgetItem(display)
            item.setData(Qt.ItemDataRole.UserRole, service_key)
            self.provider_list.addItem(item)
            if service_key == current_key:
                selected_row = idx

        self.provider_list.blockSignals(False)
        if self.provider_list.count() > 0:
            self.provider_list.setCurrentRow(selected_row)

    def _filter_provider_list(self, query: str) -> None:
        q = query.strip().lower()
        for i in range(self.provider_list.count()):
            item = self.provider_list.item(i)
            key = item.data(Qt.ItemDataRole.UserRole)
            meta = PROVIDER_METADATA.get(key, {})
            cat_loc = get_localized_category(meta.get("category", "")).lower()
            desc_loc = get_localized_provider_desc(key, meta.get("desc", "")).lower()
            match = (
                not q
                or q in key.lower()
                or q in meta.get("desc", "").lower()
                or q in desc_loc
                or q in meta.get("category", "").lower()
                or q in cat_loc
            )
            item.setHidden(not match)

    def _on_provider_selected(
        self, current: Optional[QListWidgetItem], previous: Optional[QListWidgetItem]
    ) -> None:
        if current is None:
            return
        service_key = current.data(Qt.ItemDataRole.UserRole)
        self._load_provider_form(service_key)

    def _load_provider_form(self, service_key: str) -> None:
        self._current_service = service_key
        translator_cls = SERVICE_MAP[service_key]
        meta = PROVIDER_METADATA.get(service_key, {})

        default_svc = AppSettings.get("PDF2ZH_DEFAULT_SERVICE", "Bing")
        is_def_str = tr("ai_current_default") if service_key == default_svc else ""
        self.lbl_provider_name.setText(f"{service_key}{is_def_str}")
        self.lbl_category_badge.setText(get_localized_category(meta.get("category", "")))
        self.lbl_provider_desc.setText(
            get_localized_provider_desc(
                service_key, meta.get("desc", f"-s {translator_cls.name}")
            )
        )

        doc_url = meta.get("url", "")
        self.btn_open_doc.setVisible(bool(doc_url))
        self.btn_open_doc.setProperty("docUrl", doc_url)

        self.lbl_test_result.setVisible(False)

        while self.form_layout.rowCount() > 0:
            self.form_layout.removeRow(0)
        self._field_widgets.clear()

        envs = get_provider_envs(service_key)

        if not translator_cls.envs:
            info_lbl = QLabel(tr("ai_no_key_needed"))
            info_lbl.setStyleSheet(
                "color: #15803D; background: #F0FDF4; border: 1px solid #BBF7D0; "
                "border-radius: 8px; padding: 14px; font-size: 13px;"
            )
            info_lbl.setWordWrap(True)
            self.form_layout.addRow(info_lbl)
            return

        suggested_models: list[str] = meta.get("models", [])

        for env_key, default_val in translator_cls.envs.items():
            finfo = ENV_FIELD_INFO.get(env_key, {})
            label_text = get_localized_field_label(
                env_key, finfo.get("label", env_key)
            )
            placeholder = finfo.get(
                "placeholder",
                str(default_val) if default_val is not None else env_key,
            )
            current_val = envs.get(env_key, "")

            lbl = QLabel(f"{label_text}:")
            lbl.setToolTip(f"ENV: {env_key}")

            if finfo.get("is_model") == "true" or env_key.upper().endswith("MODEL"):
                combo = QComboBox()
                combo.setEditable(True)
                models = list(suggested_models)
                if current_val and current_val not in models:
                    models.insert(0, current_val)
                elif default_val and str(default_val) not in models:
                    models.append(str(default_val))
                combo.addItems(models)
                combo.setCurrentText(current_val or (str(default_val) if default_val else ""))
                if combo.lineEdit():
                    combo.lineEdit().setPlaceholderText(placeholder)
                self._field_widgets[env_key] = combo
                self.form_layout.addRow(lbl, combo)

            elif is_secret_field(env_key):
                row_w = QWidget()
                row_h = QHBoxLayout(row_w)
                row_h.setContentsMargins(0, 0, 0, 0)
                row_h.setSpacing(6)

                edit = QLineEdit(current_val)
                edit.setPlaceholderText(placeholder)
                edit.setEchoMode(QLineEdit.EchoMode.Password)

                btn_toggle = QPushButton(tr("btn_show"))
                btn_toggle.setCheckable(True)
                btn_toggle.setFixedWidth(60)

                def _make_toggle(line_edit: QLineEdit, btn: QPushButton):
                    def _toggle(checked: bool):
                        line_edit.setEchoMode(
                            QLineEdit.EchoMode.Normal
                            if checked
                            else QLineEdit.EchoMode.Password
                        )
                        btn.setText(tr("btn_hide") if checked else tr("btn_show"))

                    return _toggle

                btn_toggle.toggled.connect(_make_toggle(edit, btn_toggle))
                row_h.addWidget(edit, 1)
                row_h.addWidget(btn_toggle)

                self._field_widgets[env_key] = edit
                self.form_layout.addRow(lbl, row_w)

            else:
                edit = QLineEdit(current_val)
                edit.setPlaceholderText(placeholder)
                self._field_widgets[env_key] = edit
                self.form_layout.addRow(lbl, edit)

        cli_hint = QLabel(tr("ai_cli_hint", name=translator_cls.name))
        cli_hint.setObjectName("CardSubtitle")
        cli_hint.setWordWrap(True)
        self.form_layout.addRow("", cli_hint)

    def _collect_current_envs(self) -> dict[str, str]:
        result: dict[str, str] = {}
        for k, widget in self._field_widgets.items():
            if isinstance(widget, QComboBox):
                result[k] = widget.currentText().strip()
            elif isinstance(widget, QLineEdit):
                result[k] = widget.text().strip()
        return result

    def save_current_provider(self) -> None:
        if not self._current_service:
            return
        envs = self._collect_current_envs()
        save_provider_envs(self._current_service, envs)
        self._populate_provider_list()
        self._show_banner(True, tr("ai_msg_saved", svc=self._current_service))
        self.settings_changed.emit()

    def set_as_default_provider(self) -> None:
        if not self._current_service:
            return
        envs = self._collect_current_envs()
        save_provider_envs(self._current_service, envs)
        AppSettings.set("PDF2ZH_DEFAULT_SERVICE", self._current_service)
        self._populate_provider_list()
        self._show_banner(True, tr("ai_msg_default_set", svc=self._current_service))
        self.settings_changed.emit()

    def reset_current_provider(self) -> None:
        if not self._current_service:
            return
        translator_cls = SERVICE_MAP[self._current_service]
        defaults = {
            k: ("" if v is None else str(v)) for k, v in translator_cls.envs.items()
        }
        save_provider_envs(self._current_service, defaults)
        self._load_provider_form(self._current_service)
        self._populate_provider_list()
        self._show_banner(True, tr("ai_msg_reset", svc=self._current_service))
        self.settings_changed.emit()

    def test_current_provider(self) -> None:
        if not self._current_service:
            return
        envs = self._collect_current_envs()
        save_provider_envs(self._current_service, envs)

        self.btn_test.setEnabled(False)
        self.btn_test.setText(tr("ai_btn_testing"))
        self._show_banner(True, tr("ai_msg_testing", svc=self._current_service))

        self._test_worker = ConnectionTestWorker(self._current_service, envs, self)
        self._test_worker.result_ready.connect(self._on_test_finished)
        self._test_worker.start()

    def _on_test_finished(self, ok: bool, message: str) -> None:
        self.btn_test.setEnabled(True)
        self.btn_test.setText(tr("ai_btn_test"))
        self._populate_provider_list()
        self._show_banner(ok, ("✅ " if ok else "❌ ") + message)

    def _show_banner(self, ok: bool, text: str) -> None:
        self.lbl_test_result.setVisible(True)
        self.lbl_test_result.setText(text)
        if ok:
            self.lbl_test_result.setStyleSheet(
                "color: #166534; background: #F0FDF4; border: 1px solid #BBF7D0; "
                "border-radius: 8px; padding: 10px 12px; font-size: 13px;"
            )
        else:
            self.lbl_test_result.setStyleSheet(
                "color: #991B1B; background: #FEF2F2; border: 1px solid #FECACA; "
                "border-radius: 8px; padding: 10px 12px; font-size: 13px;"
            )

    def _open_provider_url(self) -> None:
        url = self.btn_open_doc.property("docUrl")
        if url:
            QDesktopServices.openUrl(QUrl(str(url)))


class TranslationSettingsPage(QWidget):
    """Settings page for translation languages, engine mode, formula regex, custom prompt, and OCR."""

    settings_changed = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
        self.retranslate_ui()
        self.load_from_config()

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(16)

        # Card 1: Default Languages & Engine Mode
        card_lang, vbox_lang, self.c1_title, self.c1_sub = _create_card()
        form_lang = QFormLayout()
        form_lang.setSpacing(12)

        self.combo_lang_from = QComboBox()
        self.combo_lang_to = QComboBox()
        for label_zh, code in LANG_MAP.items():
            self.combo_lang_from.addItem(label_zh, code)
            self.combo_lang_to.addItem(label_zh, code)

        self.combo_mode = QComboBox()
        self.combo_mode.addItem("", "fast")
        self.combo_mode.addItem("", "ultrafast")
        self.combo_mode.addItem("", "babeldoc")
        self.combo_mode.addItem("", "precise")

        self.lbl_source = QLabel()
        self.lbl_target = QLabel()
        self.lbl_mode = QLabel()
        form_lang.addRow(self.lbl_source, self.combo_lang_from)
        form_lang.addRow(self.lbl_target, self.combo_lang_to)
        form_lang.addRow(self.lbl_mode, self.combo_mode)
        vbox_lang.addLayout(form_lang)
        layout.addWidget(card_lang)

        # Card 2: Formula & Font Preservation
        card_formula, vbox_formula, self.c2_title, self.c2_sub = _create_card()
        form_formula = QFormLayout()
        form_formula.setSpacing(12)

        vfont_row = QHBoxLayout()
        self.edit_vfont = QLineEdit()
        self.btn_preset_vfont = QPushButton()
        self.btn_preset_vfont.clicked.connect(
            lambda: self.edit_vfont.setText(
                r"(CM[^R]|MS.M|XY|MT|BL|RM|EU|LA|RS|LINE|LCIRCLE|TeX-|rsfs|txsy|wasy|stmary|.*Mono|.*Code|.*Ital|.*Sym|.*Math).*"
            )
        )
        vfont_row.addWidget(self.edit_vfont, 1)
        vfont_row.addWidget(self.btn_preset_vfont)

        self.edit_vchar = QLineEdit()
        self.chk_skip_subset = QCheckBox()
        self.chk_compatible = QCheckBox()

        self.lbl_vfont = QLabel()
        self.lbl_vchar = QLabel()
        form_formula.addRow(self.lbl_vfont, vfont_row)
        form_formula.addRow(self.lbl_vchar, self.edit_vchar)
        form_formula.addRow("", self.chk_skip_subset)
        form_formula.addRow("", self.chk_compatible)
        vbox_formula.addLayout(form_formula)
        layout.addWidget(card_formula)

        # Card 3: Custom LLM Prompt Template
        card_prompt, vbox_prompt, self.c3_title, self.c3_sub = _create_card()
        self.chk_use_prompt = QCheckBox()
        vbox_prompt.addWidget(self.chk_use_prompt)

        self.edit_prompt = QPlainTextEdit()
        self.edit_prompt.setMinimumHeight(130)
        self.edit_prompt.setPlaceholderText(DEFAULT_PROMPT_TEMPLATE)
        vbox_prompt.addWidget(self.edit_prompt)

        prompt_btn_row = QHBoxLayout()
        self.btn_fill_default_prompt = QPushButton()
        self.btn_fill_default_prompt.clicked.connect(
            lambda: self.edit_prompt.setPlainText(DEFAULT_PROMPT_TEMPLATE)
        )
        self.btn_load_prompt_file = QPushButton()
        self.btn_load_prompt_file.clicked.connect(self._import_prompt_file)
        prompt_btn_row.addWidget(self.btn_fill_default_prompt)
        prompt_btn_row.addWidget(self.btn_load_prompt_file)
        prompt_btn_row.addStretch(1)
        vbox_prompt.addLayout(prompt_btn_row)
        layout.addWidget(card_prompt)

        # Card 4: OCR Settings
        card_ocr, vbox_ocr, self.c4_title, self.c4_sub = _create_card()
        form_ocr = QFormLayout()
        form_ocr.setSpacing(12)

        self.edit_ocr_lang = QLineEdit()

        tess_row = QHBoxLayout()
        self.edit_tessdata = QLineEdit()
        self.btn_browse_tess = QPushButton()
        self.btn_browse_tess.clicked.connect(self._browse_tessdata)
        tess_row.addWidget(self.edit_tessdata, 1)
        tess_row.addWidget(self.btn_browse_tess)

        self.lbl_ocr_lang = QLabel()
        self.lbl_tess_dir = QLabel()
        form_ocr.addRow(self.lbl_ocr_lang, self.edit_ocr_lang)
        form_ocr.addRow(self.lbl_tess_dir, tess_row)
        vbox_ocr.addLayout(form_ocr)
        layout.addWidget(card_ocr)

        # Save bar
        save_row = QHBoxLayout()
        self.btn_save = QPushButton()
        self.btn_save.setObjectName("PrimaryButton")
        self.btn_save.clicked.connect(self.save_to_config)
        self.lbl_saved_hint = QLabel("")
        self.lbl_saved_hint.setStyleSheet("color: #15803D; font-weight: 600;")
        save_row.addWidget(self.btn_save)
        save_row.addWidget(self.lbl_saved_hint)
        save_row.addStretch(1)
        layout.addLayout(save_row)

        layout.addStretch(1)
        scroll.setWidget(container)
        outer.addWidget(scroll)

    def retranslate_ui(self) -> None:
        self.c1_title.setText(tr("ts_card1_title"))
        self.c1_sub.setText(tr("ts_card1_sub"))
        self.lbl_source.setText(tr("ts_lbl_source"))
        self.lbl_target.setText(tr("ts_lbl_target"))
        self.lbl_mode.setText(tr("ts_lbl_mode"))
        for i in range(self.combo_lang_from.count()):
            code = self.combo_lang_from.itemData(i)
            if code:
                self.combo_lang_from.setItemText(i, get_localized_lang_label(str(code)))
        for i in range(self.combo_lang_to.count()):
            code = self.combo_lang_to.itemData(i)
            if code:
                self.combo_lang_to.setItemText(i, get_localized_lang_label(str(code)))
        self.combo_mode.setItemText(0, tr("ts_mode_fast"))
        self.combo_mode.setItemText(1, tr("ts_mode_ultrafast"))
        self.combo_mode.setItemText(2, tr("ts_mode_babeldoc"))
        self.combo_mode.setItemText(3, tr("ts_mode_precise"))

        self.c2_title.setText(tr("ts_card2_title"))
        self.c2_sub.setText(tr("ts_card2_sub"))
        self.edit_vfont.setPlaceholderText(tr("ts_vfont_ph"))
        self.btn_preset_vfont.setText(tr("ts_btn_vfont_preset"))
        self.edit_vchar.setPlaceholderText(tr("ts_vchar_ph"))
        self.chk_skip_subset.setText(tr("ts_chk_skip_subset"))
        self.chk_compatible.setText(tr("ts_chk_compatible"))
        self.lbl_vfont.setText(tr("ts_lbl_vfont"))
        self.lbl_vchar.setText(tr("ts_lbl_vchar"))

        self.c3_title.setText(tr("ts_card3_title"))
        self.c3_sub.setText(tr("ts_card3_sub"))
        self.chk_use_prompt.setText(tr("ts_chk_use_prompt"))
        self.btn_fill_default_prompt.setText(tr("ts_btn_default_prompt"))
        self.btn_load_prompt_file.setText(tr("ts_btn_import_prompt"))

        self.c4_title.setText(tr("ts_card4_title"))
        self.c4_sub.setText(tr("ts_card4_sub"))
        self.edit_ocr_lang.setPlaceholderText(tr("ts_ocr_lang_ph"))
        self.edit_tessdata.setPlaceholderText(tr("ts_tess_ph"))
        self.btn_browse_tess.setText(tr("ts_btn_browse_dir"))
        self.lbl_ocr_lang.setText(tr("ts_lbl_ocr_lang"))
        self.lbl_tess_dir.setText(tr("ts_lbl_tess_dir"))
        self.btn_save.setText(tr("ts_btn_save"))
        self.lbl_saved_hint.setText("")

    def _import_prompt_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Prompt File", "", "Text Files (*.txt *.md *.prompt);;All Files (*)"
        )
        if path:
            try:
                content = Path(path).read_text(encoding="utf-8")
                self.edit_prompt.setPlainText(content)
                self.chk_use_prompt.setChecked(True)
            except Exception as exc:
                QMessageBox.warning(self, "Error", str(exc))

    def _browse_tessdata(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select TESSDATA Folder")
        if folder:
            self.edit_tessdata.setText(folder)

    def load_from_config(self) -> None:
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

        self.edit_vfont.setText(str(AppSettings.get("PDF2ZH_VFONT", "")))
        self.edit_vchar.setText(str(AppSettings.get("PDF2ZH_VCHAR", "")))
        self.chk_skip_subset.setChecked(bool(AppSettings.get("PDF2ZH_SKIP_SUBSET_FONTS", False)))
        self.chk_compatible.setChecked(bool(AppSettings.get("PDF2ZH_COMPATIBLE_PDFA", False)))

        self.chk_use_prompt.setChecked(bool(AppSettings.get("PDF2ZH_USE_CUSTOM_PROMPT", False)))
        saved_prompt = str(AppSettings.get("PDF2ZH_CUSTOM_PROMPT", ""))
        self.edit_prompt.setPlainText(saved_prompt if saved_prompt else DEFAULT_PROMPT_TEMPLATE)

        self.edit_ocr_lang.setText(str(AppSettings.get("PDF2ZH_OCR_LANGUAGE", "")))
        self.edit_tessdata.setText(str(AppSettings.get("PDF2ZH_TESSDATA_PREFIX", "")))

    def save_to_config(self) -> None:
        AppSettings.set(
            "PDF2ZH_LANG_FROM_CODE",
            self.combo_lang_from.currentData()
            or LANG_MAP.get(self.combo_lang_from.currentText(), "en"),
        )
        AppSettings.set(
            "PDF2ZH_LANG_TO_CODE",
            self.combo_lang_to.currentData()
            or LANG_MAP.get(self.combo_lang_to.currentText(), "zh"),
        )
        AppSettings.set("PDF2ZH_DEFAULT_MODE", self.combo_mode.currentData())
        AppSettings.set("PDF2ZH_VFONT", self.edit_vfont.text().strip())
        AppSettings.set("PDF2ZH_VCHAR", self.edit_vchar.text().strip())
        AppSettings.set("PDF2ZH_SKIP_SUBSET_FONTS", self.chk_skip_subset.isChecked())
        AppSettings.set("PDF2ZH_COMPATIBLE_PDFA", self.chk_compatible.isChecked())
        AppSettings.set("PDF2ZH_USE_CUSTOM_PROMPT", self.chk_use_prompt.isChecked())
        AppSettings.set("PDF2ZH_CUSTOM_PROMPT", self.edit_prompt.toPlainText().strip())
        AppSettings.set("PDF2ZH_OCR_LANGUAGE", self.edit_ocr_lang.text().strip())
        AppSettings.set("PDF2ZH_TESSDATA_PREFIX", self.edit_tessdata.text().strip())

        AppSettings.apply_runtime_settings()
        self.lbl_saved_hint.setText(tr("ts_msg_saved"))
        self.settings_changed.emit()


class OutputSettingsPage(QWidget):
    """Settings page for output directory, mono/dual file generation, concurrency, and post-actions."""

    settings_changed = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
        self.retranslate_ui()
        self.load_from_config()

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(16)

        # Card 1: Output Folder
        card_dir, vbox_dir, self.c1_title, self.c1_sub = _create_card()
        self.chk_save_next_to_source = QCheckBox()
        self.chk_save_next_to_source.toggled.connect(self._on_dir_mode_toggled)
        vbox_dir.addWidget(self.chk_save_next_to_source)

        dir_row = QHBoxLayout()
        self.lbl_fixed_dir = QLabel()
        self.edit_output_dir = QLineEdit()
        self.btn_browse_dir = QPushButton()
        self.btn_browse_dir.clicked.connect(self._browse_output_dir)
        self.btn_open_dir = QPushButton()
        self.btn_open_dir.clicked.connect(self._open_output_dir)
        dir_row.addWidget(self.lbl_fixed_dir)
        dir_row.addWidget(self.edit_output_dir, 1)
        dir_row.addWidget(self.btn_browse_dir)
        dir_row.addWidget(self.btn_open_dir)
        vbox_dir.addLayout(dir_row)
        layout.addWidget(card_dir)

        # Card 2: Output File Variants
        card_types, vbox_types, self.c2_title, self.c2_sub = _create_card()
        self.chk_gen_mono = QCheckBox()
        self.chk_gen_dual = QCheckBox()
        vbox_types.addWidget(self.chk_gen_mono)
        vbox_types.addWidget(self.chk_gen_dual)
        layout.addWidget(card_types)

        # Card 3: Concurrency & Post-translation Automation
        card_task, vbox_task, self.c3_title, self.c3_sub = _create_card()
        form_task = QFormLayout()
        form_task.setSpacing(12)

        self.spin_threads = QSpinBox()
        self.spin_threads.setRange(1, 64)
        self.spin_threads.setFixedWidth(180)

        self.chk_auto_preview = QCheckBox()
        self.chk_auto_open_dir = QCheckBox()

        self.lbl_threads = QLabel()
        form_task.addRow(self.lbl_threads, self.spin_threads)
        form_task.addRow("", self.chk_auto_preview)
        form_task.addRow("", self.chk_auto_open_dir)
        vbox_task.addLayout(form_task)
        layout.addWidget(card_task)

        save_row = QHBoxLayout()
        self.btn_save = QPushButton()
        self.btn_save.setObjectName("PrimaryButton")
        self.btn_save.clicked.connect(self.save_to_config)
        self.lbl_saved_hint = QLabel("")
        self.lbl_saved_hint.setStyleSheet("color: #15803D; font-weight: 600;")
        save_row.addWidget(self.btn_save)
        save_row.addWidget(self.lbl_saved_hint)
        save_row.addStretch(1)
        layout.addLayout(save_row)

        layout.addStretch(1)
        scroll.setWidget(container)
        outer.addWidget(scroll)

    def retranslate_ui(self) -> None:
        self.c1_title.setText(tr("os_card1_title"))
        self.c1_sub.setText(tr("os_card1_sub"))
        self.chk_save_next_to_source.setText(tr("os_chk_save_next"))
        self.lbl_fixed_dir.setText(tr("os_lbl_fixed_dir"))
        self.edit_output_dir.setPlaceholderText(tr("os_dir_ph"))
        self.btn_browse_dir.setText(tr("os_btn_browse"))
        self.btn_open_dir.setText(tr("os_btn_open_dir"))

        self.c2_title.setText(tr("os_card2_title"))
        self.c2_sub.setText(tr("os_card2_sub"))
        self.chk_gen_mono.setText(tr("os_chk_mono"))
        self.chk_gen_dual.setText(tr("os_chk_dual"))

        self.c3_title.setText(tr("os_card3_title"))
        self.c3_sub.setText(tr("os_card3_sub"))
        self.lbl_threads.setText(tr("os_lbl_threads"))
        self.chk_auto_preview.setText(tr("os_chk_auto_preview"))
        self.chk_auto_open_dir.setText(tr("os_chk_auto_open_dir"))

        self.btn_save.setText(tr("os_btn_save"))
        self.lbl_saved_hint.setText("")

    def _on_dir_mode_toggled(self, checked: bool) -> None:
        self.edit_output_dir.setEnabled(not checked)
        self.btn_browse_dir.setEnabled(not checked)

    def _browse_output_dir(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.edit_output_dir.setText(folder)
            self.chk_save_next_to_source.setChecked(False)

    def _open_output_dir(self) -> None:
        d = self.edit_output_dir.text().strip()
        if d and os.path.exists(d):
            reveal_in_file_manager(d)
        else:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(Path.home())))

    def load_from_config(self) -> None:
        save_next = bool(AppSettings.get("PDF2ZH_SAVE_NEXT_TO_SOURCE", True))
        self.chk_save_next_to_source.setChecked(save_next)
        self.edit_output_dir.setText(str(AppSettings.get("PDF2ZH_OUTPUT_DIR", "")))
        self._on_dir_mode_toggled(save_next)

        self.chk_gen_mono.setChecked(bool(AppSettings.get("PDF2ZH_GEN_MONO", True)))
        self.chk_gen_dual.setChecked(bool(AppSettings.get("PDF2ZH_GEN_DUAL", True)))
        self.spin_threads.setValue(int(AppSettings.get("PDF2ZH_THREADS", 4)))
        self.chk_auto_preview.setChecked(bool(AppSettings.get("PDF2ZH_AUTO_PREVIEW", True)))
        self.chk_auto_open_dir.setChecked(bool(AppSettings.get("PDF2ZH_AUTO_OPEN_DIR", False)))

    def save_to_config(self) -> None:
        if not self.chk_gen_mono.isChecked() and not self.chk_gen_dual.isChecked():
            self.chk_gen_dual.setChecked(True)

        AppSettings.set("PDF2ZH_SAVE_NEXT_TO_SOURCE", self.chk_save_next_to_source.isChecked())
        AppSettings.set("PDF2ZH_OUTPUT_DIR", self.edit_output_dir.text().strip())
        AppSettings.set("PDF2ZH_GEN_MONO", self.chk_gen_mono.isChecked())
        AppSettings.set("PDF2ZH_GEN_DUAL", self.chk_gen_dual.isChecked())
        AppSettings.set("PDF2ZH_THREADS", self.spin_threads.value())
        AppSettings.set("PDF2ZH_AUTO_PREVIEW", self.chk_auto_preview.isChecked())
        AppSettings.set("PDF2ZH_AUTO_OPEN_DIR", self.chk_auto_open_dir.isChecked())

        self.lbl_saved_hint.setText(tr("os_msg_saved"))
        self.settings_changed.emit()


class SystemSettingsPage(QWidget):
    """Settings page for network proxy, translation cache, ONNX runtime backend, and config import/export."""

    settings_changed = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
        self.retranslate_ui()
        self.load_from_config()

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(16)

        # Card 1: Network Proxy
        card_proxy, vbox_proxy, self.c1_title, self.c1_sub = _create_card()
        self.chk_proxy_enabled = QCheckBox()
        vbox_proxy.addWidget(self.chk_proxy_enabled)

        proxy_row = QHBoxLayout()
        self.lbl_proxy_url = QLabel()
        self.edit_proxy_url = QLineEdit()
        proxy_row.addWidget(self.lbl_proxy_url)
        proxy_row.addWidget(self.edit_proxy_url, 1)
        vbox_proxy.addLayout(proxy_row)
        layout.addWidget(card_proxy)

        # Card 2: Translation Cache Management
        card_cache, vbox_cache, self.c2_title, self.c2_sub = _create_card()
        self.chk_ignore_cache = QCheckBox()
        vbox_cache.addWidget(self.chk_ignore_cache)

        self.lbl_cache_stats = QLabel()
        self.lbl_cache_stats.setObjectName("CardSubtitle")
        vbox_cache.addWidget(self.lbl_cache_stats)

        cache_btn_row = QHBoxLayout()
        self.btn_refresh_cache = QPushButton()
        self.btn_refresh_cache.clicked.connect(self.refresh_cache_stats)
        self.btn_clear_cache = QPushButton()
        self.btn_clear_cache.clicked.connect(self.clear_translation_cache)
        self.btn_reveal_cache = QPushButton()
        self.btn_reveal_cache.clicked.connect(
            lambda: reveal_in_file_manager(str(AppSettings.cache_db_path()))
        )
        cache_btn_row.addWidget(self.btn_refresh_cache)
        cache_btn_row.addWidget(self.btn_clear_cache)
        cache_btn_row.addWidget(self.btn_reveal_cache)
        cache_btn_row.addStretch(1)
        vbox_cache.addLayout(cache_btn_row)
        layout.addWidget(card_cache)

        # Card 3: ONNX Runtime & Layout Model
        card_onnx, vbox_onnx, self.c3_title, self.c3_sub = _create_card()
        form_onnx = QFormLayout()
        form_onnx.setSpacing(12)

        self.combo_onnx_backend = QComboBox()
        self.combo_onnx_backend.addItem("auto (Recommended)", "auto")
        self.combo_onnx_backend.addItem("cpu (CPUExecutionProvider)", "cpu")
        self.combo_onnx_backend.addItem("cuda (NVIDIA CUDA)", "cuda")
        self.combo_onnx_backend.addItem("dml (DirectML)", "dml")

        onnx_path_row = QHBoxLayout()
        self.edit_onnx_path = QLineEdit()
        self.btn_browse_onnx = QPushButton()
        self.btn_browse_onnx.clicked.connect(self._browse_onnx_model)
        onnx_path_row.addWidget(self.edit_onnx_path, 1)
        onnx_path_row.addWidget(self.btn_browse_onnx)

        self.lbl_onnx_backend = QLabel()
        self.lbl_onnx_path = QLabel()
        form_onnx.addRow(self.lbl_onnx_backend, self.combo_onnx_backend)
        form_onnx.addRow(self.lbl_onnx_path, onnx_path_row)
        vbox_onnx.addLayout(form_onnx)
        layout.addWidget(card_onnx)

        # Card 4: Config File Management (Import / Export / Reset)
        card_cfg, vbox_cfg, self.c4_title, self.c4_sub = _create_card()
        cfg_btn_row = QHBoxLayout()
        self.btn_open_cfg = QPushButton()
        self.btn_open_cfg.clicked.connect(
            lambda: reveal_in_file_manager(str(AppSettings.config_file_path()))
        )
        self.btn_export_cfg = QPushButton()
        self.btn_export_cfg.clicked.connect(self.export_config_file)
        self.btn_import_cfg = QPushButton()
        self.btn_import_cfg.clicked.connect(self.import_config_file)
        self.btn_reset_all = QPushButton()
        self.btn_reset_all.clicked.connect(self.reset_all_settings)

        cfg_btn_row.addWidget(self.btn_open_cfg)
        cfg_btn_row.addWidget(self.btn_export_cfg)
        cfg_btn_row.addWidget(self.btn_import_cfg)
        cfg_btn_row.addWidget(self.btn_reset_all)
        cfg_btn_row.addStretch(1)
        vbox_cfg.addLayout(cfg_btn_row)
        layout.addWidget(card_cfg)

        # Save button
        save_row = QHBoxLayout()
        self.btn_save = QPushButton()
        self.btn_save.setObjectName("PrimaryButton")
        self.btn_save.clicked.connect(self.save_to_config)
        self.lbl_saved_hint = QLabel("")
        self.lbl_saved_hint.setStyleSheet("color: #15803D; font-weight: 600;")
        save_row.addWidget(self.btn_save)
        save_row.addWidget(self.lbl_saved_hint)
        save_row.addStretch(1)
        layout.addLayout(save_row)

        layout.addStretch(1)
        scroll.setWidget(container)
        outer.addWidget(scroll)

    def retranslate_ui(self) -> None:
        self.c1_title.setText(tr("ss_card1_title"))
        self.c1_sub.setText(tr("ss_card1_sub"))
        self.chk_proxy_enabled.setText(tr("ss_chk_proxy"))
        self.lbl_proxy_url.setText(tr("ss_lbl_proxy_url"))
        self.edit_proxy_url.setPlaceholderText(tr("ss_proxy_ph"))

        self.c2_title.setText(tr("ss_card2_title"))
        self.c2_sub.setText(tr("ss_card2_sub"))
        self.chk_ignore_cache.setText(tr("ss_chk_ignore_cache"))
        self.btn_refresh_cache.setText(tr("ss_btn_refresh_cache"))
        self.btn_clear_cache.setText(tr("ss_btn_clear_cache"))
        self.btn_reveal_cache.setText(tr("ss_btn_reveal_cache"))

        self.c3_title.setText(tr("ss_card3_title"))
        self.c3_sub.setText(tr("ss_card3_sub"))
        self.lbl_onnx_backend.setText(tr("ss_lbl_onnx_backend"))
        self.lbl_onnx_path.setText(tr("ss_lbl_onnx_path"))
        self.edit_onnx_path.setPlaceholderText(tr("ss_onnx_ph"))
        self.btn_browse_onnx.setText(tr("ss_btn_browse_onnx"))

        self.c4_title.setText(tr("ss_card4_title"))
        self.c4_sub.setText(tr("status_config_path", path=AppSettings.config_file_path()))
        self.btn_open_cfg.setText(tr("ss_btn_open_cfg"))
        self.btn_export_cfg.setText(tr("ss_btn_export_cfg"))
        self.btn_import_cfg.setText(tr("ss_btn_import_cfg"))
        self.btn_reset_all.setText(tr("ss_btn_reset_all"))
        self.btn_save.setText(tr("ss_btn_save"))
        self.lbl_saved_hint.setText("")
        self.refresh_cache_stats()

    def _browse_onnx_model(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Select ONNX Model", "", "ONNX Model (*.onnx);;All Files (*)"
        )
        if path:
            self.edit_onnx_path.setText(path)

    def refresh_cache_stats(self) -> None:
        db_path = AppSettings.cache_db_path()
        if not db_path.exists():
            self.lbl_cache_stats.setText(f"{db_path} (0 MB)")
            return
        size_mb = db_path.stat().st_size / (1024 * 1024)
        count_str = "-"
        try:
            from pdf2zh.cache import _TranslationCache

            count_str = f"{_TranslationCache.select().count()} records"
        except Exception:
            pass
        self.lbl_cache_stats.setText(
            f"SQLite: {db_path}  |  {size_mb:.2f} MB  |  {count_str}"
        )

    def clear_translation_cache(self) -> None:
        ans = QMessageBox.question(
            self,
            tr("ss_btn_clear_cache"),
            "Clear all cached translation segments in SQLite?",
        )
        if ans != QMessageBox.StandardButton.Yes:
            return
        try:
            from pdf2zh.cache import _TranslationCache, init_db

            _TranslationCache.delete().execute()
            init_db()
            self.refresh_cache_stats()
            QMessageBox.information(self, "OK", "Translation cache cleared.")
        except Exception as exc:
            QMessageBox.warning(self, "Error", str(exc))

    def export_config_file(self) -> None:
        src = AppSettings.config_file_path()
        dest, _ = QFileDialog.getSaveFileName(
            self,
            "Export Config JSON",
            str(Path.home() / "pdf2zh_config_backup.json"),
            "JSON Files (*.json)",
        )
        if dest:
            try:
                shutil.copyfile(src, dest)
                QMessageBox.information(self, "OK", f"Saved to:\n{dest}")
            except Exception as exc:
                QMessageBox.warning(self, "Error", str(exc))

    def import_config_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Import Config JSON", "", "JSON Files (*.json)"
        )
        if not path:
            return
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("Root must be a JSON object")
            ConfigManager.custome_config(path)
            std_path = AppSettings.config_file_path()
            std_path.parent.mkdir(parents=True, exist_ok=True)
            std_path.write_text(
                json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8"
            )
            ConfigManager.custome_config(str(std_path))
            self.load_from_config()
            self.settings_changed.emit()
            QMessageBox.information(self, "OK", "Configuration imported successfully!")
        except Exception as exc:
            QMessageBox.warning(self, "Error", str(exc))

    def reset_all_settings(self) -> None:
        ans = QMessageBox.warning(
            self,
            tr("ss_btn_reset_all"),
            "Reset all saved settings and API keys to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if ans == QMessageBox.StandardButton.Yes:
            ConfigManager.clear()
            self.load_from_config()
            self.settings_changed.emit()

    def load_from_config(self) -> None:
        self.chk_proxy_enabled.setChecked(bool(AppSettings.get("PDF2ZH_PROXY_ENABLED", False)))
        self.edit_proxy_url.setText(
            str(AppSettings.get("PDF2ZH_HTTP_PROXY", "http://127.0.0.1:7890"))
        )
        self.chk_ignore_cache.setChecked(bool(AppSettings.get("PDF2ZH_IGNORE_CACHE", False)))

        backend = str(AppSettings.get("PDF2ZH_ONNX_BACKEND", "auto"))
        idx = self.combo_onnx_backend.findData(backend)
        if idx >= 0:
            self.combo_onnx_backend.setCurrentIndex(idx)

        self.edit_onnx_path.setText(str(AppSettings.get("PDF2ZH_ONNX_MODEL_PATH", "")))
        self.refresh_cache_stats()

    def save_to_config(self) -> None:
        AppSettings.set("PDF2ZH_PROXY_ENABLED", self.chk_proxy_enabled.isChecked())
        AppSettings.set("PDF2ZH_HTTP_PROXY", self.edit_proxy_url.text().strip())
        AppSettings.set("PDF2ZH_IGNORE_CACHE", self.chk_ignore_cache.isChecked())
        AppSettings.set("PDF2ZH_ONNX_BACKEND", self.combo_onnx_backend.currentData())
        AppSettings.set("PDF2ZH_ONNX_MODEL_PATH", self.edit_onnx_path.text().strip())

        AppSettings.apply_runtime_settings()
        self.lbl_saved_hint.setText(tr("ss_msg_saved"))
        self.settings_changed.emit()


class HelpGuidePage(QWidget):
    """Comprehensive interactive User Guide & FAQ page supporting multiple languages."""

    navigate_requested = Signal(int)  # page index in main stack

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
        self.retranslate_ui()

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 20, 24, 20)
        outer.setSpacing(14)

        header_card = QFrame()
        header_card.setObjectName("CardFrame")
        h_layout = QHBoxLayout(header_card)
        h_layout.setContentsMargins(20, 16, 20, 16)

        title_col = QVBoxLayout()
        self.lbl_title = QLabel()
        self.lbl_title.setStyleSheet("font-size: 19px; font-weight: 700; color: #0F172A;")
        self.lbl_subtitle = QLabel()
        self.lbl_subtitle.setObjectName("CardSubtitle")
        title_col.addWidget(self.lbl_title)
        title_col.addWidget(self.lbl_subtitle)
        h_layout.addLayout(title_col, 1)

        self.btn_go_workspace = QPushButton()
        self.btn_go_workspace.setObjectName("PrimaryButton")
        self.btn_go_workspace.clicked.connect(lambda: self.navigate_requested.emit(0))

        self.btn_go_keys = QPushButton()
        self.btn_go_keys.clicked.connect(lambda: self.navigate_requested.emit(1))

        self.btn_github = QPushButton()
        self.btn_github.clicked.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://github.com/Byaidu/PDFMathTranslate")
            )
        )

        h_layout.addWidget(self.btn_go_workspace)
        h_layout.addWidget(self.btn_go_keys)
        h_layout.addWidget(self.btn_github)

        outer.addWidget(header_card)

        # Rich HTML Guide Browser
        guide_card = QFrame()
        guide_card.setObjectName("CardFrame")
        g_layout = QVBoxLayout(guide_card)
        g_layout.setContentsMargins(16, 12, 16, 12)

        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setFrameShape(QFrame.Shape.NoFrame)
        g_layout.addWidget(self.browser, 1)

        outer.addWidget(guide_card, 1)

    def retranslate_ui(self) -> None:
        self.lbl_title.setText(tr("help_title"))
        self.lbl_subtitle.setText(tr("help_subtitle"))
        self.btn_go_workspace.setText(tr("help_btn_go_workspace"))
        self.btn_go_keys.setText(tr("help_btn_go_keys"))
        self.btn_github.setText(tr("help_btn_github"))
        self.browser.setHtml(get_user_guide_html(I18nManager.get_lang()))
