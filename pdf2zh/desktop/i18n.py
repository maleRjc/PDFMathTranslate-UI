"""Internationalization (i18n) and localized User Guide for PDFMathTranslate Desktop UI."""

from __future__ import annotations

from typing import Any
from pdf2zh.desktop.metadata import AppSettings

UI_LANGUAGES: dict[str, str] = {
    "zh": "简体中文",
    "zh-TW": "繁體中文",
    "en": "English",
    "ja": "日本語",
    "ko": "한국어",
    "fr": "Français",
    "de": "Deutsch",
    "ru": "Русский",
    "es": "Español",
    "it": "Italiano",
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    "zh": {
        # Window & Navigation
        "window_title": "PDFMathTranslate 桌面版 v{version} — AI 学术 PDF 双语翻译工具",
        "nav_workspace": "📄  翻译工作台",
        "nav_ai_keys": "🔑  AI 密钥与服务商",
        "nav_trans_settings": "⚙️  翻译与排版设置",
        "nav_output_settings": "📁  输出与任务设置",
        "nav_system_settings": "🛠️  系统与高级设置",
        "nav_user_guide": "📖  使用说明与帮助",
        "ui_lang_label": "🌐 界面语言:",
        "sb_default_service": "默认服务: {svc}",
        "sb_default_mode": "默认引擎: {mode} | 线程: {threads}",
        "sb_proxy_on": "网络代理: 已开启",
        "sb_proxy_off": "网络代理: 未开启",
        "status_config_path": "配置文件路径: {path}",
        # Menu bar
        "menu_file": "文件 (File)",
        "menu_add_files": "添加 PDF/Word 文件...",
        "menu_add_folder": "添加文件夹...",
        "menu_settings": "AI 密钥与设置...",
        "menu_help": "帮助 (Help)",
        "menu_open_guide": "打开使用说明...",
        # Workspace
        "drop_hint": "📄 拖入 PDF / Word 文件或文件夹，或点击右侧添加",
        "btn_add_file": "＋ 文件",
        "btn_add_folder": "＋ 文件夹",
        "btn_add_url": "＋ 链接",
        "btn_clear": "清空",
        "col_filename": "文档名称",
        "col_status": "状态",
        "col_progress": "进度",
        "col_time": "耗时",
        "status_pending": "待翻译",
        "status_running": "⏳ 翻译中",
        "status_done": "✅ 已完成",
        "status_failed": "❌ 失败",
        "opt_card_title": "翻译参数配置",
        "lbl_ai_service": "AI / 翻译服务:",
        "btn_cfg_key": "🔑 配置密钥",
        "tip_cfg_key": "打开该服务商的 API Key 与参数设置",
        "lbl_model": "使用模型 (Model):",
        "model_default_none": "默认 (无需指定模型)",
        "lbl_trans_lang": "翻译语言:",
        "tip_swap_lang": "交换源语言与目标语言",
        "lbl_page_range": "翻译页码:",
        "pages_all": "全部页面 (All)",
        "pages_first": "仅第 1 页",
        "pages_first5": "前 5 页 (1-5)",
        "pages_custom": "自定义页码范围",
        "pages_custom_ph": "如: 1-3, 5, 8-10",
        "lbl_engine_mode": "排版引擎:",
        "mode_fast_short": "fast (标准 AI 布局分析)",
        "mode_ultrafast_short": "ultrafast (极速原生文本流)",
        "mode_babeldoc_short": "babeldoc (BabelDOC 排版后端)",
        "mode_precise_short": "precise (Precise v2 精准模式)",
        "lbl_output_opt": "输出选项:",
        "chk_mono_short": "纯译文 (Mono)",
        "chk_dual_short": "双语对照 (Dual)",
        "chk_ignore_cache_short": "忽略缓存",
        "btn_start": "🚀 开始翻译",
        "btn_stop": "⏹ 停止",
        "btn_log": "📋 日志",
        "btn_help_quick": "📖 使用说明",
        "prog_ready": "就绪 — 添加 PDF 文档后点击「开始翻译」",
        "prog_stopping": "正在停止当前翻译任务...",
        "prog_processing": "正在处理: {name}",
        "prog_all_done": "🎉 队列任务处理完毕",
        "prog_error": "出错: {err}",
        "msg_no_files": "请先添加至少一个 PDF 或 Word 文件到列表中。",
        "msg_unconfigured_title": "未配置 API Key",
        "msg_unconfigured_body": "当前选择的「{svc}」尚未配置 API Key，是否立即前往设置页面配置？",
        "msg_stop_first": "请先停止正在运行的翻译任务。",
        "msg_no_pdf_in_dir": "所选文件夹中未找到可翻译的 PDF/Word 文件。",
        "dlg_add_url_title": "添加在线 PDF 链接",
        "dlg_add_url_label": "请输入以 http:// 或 https:// 开头的在线 PDF 地址 (如 arXiv 论文链接):",
        # PDF Viewer
        "pdf_orig": "原文",
        "pdf_mono": "纯译文 (Mono)",
        "pdf_dual": "双语对照 (Dual)",
        "pdf_total_pages": "/ {count} 页",
        "pdf_open_ext": "外部打开",
        "pdf_open_ext_tip": "使用系统默认 PDF 阅读器打开当前文档",
        "pdf_reveal": "打开所在目录",
        "pdf_reveal_tip": "在系统文件管理器中显示当前文件",
        "pdf_empty_hint": "在左侧选择或拖入 PDF 文件后可在此预览原文与译文",
        "pdf_err_load": "无法预览该文档: {err}",
        # Provider statuses
        "status_free": "免配置",
        "status_ready": "已就绪",
        "status_need_key": "待配置密钥",
        "status_configured": "已配置",
        # AI Providers Page
        "ai_list_title": "AI 与翻译服务商",
        "ai_search_ph": "🔍 搜索服务商 (如 DeepSeek, OpenAI, 智谱...)",
        "ai_btn_doc": "🔗 获取 API Key / 官方控制台",
        "ai_current_default": " (当前默认服务)",
        "ai_no_key_needed": "✅ 该翻译服务无需配置 API Key 或环境变量，可直接设为默认并在工作台中使用。",
        "ai_cli_hint": "💡 提示：配置会自动保存在 ~/.config/PDFMathTranslate/config.json 中，CLI 与桌面端共享（命令行标识：-s {name}）。",
        "ai_btn_save": "💾 保存当前服务配置",
        "ai_btn_test": "⚡ 测试连接",
        "ai_btn_testing": "⏳ 正在测试...",
        "ai_btn_set_default": "⭐ 设为默认翻译服务",
        "ai_btn_reset": "恢复默认项",
        "btn_show": "显示",
        "btn_hide": "隐藏",
        "ai_msg_saved": "✅ 已保存「{svc}」的配置信息。",
        "ai_msg_default_set": "⭐ 已将「{svc}」设为默认翻译服务并保存配置。",
        "ai_msg_reset": "已将「{svc}」恢复为默认参数。",
        "ai_msg_testing": "正在连接「{svc}」进行翻译测试，请稍候...",
        # Translation Settings Page
        "ts_card1_title": "默认语言与翻译引擎模式",
        "ts_card1_sub": "配置启动工作台时的默认源语言、目标语言以及排版解析引擎。",
        "ts_lbl_source": "默认源语言 (Source):",
        "ts_lbl_target": "默认目标语言 (Target):",
        "ts_lbl_mode": "默认翻译模式 (Mode):",
        "ts_mode_fast": "fast — 标准模式 (DocLayout-YOLO 布局分析，推荐)",
        "ts_mode_ultrafast": "ultrafast — 极速模式 (免神经网络模型，纯原生文本流极速解析)",
        "ts_mode_babeldoc": "babeldoc — BabelDOC 增强排版后端 (实验性支持复杂版面)",
        "ts_mode_precise": "precise — Precise v2 精准模式 (需安装 pdf2zh_next)",
        "ts_card2_title": "公式保护与字体排版设置",
        "ts_card2_sub": "控制数学公式字体/字符的正则匹配规则，以及输出 PDF 字体子集化与兼容性。",
        "ts_vfont_ph": "留空使用内置公式字体规则，例如: (CM[^R]|MS.M|XY|MT|BL|RM|EU|LA|RS).*",
        "ts_btn_vfont_preset": "填入 LaTeX 常用数学字体正则",
        "ts_vchar_ph": "自定义视为公式的字符正则表达式 (-c / --vchar)，留空使用默认规则",
        "ts_chk_skip_subset": "跳过字体子集化 (--skip-subset-fonts，提升部分阅读器兼容性，但文件体积更大)",
        "ts_chk_compatible": "转换输入文档为 PDF/A 格式 (--compatible，修复部分破损 PDF 结构)",
        "ts_lbl_vfont": "公式字体正则 (vfont):",
        "ts_lbl_vchar": "公式字符正则 (vchar):",
        "ts_card3_title": "AI 大模型自定义提示词 (Custom Prompt)",
        "ts_card3_sub": "针对支持自定义 Prompt 的大模型（OpenAI、DeepSeek、Gemini、Qwen、Ollama 等）定制翻译指令。支持变量：${lang_in}、${lang_out}、${text}。",
        "ts_chk_use_prompt": "启用自定义大模型翻译提示词 (Prompt Template)",
        "ts_btn_default_prompt": "填入默认学术翻译模板",
        "ts_btn_import_prompt": "从文件导入 Prompt (.txt/.md)",
        "ts_card4_title": "OCR 扫描件识别设置",
        "ts_card4_sub": "当遇到纯图片扫描页时，PyMuPDF 可调用 Tesseract 语言包自动识别文字层。",
        "ts_ocr_lang_ph": "留空根据源语言自动匹配（如 eng、chi_sim、eng+deu）",
        "ts_tess_ph": "留空使用 ~/.cache/pdf2zh/tessdata 自动下载或环境变量 TESSDATA_PREFIX",
        "ts_btn_browse_dir": "选择目录...",
        "ts_lbl_ocr_lang": "OCR 语言覆盖:",
        "ts_lbl_tess_dir": "TESSDATA 目录:",
        "ts_btn_save": "💾 保存翻译与排版设置",
        "ts_msg_saved": "✅ 已保存翻译与排版设置",
        # Output Settings Page
        "os_card1_title": "输出目录设置",
        "os_card1_sub": "设置翻译后生成的 PDF 文件保存位置。",
        "os_chk_save_next": "默认保存在源 PDF 文件所在目录（推荐，方便就地对照查看）",
        "os_lbl_fixed_dir": "固定输出目录:",
        "os_dir_ph": "选择自定义输出目录，例如 ~/Downloads/PDF_Translated",
        "os_btn_browse": "浏览文件夹...",
        "os_btn_open_dir": "打开目录",
        "os_card2_title": "输出文档类型开关",
        "os_card2_sub": "可选择同时生成纯译文版与双语对照版，或只保留其中一种。",
        "os_chk_mono": "生成纯译文 PDF (文件名后缀 -mono.pdf)",
        "os_chk_dual": "生成双语对照 PDF (文件名后缀 -dual.pdf，一页原文一页译文对照)",
        "os_card3_title": "并发线程与任务自动化",
        "os_card3_sub": "控制翻译请求并发度（注意不要超过所选 AI 服务商的速率限制 RPM/QPS）。",
        "os_lbl_threads": "默认并发线程数 (-t):",
        "os_chk_auto_preview": "翻译完成后自动在右侧内置阅读器中预览生成的文档",
        "os_chk_auto_open_dir": "队列全部翻译完成后自动打开输出目录",
        "os_btn_save": "💾 保存输出与任务设置",
        "os_msg_saved": "✅ 已保存输出与任务设置",
        # System Settings Page
        "ss_card1_title": "网络代理设置 (HTTP / HTTPS Proxy)",
        "ss_card1_sub": "访问 Google 翻译、OpenAI、Gemini 等海外服务或下载 HuggingFace 模型时可开启本地代理。",
        "ss_chk_proxy": "启用自定义网络代理 (自动设置 HTTP_PROXY 与 HTTPS_PROXY)",
        "ss_lbl_proxy_url": "代理地址:",
        "ss_proxy_ph": "例如 http://127.0.0.1:7890 或 socks5://127.0.0.1:1080",
        "ss_card2_title": "翻译缓存管理 (SQLite Cache)",
        "ss_card2_sub": "PDFMathTranslate 会自动缓存已翻译过的段落，避免重复消耗大模型 Token。",
        "ss_chk_ignore_cache": "忽略翻译缓存 (--ignore-cache，每次强制重新请求 AI 翻译)",
        "ss_btn_refresh_cache": "🔄 刷新缓存统计",
        "ss_btn_clear_cache": "🧹 一键清空翻译缓存",
        "ss_btn_reveal_cache": "查看缓存文件",
        "ss_card3_title": "ONNX 布局模型与硬件加速设置",
        "ss_card3_sub": "配置 DocLayout-YOLO 页面布局分析模型的推理后端与自定义模型路径。",
        "ss_lbl_onnx_backend": "ONNX 推理后端:",
        "ss_lbl_onnx_path": "自定义 ONNX 模型:",
        "ss_onnx_ph": "留空使用内置/自动加载的 DocLayout-YOLO ONNX 模型",
        "ss_btn_browse_onnx": "选择 .onnx 文件...",
        "ss_card4_title": "配置文件管理与备份",
        "ss_btn_open_cfg": "📂 查看配置文件",
        "ss_btn_export_cfg": "📤 导出配置备份 (.json)",
        "ss_btn_import_cfg": "📥 导入配置文件 (.json)",
        "ss_btn_reset_all": "⚠️ 重置所有设置",
        "ss_btn_save": "💾 保存系统与高级设置",
        "ss_msg_saved": "✅ 已保存系统与高级设置",
        # Help / User Guide Page
        "help_title": "📖 PDFMathTranslate 桌面版使用说明",
        "help_subtitle": "保留公式、图表、目录与排版结构的 AI 学术论文双语翻译工具",
        "help_btn_go_workspace": "🚀 前往翻译工作台",
        "help_btn_go_keys": "🔑 去配置 AI 密钥",
        "help_btn_github": "🌐 访问 GitHub 仓库",
    },
    "zh-TW": {
        "window_title": "PDFMathTranslate 桌面版 v{version} — AI 學術 PDF 雙語翻譯工具",
        "nav_workspace": "📄  翻譯工作台",
        "nav_ai_keys": "🔑  AI 金鑰與服務商",
        "nav_trans_settings": "⚙️  翻譯與排版設定",
        "nav_output_settings": "📁  輸出與任務設定",
        "nav_system_settings": "🛠️  系統與進階設定",
        "nav_user_guide": "📖  使用說明與說明書",
        "ui_lang_label": "🌐 介面語言:",
        "sb_default_service": "預設服務: {svc}",
        "sb_default_mode": "預設引擎: {mode} | 執行緒: {threads}",
        "sb_proxy_on": "網路代理: 已開啟",
        "sb_proxy_off": "網路代理: 未開啟",
        "status_config_path": "設定檔路徑: {path}",
        "menu_file": "檔案 (File)",
        "menu_add_files": "加入 PDF/Word 檔案...",
        "menu_add_folder": "加入資料夾...",
        "menu_settings": "AI 金鑰與設定...",
        "menu_help": "說明 (Help)",
        "menu_open_guide": "開啟使用說明...",
        "drop_hint": "📄 拖入 PDF / Word 檔案或資料夾，或點擊右側新增",
        "btn_add_file": "＋ 檔案",
        "btn_add_folder": "＋ 資料夾",
        "btn_add_url": "＋ 連結",
        "btn_clear": "清空",
        "col_filename": "文件名稱",
        "col_status": "狀態",
        "col_progress": "進度",
        "col_time": "耗時",
        "status_pending": "待翻譯",
        "status_running": "⏳ 翻譯中",
        "status_done": "✅ 已完成",
        "status_failed": "❌ 失敗",
        "opt_card_title": "翻譯參數設定",
        "lbl_ai_service": "AI / 翻譯服務:",
        "btn_cfg_key": "🔑 設定金鑰",
        "tip_cfg_key": "開啟該服務商的 API Key 與參數設定",
        "lbl_model": "使用模型 (Model):",
        "model_default_none": "預設 (無需指定模型)",
        "lbl_trans_lang": "翻譯語言:",
        "tip_swap_lang": "交換來源語言與目標語言",
        "lbl_page_range": "翻譯頁碼:",
        "pages_all": "全部頁面 (All)",
        "pages_first": "僅第 1 頁",
        "pages_first5": "前 5 頁 (1-5)",
        "pages_custom": "自訂頁碼範圍",
        "pages_custom_ph": "例如: 1-3, 5, 8-10",
        "lbl_engine_mode": "排版引擎:",
        "mode_fast_short": "fast (標準 AI 版面分析)",
        "mode_ultrafast_short": "ultrafast (極速原生文字流)",
        "mode_babeldoc_short": "babeldoc (BabelDOC 排版後端)",
        "mode_precise_short": "precise (Precise v2 精準模式)",
        "lbl_output_opt": "輸出選項:",
        "chk_mono_short": "純譯文 (Mono)",
        "chk_dual_short": "雙語對照 (Dual)",
        "chk_ignore_cache_short": "忽略快取",
        "btn_start": "🚀 開始翻譯",
        "btn_stop": "⏹ 停止",
        "btn_log": "📋 日誌",
        "btn_help_quick": "📖 使用說明",
        "prog_ready": "就緒 — 加入 PDF 文件後點擊「開始翻譯」",
        "prog_stopping": "正在停止目前翻譯任務...",
        "prog_processing": "正在處理: {name}",
        "prog_all_done": "🎉 佇列任務處理完畢",
        "prog_error": "出錯: {err}",
        "msg_no_files": "請先加入至少一個 PDF 或 Word 檔案到清單中。",
        "msg_unconfigured_title": "尚未設定 API Key",
        "msg_unconfigured_body": "目前選擇的「{svc}」尚未設定 API Key，是否立即前往設定頁面？",
        "msg_stop_first": "請先停止正在執行的翻譯任務。",
        "msg_no_pdf_in_dir": "所選資料夾中未找到可翻譯的 PDF/Word 檔案。",
        "dlg_add_url_title": "加入線上 PDF 連結",
        "dlg_add_url_label": "請輸入以 http:// 或 https:// 開頭的線上 PDF 網址 (如 arXiv 論文連結):",
        "pdf_orig": "原文",
        "pdf_mono": "純譯文 (Mono)",
        "pdf_dual": "雙語對照 (Dual)",
        "pdf_total_pages": "/ {count} 頁",
        "pdf_open_ext": "外部開啟",
        "pdf_open_ext_tip": "使用系統預設 PDF 閱讀器開啟目前文件",
        "pdf_reveal": "開啟所在目錄",
        "pdf_reveal_tip": "在檔案管理員中顯示目前檔案",
        "pdf_empty_hint": "在左側選擇或拖入 PDF 檔案後可在此預覽原文與譯文",
        "pdf_err_load": "無法預覽該文件: {err}",
        "status_free": "免設定",
        "status_ready": "已就緒",
        "status_need_key": "待設定金鑰",
        "status_configured": "已設定",
        "ai_list_title": "AI 與翻譯服務商",
        "ai_search_ph": "🔍 搜尋服務商 (如 DeepSeek, OpenAI, Gemini...)",
        "ai_btn_doc": "🔗 取得 API Key / 官方主控台",
        "ai_current_default": " (目前預設服務)",
        "ai_no_key_needed": "✅ 該翻譯服務無需設定 API Key 或環境變數，可直接設為預設並在工作台中使用。",
        "ai_cli_hint": "💡 提示：設定會自動儲存在 ~/.config/PDFMathTranslate/config.json 中，CLI 與桌面端共用（指令列識別：-s {name}）。",
        "ai_btn_save": "💾 儲存目前服務設定",
        "ai_btn_test": "⚡ 測試連線",
        "ai_btn_testing": "⏳ 正在測試...",
        "ai_btn_set_default": "⭐ 設為預設翻譯服務",
        "ai_btn_reset": "恢復預設值",
        "btn_show": "顯示",
        "btn_hide": "隱藏",
        "ai_msg_saved": "✅ 已儲存「{svc}」的設定資訊。",
        "ai_msg_default_set": "⭐ 已將「{svc}」設為預設翻譯服務並儲存設定。",
        "ai_msg_reset": "已將「{svc}」恢復為預設參數。",
        "ai_msg_testing": "正在連線「{svc}」進行翻譯測試，請稍候...",
        "ts_card1_title": "預設語言與翻譯引擎模式",
        "ts_card1_sub": "設定啟動工作台時的預設來源語言、目標語言以及排版解析引擎。",
        "ts_lbl_source": "預設來源語言 (Source):",
        "ts_lbl_target": "預設目標語言 (Target):",
        "ts_lbl_mode": "預設翻譯模式 (Mode):",
        "ts_mode_fast": "fast — 標準模式 (DocLayout-YOLO 版面分析，推薦)",
        "ts_mode_ultrafast": "ultrafast — 極速模式 (免神經網路模型，純原生文字流極速解析)",
        "ts_mode_babeldoc": "babeldoc — BabelDOC 增強排版後端 (實驗性支援複雜版面)",
        "ts_mode_precise": "precise — Precise v2 精準模式 (需安裝 pdf2zh_next)",
        "ts_card2_title": "公式保護與字型排版設定",
        "ts_card2_sub": "控制數學公式字型/字元的正規表示式規則，以及輸出 PDF 字型子集化與相容性。",
        "ts_vfont_ph": "留空使用內建公式字型規則，例如: (CM[^R]|MS.M|XY|MT|BL|RM|EU|LA|RS).*",
        "ts_btn_vfont_preset": "填入 LaTeX 常用數學字型正則",
        "ts_vchar_ph": "自訂視為公式的字元正規表示式 (-c / --vchar)，留空使用預設規則",
        "ts_chk_skip_subset": "略過字型子集化 (--skip-subset-fonts，提升部分閱讀器相容性，但檔案體積較大)",
        "ts_chk_compatible": "轉換輸入文件為 PDF/A 格式 (--compatible，修復部分受損 PDF 結構)",
        "ts_lbl_vfont": "公式字型正則 (vfont):",
        "ts_lbl_vchar": "公式字元正則 (vchar):",
        "ts_card3_title": "AI 大模型自訂提示詞 (Custom Prompt)",
        "ts_card3_sub": "針對支援自訂 Prompt 的大模型定制翻譯指令。支援變數：${lang_in}、${lang_out}、${text}。",
        "ts_chk_use_prompt": "啟用自訂大模型翻譯提示詞 (Prompt Template)",
        "ts_btn_default_prompt": "填入預設學術翻譯範本",
        "ts_btn_import_prompt": "從檔案匯入 Prompt (.txt/.md)",
        "ts_card4_title": "OCR 掃描件辨識設定",
        "ts_card4_sub": "當遇到純圖片掃描頁時，PyMuPDF 可呼叫 Tesseract 語言包自動辨識文字層。",
        "ts_ocr_lang_ph": "留空根據來源語言自動配對（如 eng、chi_tra、eng+deu）",
        "ts_tess_ph": "留空使用 ~/.cache/pdf2zh/tessdata 自動下載或環境變數 TESSDATA_PREFIX",
        "ts_btn_browse_dir": "選擇目錄...",
        "ts_lbl_ocr_lang": "OCR 語言覆蓋:",
        "ts_lbl_tess_dir": "TESSDATA 目錄:",
        "ts_btn_save": "💾 儲存翻譯與排版設定",
        "ts_msg_saved": "✅ 已儲存翻譯與排版設定",
        "os_card1_title": "輸出目錄設定",
        "os_card1_sub": "設定翻譯後產生的 PDF 檔案儲存位置。",
        "os_chk_save_next": "預設儲存在來源 PDF 檔案所在目錄（推薦，方便就地對照檢視）",
        "os_lbl_fixed_dir": "固定輸出目錄:",
        "os_dir_ph": "選擇自訂輸出目錄，例如 ~/Downloads/PDF_Translated",
        "os_btn_browse": "瀏覽資料夾...",
        "os_btn_open_dir": "開啟目錄",
        "os_card2_title": "輸出文件類型開關",
        "os_card2_sub": "可選擇同時產生純譯文版與雙語對照版，或只保留其中一種。",
        "os_chk_mono": "產生純譯文 PDF (檔名後綴 -mono.pdf)",
        "os_chk_dual": "產生雙語對照 PDF (檔名後綴 -dual.pdf，一頁原文一頁譯文對照)",
        "os_card3_title": "並行執行緒與任務自動化",
        "os_card3_sub": "控制翻譯請求並行度（注意不要超過所選 AI 服務商的速率限制 RPM/QPS）。",
        "os_lbl_threads": "預設並行執行緒數 (-t):",
        "os_chk_auto_preview": "翻譯完成後自動在右側內建閱讀器中預覽產生的文件",
        "os_chk_auto_open_dir": "佇列全部翻譯完成後自動開啟輸出目錄",
        "os_btn_save": "💾 儲存輸出與任務設定",
        "os_msg_saved": "✅ 已儲存輸出與任務設定",
        "ss_card1_title": "網路代理設定 (HTTP / HTTPS Proxy)",
        "ss_card1_sub": "連線 Google 翻譯、OpenAI、Gemini 等服務或下載模型時可開啟本地代理。",
        "ss_chk_proxy": "啟用自訂網路代理 (自動設定 HTTP_PROXY 與 HTTPS_PROXY)",
        "ss_lbl_proxy_url": "代理位址:",
        "ss_proxy_ph": "例如 http://127.0.0.1:7890 或 socks5://127.0.0.1:1080",
        "ss_card2_title": "翻譯快取管理 (SQLite Cache)",
        "ss_card2_sub": "PDFMathTranslate 會自動快取已翻譯過的段落，避免重複消耗大模型 Token。",
        "ss_chk_ignore_cache": "忽略翻譯快取 (--ignore-cache，每次強制重新請求 AI 翻譯)",
        "ss_btn_refresh_cache": "🔄 重新整理快取統計",
        "ss_btn_clear_cache": "🧹 一鍵清空翻譯快取",
        "ss_btn_reveal_cache": "檢視快取檔案",
        "ss_card3_title": "ONNX 版面模型與硬體加速設定",
        "ss_card3_sub": "設定 DocLayout-YOLO 頁面版面分析模型的推論後端與自訂模型路徑。",
        "ss_lbl_onnx_backend": "ONNX 推論後端:",
        "ss_lbl_onnx_path": "自訂 ONNX 模型:",
        "ss_onnx_ph": "留空使用內建/自動載入的 DocLayout-YOLO ONNX 模型",
        "ss_btn_browse_onnx": "選擇 .onnx 檔案...",
        "ss_card4_title": "設定檔管理與備份",
        "ss_btn_open_cfg": "📂 檢視設定檔",
        "ss_btn_export_cfg": "📤 匯出設定備份 (.json)",
        "ss_btn_import_cfg": "📥 匯入設定檔 (.json)",
        "ss_btn_reset_all": "⚠️ 重設所有設定",
        "ss_btn_save": "💾 儲存系統與進階設定",
        "ss_msg_saved": "✅ 已儲存系統與進階設定",
        "help_title": "📖 PDFMathTranslate 桌面版使用說明",
        "help_subtitle": "保留公式、圖表、目錄與排版結構的 AI 學術論文雙語翻譯工具",
        "help_btn_go_workspace": "🚀 前往翻譯工作台",
        "help_btn_go_keys": "🔑 去設定 AI 金鑰",
        "help_btn_github": "🌐 造訪 GitHub 專案",
    },
    "en": {
        "window_title": "PDFMathTranslate Desktop v{version} — AI Scientific PDF Translator",
        "nav_workspace": "📄  Workspace",
        "nav_ai_keys": "🔑  AI Keys & Providers",
        "nav_trans_settings": "⚙️  Translation & Layout",
        "nav_output_settings": "📁  Output & Tasks",
        "nav_system_settings": "🛠️  System & Advanced",
        "nav_user_guide": "📖  User Guide & Help",
        "ui_lang_label": "🌐 Language:",
        "sb_default_service": "Default: {svc}",
        "sb_default_mode": "Mode: {mode} | Threads: {threads}",
        "sb_proxy_on": "Proxy: Enabled",
        "sb_proxy_off": "Proxy: Disabled",
        "status_config_path": "Config File: {path}",
        "menu_file": "File",
        "menu_add_files": "Add PDF/Word Files...",
        "menu_add_folder": "Add Folder...",
        "menu_settings": "AI Keys & Settings...",
        "menu_help": "Help",
        "menu_open_guide": "User Guide...",
        "drop_hint": "📄 Drag & drop PDF / Word files or folders here, or click Add",
        "btn_add_file": "＋ Files",
        "btn_add_folder": "＋ Folder",
        "btn_add_url": "＋ URL",
        "btn_clear": "Clear",
        "col_filename": "Document",
        "col_status": "Status",
        "col_progress": "Progress",
        "col_time": "Time",
        "status_pending": "Pending",
        "status_running": "⏳ Running",
        "status_done": "✅ Done",
        "status_failed": "❌ Failed",
        "opt_card_title": "Translation Options",
        "lbl_ai_service": "AI / Service:",
        "btn_cfg_key": "🔑 API Key",
        "tip_cfg_key": "Configure API Key and parameters for this provider",
        "lbl_model": "Model:",
        "model_default_none": "Default (No model required)",
        "lbl_trans_lang": "Languages:",
        "tip_swap_lang": "Swap source and target languages",
        "lbl_page_range": "Pages:",
        "pages_all": "All Pages",
        "pages_first": "First Page Only",
        "pages_first5": "First 5 Pages (1-5)",
        "pages_custom": "Custom Page Range",
        "pages_custom_ph": "e.g. 1-3, 5, 8-10",
        "lbl_engine_mode": "Engine Mode:",
        "mode_fast_short": "fast (Standard AI Layout)",
        "mode_ultrafast_short": "ultrafast (Native Text Stream)",
        "mode_babeldoc_short": "babeldoc (BabelDOC Backend)",
        "mode_precise_short": "precise (Precise v2 Kernel)",
        "lbl_output_opt": "Outputs:",
        "chk_mono_short": "Mono PDF",
        "chk_dual_short": "Dual PDF",
        "chk_ignore_cache_short": "No Cache",
        "btn_start": "🚀 Translate",
        "btn_stop": "⏹ Stop",
        "btn_log": "📋 Logs",
        "btn_help_quick": "📖 Guide",
        "prog_ready": "Ready — Add PDF files and click 'Translate'",
        "prog_stopping": "Stopping current translation task...",
        "prog_processing": "Processing: {name}",
        "prog_all_done": "🎉 All tasks in queue completed!",
        "prog_error": "Error: {err}",
        "msg_no_files": "Please add at least one PDF or Word document to the queue first.",
        "msg_unconfigured_title": "API Key Required",
        "msg_unconfigured_body": "Provider '{svc}' is not configured yet. Open AI Key Settings now?",
        "msg_stop_first": "Please stop the running translation task first.",
        "msg_no_pdf_in_dir": "No translatable PDF/Word files found in the selected folder.",
        "dlg_add_url_title": "Add Online PDF URL",
        "dlg_add_url_label": "Enter an http:// or https:// PDF link (e.g. arXiv paper URL):",
        "pdf_orig": "Original",
        "pdf_mono": "Translated (Mono)",
        "pdf_dual": "Bilingual (Dual)",
        "pdf_total_pages": "/ {count} pages",
        "pdf_open_ext": "Open External",
        "pdf_open_ext_tip": "Open current PDF in system default viewer",
        "pdf_reveal": "Reveal in Finder",
        "pdf_reveal_tip": "Reveal current PDF file in Finder / Explorer",
        "pdf_empty_hint": "Select or drop a PDF file on the left to preview Original, Mono, and Dual versions here",
        "pdf_err_load": "Unable to preview document: {err}",
        "status_free": "No Key Needed",
        "status_ready": "Ready",
        "status_need_key": "Key Required",
        "status_configured": "Configured",
        "ai_list_title": "AI & Translation Providers",
        "ai_search_ph": "🔍 Search providers (OpenAI, DeepSeek, Gemini...)",
        "ai_btn_doc": "🔗 Get API Key / Console",
        "ai_current_default": " (Default)",
        "ai_no_key_needed": "✅ This translation service requires no API key and can be used right away.",
        "ai_cli_hint": "💡 Tip: Settings are persisted in ~/.config/PDFMathTranslate/config.json and shared with the CLI (flag: -s {name}).",
        "ai_btn_save": "💾 Save Provider Config",
        "ai_btn_test": "⚡ Test Connection",
        "ai_btn_testing": "⏳ Testing...",
        "ai_btn_set_default": "⭐ Set as Default",
        "ai_btn_reset": "Reset Defaults",
        "btn_show": "Show",
        "btn_hide": "Hide",
        "ai_msg_saved": "✅ Saved configuration for '{svc}'.",
        "ai_msg_default_set": "⭐ Set '{svc}' as default translation service and saved config.",
        "ai_msg_reset": "Reset '{svc}' to default parameters.",
        "ai_msg_testing": "Testing connection to '{svc}', please wait...",
        "ts_card1_title": "Default Languages & Engine Mode",
        "ts_card1_sub": "Configure default source/target languages and layout parsing engine.",
        "ts_lbl_source": "Default Source Lang:",
        "ts_lbl_target": "Default Target Lang:",
        "ts_lbl_mode": "Default Engine Mode:",
        "ts_mode_fast": "fast — Standard Mode (DocLayout-YOLO neural layout, recommended)",
        "ts_mode_ultrafast": "ultrafast — Ultrafast Mode (No neural model, native text stream)",
        "ts_mode_babeldoc": "babeldoc — BabelDOC Experimental Backend",
        "ts_mode_precise": "precise — Precise v2 Mode (requires pdf2zh_next)",
        "ts_card2_title": "Formula Preservation & Typography",
        "ts_card2_sub": "Configure regex patterns for math formula fonts/characters and PDF compatibility.",
        "ts_vfont_ph": "Leave empty for default rules, e.g. (CM[^R]|MS.M|XY|MT|BL|RM|EU|LA|RS).*",
        "ts_btn_vfont_preset": "Fill Common LaTeX Math Font Regex",
        "ts_vchar_ph": "Custom regex for formula characters (-c / --vchar), leave empty for default",
        "ts_chk_skip_subset": "Skip font subsetting (--skip-subset-fonts, improves compatibility, larger file)",
        "ts_chk_compatible": "Convert input PDF to PDF/A format (--compatible)",
        "ts_lbl_vfont": "Formula Font Regex (vfont):",
        "ts_lbl_vchar": "Formula Char Regex (vchar):",
        "ts_card3_title": "Custom LLM Prompt Template",
        "ts_card3_sub": "Customize system prompt for LLM translators. Supported variables: ${lang_in}, ${lang_out}, ${text}.",
        "ts_chk_use_prompt": "Enable Custom LLM Prompt Template",
        "ts_btn_default_prompt": "Restore Default Academic Prompt",
        "ts_btn_import_prompt": "Import Prompt from File (.txt/.md)",
        "ts_card4_title": "OCR Settings for Scanned PDFs",
        "ts_card4_sub": "Configure Tesseract language codes for scanned image-only pages.",
        "ts_ocr_lang_ph": "Leave empty for auto detection (e.g. eng, chi_sim, eng+deu)",
        "ts_tess_ph": "Leave empty for ~/.cache/pdf2zh/tessdata or TESSDATA_PREFIX",
        "ts_btn_browse_dir": "Browse...",
        "ts_lbl_ocr_lang": "OCR Language Override:",
        "ts_lbl_tess_dir": "TESSDATA Directory:",
        "ts_btn_save": "💾 Save Translation & Layout Settings",
        "ts_msg_saved": "✅ Translation & Layout settings saved",
        "os_card1_title": "Output Directory",
        "os_card1_sub": "Choose where translated PDF files are saved.",
        "os_chk_save_next": "Save in the same folder as the source PDF (Recommended)",
        "os_lbl_fixed_dir": "Custom Output Folder:",
        "os_dir_ph": "Select output directory, e.g. ~/Downloads/PDF_Translated",
        "os_btn_browse": "Browse...",
        "os_btn_open_dir": "Open Folder",
        "os_card2_title": "Output Document Variants",
        "os_card2_sub": "Choose whether to generate Mono PDF, Dual PDF, or both.",
        "os_chk_mono": "Generate Monolingual Translated PDF (-mono.pdf)",
        "os_chk_dual": "Generate Bilingual Side-by-Side PDF (-dual.pdf)",
        "os_card3_title": "Concurrency & Automation",
        "os_card3_sub": "Control worker thread count (mind your AI provider's rate limit).",
        "os_lbl_threads": "Concurrent Threads (-t):",
        "os_chk_auto_preview": "Automatically preview translated PDF in built-in viewer when done",
        "os_chk_auto_open_dir": "Automatically open output folder when queue finishes",
        "os_btn_save": "💾 Save Output & Task Settings",
        "os_msg_saved": "✅ Output & Task settings saved",
        "ss_card1_title": "Network Proxy (HTTP / HTTPS)",
        "ss_card1_sub": "Configure local proxy for accessing OpenAI, Google, Gemini, or HuggingFace.",
        "ss_chk_proxy": "Enable Custom Network Proxy (sets HTTP_PROXY & HTTPS_PROXY)",
        "ss_lbl_proxy_url": "Proxy URL:",
        "ss_proxy_ph": "e.g. http://127.0.0.1:7890 or socks5://127.0.0.1:1080",
        "ss_card2_title": "Translation Cache (SQLite)",
        "ss_card2_sub": "Caches translated paragraphs locally to avoid redundant API token usage.",
        "ss_chk_ignore_cache": "Ignore translation cache (--ignore-cache, force re-translation)",
        "ss_btn_refresh_cache": "🔄 Refresh Stats",
        "ss_btn_clear_cache": "🧹 Clear Translation Cache",
        "ss_btn_reveal_cache": "Reveal Cache File",
        "ss_card3_title": "ONNX Layout Model & Hardware Acceleration",
        "ss_card3_sub": "Configure ONNX Runtime execution provider and custom model path.",
        "ss_lbl_onnx_backend": "ONNX Backend:",
        "ss_lbl_onnx_path": "Custom ONNX Model:",
        "ss_onnx_ph": "Leave empty to use built-in DocLayout-YOLO ONNX model",
        "ss_btn_browse_onnx": "Select .onnx...",
        "ss_card4_title": "Configuration File Backup & Reset",
        "ss_btn_open_cfg": "📂 Reveal Config File",
        "ss_btn_export_cfg": "📤 Export Config (.json)",
        "ss_btn_import_cfg": "📥 Import Config (.json)",
        "ss_btn_reset_all": "⚠️ Reset All Settings",
        "ss_btn_save": "💾 Save System & Advanced Settings",
        "ss_msg_saved": "✅ System & Advanced settings saved",
        "help_title": "📖 PDFMathTranslate Desktop User Guide",
        "help_subtitle": "AI Scientific PDF Translator with preserved formulas, figures, and layout",
        "help_btn_go_workspace": "🚀 Go to Workspace",
        "help_btn_go_keys": "🔑 Configure AI Keys",
        "help_btn_github": "🌐 Visit GitHub Repo",
    },
    "ja": {
        "window_title": "PDFMathTranslate デスクトップ版 v{version} — AI 学術 PDF 翻訳ツール",
        "nav_workspace": "📄  翻訳ワークスペース",
        "nav_ai_keys": "🔑  AI キー・プロバイダー設定",
        "nav_trans_settings": "⚙️  翻訳・組版設定",
        "nav_output_settings": "📁  出力・タスク設定",
        "nav_system_settings": "🛠️  システム・詳細設定",
        "nav_user_guide": "📖  使い方ガイド・ヘルプ",
        "ui_lang_label": "🌐 表示言語:",
        "sb_default_service": "既定サービス: {svc}",
        "sb_default_mode": "エンジン: {mode} | スレッド: {threads}",
        "sb_proxy_on": "プロキシ: 有効",
        "sb_proxy_off": "プロキシ: 無効",
        "status_config_path": "設定ファイル: {path}",
        "menu_file": "ファイル (File)",
        "menu_add_files": "PDF/Word ファイルを追加...",
        "menu_add_folder": "フォルダを追加...",
        "menu_settings": "AI キーと設定...",
        "menu_help": "ヘルプ (Help)",
        "menu_open_guide": "使い方ガイドを開く...",
        "drop_hint": "📄 PDF / Word ファイルやフォルダをここにドロップ、または右側から追加",
        "btn_add_file": "＋ ファイル",
        "btn_add_folder": "＋ フォルダ",
        "btn_add_url": "＋ URL",
        "btn_clear": "クリア",
        "col_filename": "ドキュメント名",
        "col_status": "状態",
        "col_progress": "進捗",
        "col_time": "時間",
        "status_pending": "待機中",
        "status_running": "⏳ 翻訳中",
        "status_done": "✅ 完了",
        "status_failed": "❌ 失敗",
        "opt_card_title": "翻訳オプション設定",
        "lbl_ai_service": "AI / 翻訳サービス:",
        "btn_cfg_key": "🔑 キー設定",
        "tip_cfg_key": "このサービスの API キーと詳細設定を開く",
        "lbl_model": "モデル (Model):",
        "model_default_none": "既定 (モデル指定不要)",
        "lbl_trans_lang": "翻訳言語:",
        "tip_swap_lang": "原文言語と翻訳先言語を入れ替え",
        "lbl_page_range": "ページ範囲:",
        "pages_all": "すべてのページ (All)",
        "pages_first": "最初の 1 ページのみ",
        "pages_first5": "最初の 5 ページ (1-5)",
        "pages_custom": "カスタム範囲",
        "pages_custom_ph": "例: 1-3, 5, 8-10",
        "lbl_engine_mode": "組版エンジン:",
        "mode_fast_short": "fast (標準 AI レイアウト解析)",
        "mode_ultrafast_short": "ultrafast (超高速テキスト解析)",
        "mode_babeldoc_short": "babeldoc (BabelDOC バックエンド)",
        "mode_precise_short": "precise (Precise v2 高精度モード)",
        "lbl_output_opt": "出力形式:",
        "chk_mono_short": "翻訳のみ (Mono)",
        "chk_dual_short": "対訳見開き (Dual)",
        "chk_ignore_cache_short": "キャッシュ無視",
        "btn_start": "🚀 翻訳開始",
        "btn_stop": "⏹ 停止",
        "btn_log": "📋 ログ",
        "btn_help_quick": "📖 ガイド",
        "prog_ready": "準備完了 — PDF を追加して「翻訳開始」をクリック",
        "prog_stopping": "翻訳タスクを停止しています...",
        "prog_processing": "処理中: {name}",
        "prog_all_done": "🎉 すべての翻訳タスクが完了しました",
        "prog_error": "エラー: {err}",
        "msg_no_files": "先に少なくとも1つの PDF または Word ファイルを追加してください。",
        "msg_unconfigured_title": "API キー未設定",
        "msg_unconfigured_body": "選択された「{svc}」は API キーが設定されていません。今すぐ設定画面を開きますか？",
        "msg_stop_first": "先に実行中の翻訳タスクを停止してください。",
        "msg_no_pdf_in_dir": "選択したフォルダ内に翻訳可能な PDF/Word ファイルが見つかりませんでした。",
        "dlg_add_url_title": "オンライン PDF URL を追加",
        "dlg_add_url_label": "http:// または https:// で始まる PDF リンクを入力 (arXiv など):",
        "pdf_orig": "原文",
        "pdf_mono": "翻訳文 (Mono)",
        "pdf_dual": "対訳 (Dual)",
        "pdf_total_pages": "/ {count} ページ",
        "pdf_open_ext": "外部で開く",
        "pdf_open_ext_tip": "システムの既定 PDF ビューアで開く",
        "pdf_reveal": "フォルダを開く",
        "pdf_reveal_tip": "Finder / エクスプローラーでファイルを表示",
        "pdf_empty_hint": "左側に PDF ファイルを追加・選択すると、ここで原文・翻訳文・対訳をプレビューできます",
        "pdf_err_load": "プレビューできません: {err}",
        "status_free": "設定不要",
        "status_ready": "準備完了",
        "status_need_key": "要キー設定",
        "status_configured": "設定済",
        "ai_list_title": "AI・翻訳プロバイダー一覧",
        "ai_search_ph": "🔍 プロバイダーを検索 (DeepSeek, OpenAI, Gemini...)",
        "ai_btn_doc": "🔗 API キー取得 / 公式コンソール",
        "ai_current_default": " (既定サービス)",
        "ai_no_key_needed": "✅ この翻訳サービスは API キー不要でそのまま利用できます。",
        "ai_cli_hint": "💡 ヒント：設定は ~/.config/PDFMathTranslate/config.json に保存され、CLI と共有されます（CLI 指定：-s {name}）。",
        "ai_btn_save": "💾 この設定を保存",
        "ai_btn_test": "⚡ 接続テスト",
        "ai_btn_testing": "⏳ テスト中...",
        "ai_btn_set_default": "⭐ 既定サービスに設定",
        "ai_btn_reset": "初期値に戻す",
        "btn_show": "表示",
        "btn_hide": "隠す",
        "ai_msg_saved": "✅ 「{svc}」の設定を保存しました。",
        "ai_msg_default_set": "⭐ 「{svc}」を既定サービスに設定し保存しました。",
        "ai_msg_reset": "「{svc}」を初期設定に戻しました。",
        "ai_msg_testing": "「{svc}」への接続をテストしています...",
        "ts_card1_title": "既定の言語と翻訳エンジンモード",
        "ts_card1_sub": "起動時の原文言語、翻訳先言語、およびレイアウト解析エンジンを設定します。",
        "ts_lbl_source": "既定の原文言語 (Source):",
        "ts_lbl_target": "既定の翻訳先言語 (Target):",
        "ts_lbl_mode": "既定のエンジンモード:",
        "ts_mode_fast": "fast — 標準モード (DocLayout-YOLO レイアウト解析、推奨)",
        "ts_mode_ultrafast": "ultrafast — 超高速モード (ニューラルモデル不使用、ネイティブテキスト解析)",
        "ts_mode_babeldoc": "babeldoc — BabelDOC 拡張組版バックエンド",
        "ts_mode_precise": "precise — Precise v2 高精度モード (要 pdf2zh_next)",
        "ts_card2_title": "数式保護とフォント組版設定",
        "ts_card2_sub": "数式フォント・文字の正規表現ルール、およびフォントサブセット化を設定します。",
        "ts_vfont_ph": "空欄で既定ルールを使用、例: (CM[^R]|MS.M|XY|MT|BL|RM|EU|LA|RS).*",
        "ts_btn_vfont_preset": "LaTeX 数式フォント正規表現を入力",
        "ts_vchar_ph": "数式文字とみなす正規表現 (-c / --vchar)、空欄で既定",
        "ts_chk_skip_subset": "フォントのサブセット化をスキップ (--skip-subset-fonts)",
        "ts_chk_compatible": "入力を PDF/A 形式に変換 (--compatible)",
        "ts_lbl_vfont": "数式フォント正規表現 (vfont):",
        "ts_lbl_vchar": "数式文字正規表現 (vchar):",
        "ts_card3_title": "AI カスタムプロンプト (Custom Prompt)",
        "ts_card3_sub": "LLM 用の翻訳プロンプトをカスタマイズします。利用可能な変数：${lang_in}、${lang_out}、${text}。",
        "ts_chk_use_prompt": "カスタムプロンプトを有効化",
        "ts_btn_default_prompt": "標準の学術翻訳テンプレートを入力",
        "ts_btn_import_prompt": "ファイルから読み込む (.txt/.md)",
        "ts_card4_title": "OCR スキャン文書設定",
        "ts_card4_sub": "画像のみのページに対して Tesseract OCR を実行する際の設定です。",
        "ts_ocr_lang_ph": "空欄で自動判定 (例: eng, jpn, chi_sim)",
        "ts_tess_ph": "空欄で ~/.cache/pdf2zh/tessdata または TESSDATA_PREFIX を使用",
        "ts_btn_browse_dir": "フォルダ選択...",
        "ts_lbl_ocr_lang": "OCR 言語指定:",
        "ts_lbl_tess_dir": "TESSDATA フォルダ:",
        "ts_btn_save": "💾 翻訳・組版設定を保存",
        "ts_msg_saved": "✅ 翻訳・組版設定を保存しました",
        "os_card1_title": "出力先フォルダ設定",
        "os_card1_sub": "翻訳後の PDF ファイルの保存先を設定します。",
        "os_chk_save_next": "元の PDF ファイルと同じフォルダに保存する（推奨）",
        "os_lbl_fixed_dir": "固定出力先フォルダ:",
        "os_dir_ph": "出力先を選択、例: ~/Downloads/PDF_Translated",
        "os_btn_browse": "参照...",
        "os_btn_open_dir": "フォルダを開く",
        "os_card2_title": "出力ファイルの形式",
        "os_card2_sub": "翻訳文のみ (Mono) と 対訳 (Dual) の出力有無を選択します。",
        "os_chk_mono": "純粋な翻訳 PDF を生成 (-mono.pdf)",
        "os_chk_dual": "見開き対訳 PDF を生成 (-dual.pdf)",
        "os_card3_title": "並列スレッド数と自動化",
        "os_card3_sub": "同時翻訳リクエスト数を制御します（API のレート制限にご注意ください）。",
        "os_lbl_threads": "既定の並列スレッド数 (-t):",
        "os_chk_auto_preview": "翻訳完了後に内蔵ビューアで自動的にプレビューする",
        "os_chk_auto_open_dir": "キュー完了後に出力フォルダを自動的に開く",
        "os_btn_save": "💾 出力・タスク設定を保存",
        "os_msg_saved": "✅ 出力・タスク設定を保存しました",
        "ss_card1_title": "ネットワークプロキシ設定 (HTTP / HTTPS)",
        "ss_card1_sub": "OpenAI、Google、Gemini、HuggingFace 接続用のローカルプロキシを設定します。",
        "ss_chk_proxy": "カスタムプロキシを有効化 (HTTP_PROXY / HTTPS_PROXY)",
        "ss_lbl_proxy_url": "プロキシ URL:",
        "ss_proxy_ph": "例: http://127.0.0.1:7890 または socks5://127.0.0.1:1080",
        "ss_card2_title": "翻訳キャッシュ管理 (SQLite)",
        "ss_card2_sub": "翻訳済みの段落をキャッシュし、API トークンの重複消費を防ぎます。",
        "ss_chk_ignore_cache": "翻訳キャッシュを無視する (--ignore-cache)",
        "ss_btn_refresh_cache": "🔄 統計を更新",
        "ss_btn_clear_cache": "🧹 キャッシュを消去",
        "ss_btn_reveal_cache": "キャッシュファイルを表示",
        "ss_card3_title": "ONNX レイアウトモデル・ハードウェアアクセラレーション",
        "ss_card3_sub": "DocLayout-YOLO モデルの推論バックエンドとカスタムモデルパスを設定します。",
        "ss_lbl_onnx_backend": "ONNX バックエンド:",
        "ss_lbl_onnx_path": "カスタム ONNX モデル:",
        "ss_onnx_ph": "空欄で標準の DocLayout-YOLO モデルを使用",
        "ss_btn_browse_onnx": ".onnx を選択...",
        "ss_card4_title": "設定ファイルのバックアップと初期化",
        "ss_btn_open_cfg": "📂 設定ファイルを表示",
        "ss_btn_export_cfg": "📤 設定をエクスポート (.json)",
        "ss_btn_import_cfg": "📥 設定をインポート (.json)",
        "ss_btn_reset_all": "⚠️ すべての設定を初期化",
        "ss_btn_save": "💾 システム・詳細設定を保存",
        "ss_msg_saved": "✅ システム・詳細設定を保存しました",
        "help_title": "📖 PDFMathTranslate デスクトップ版 使い方ガイド",
        "help_subtitle": "数式・図表・目次・レイアウトを維持する AI 学術 PDF 翻訳ツール",
        "help_btn_go_workspace": "🚀 翻訳ワークスペースへ",
        "help_btn_go_keys": "🔑 AI キーを設定する",
        "help_btn_github": "🌐 GitHub リポジトリを開く",
    },
    "ko": {
        "window_title": "PDFMathTranslate 데스크톱 v{version} — AI 학술 PDF 이중언어 번역 도구",
        "nav_workspace": "📄  번역 작업 공간",
        "nav_ai_keys": "🔑  AI 키 및 서비스",
        "nav_trans_settings": "⚙️  번역 및 조판 설정",
        "nav_output_settings": "📁  출력 및 작업 설정",
        "nav_system_settings": "🛠️  시스템 및 고급 설정",
        "nav_user_guide": "📖  사용 설명서 및 도움말",
        "ui_lang_label": "🌐 인터페이스 언어:",
        "sb_default_service": "기본 서비스: {svc}",
        "sb_default_mode": "기본 엔진: {mode} | 스레드: {threads}",
        "sb_proxy_on": "프록시: 켜짐",
        "sb_proxy_off": "프록시: 꺼짐",
        "status_config_path": "설정 파일 경로: {path}",
        "menu_file": "파일 (File)",
        "menu_add_files": "PDF/Word 파일 추가...",
        "menu_add_folder": "폴더 추가...",
        "menu_settings": "AI 키 및 설정...",
        "menu_help": "도움말 (Help)",
        "menu_open_guide": "사용 설명서 열기...",
        "drop_hint": "📄 PDF / Word 파일 또는 폴더를 여기에 드래그하거나 오른쪽 버튼을 클릭하세요",
        "btn_add_file": "＋ 파일",
        "btn_add_folder": "＋ 폴더",
        "btn_add_url": "＋ URL",
        "btn_clear": "지우기",
        "col_filename": "문서 이름",
        "col_status": "상태",
        "col_progress": "진행률",
        "col_time": "소요 시간",
        "status_pending": "대기 중",
        "status_running": "⏳ 번역 중",
        "status_done": "✅ 완료됨",
        "status_failed": "❌ 실패",
        "opt_card_title": "번역 매개변수 설정",
        "lbl_ai_service": "AI / 번역 서비스:",
        "btn_cfg_key": "🔑 키 설정",
        "tip_cfg_key": "이 서비스의 API 키 및 매개변수 설정 열기",
        "lbl_model": "사용 모델 (Model):",
        "model_default_none": "기본값 (모델 지정 불필요)",
        "lbl_trans_lang": "번역 언어:",
        "tip_swap_lang": "원본 언어와 대상 언어 바꾸기",
        "lbl_page_range": "페이지 범위:",
        "pages_all": "전체 페이지 (All)",
        "pages_first": "첫 페이지만 (Page 1)",
        "pages_first5": "처음 5페이지 (1-5)",
        "pages_custom": "사용자 지정 범위",
        "pages_custom_ph": "예: 1-3, 5, 8-10",
        "lbl_engine_mode": "조판 엔진:",
        "mode_fast_short": "fast (표준 AI 레이아웃 분석)",
        "mode_ultrafast_short": "ultrafast (초고속 네이티브 스트림)",
        "mode_babeldoc_short": "babeldoc (BabelDOC 백엔드)",
        "mode_precise_short": "precise (Precise v2 정밀 모드)",
        "lbl_output_opt": "출력 옵션:",
        "chk_mono_short": "번역본만 (Mono)",
        "chk_dual_short": "이중언어 대조 (Dual)",
        "chk_ignore_cache_short": "캐시 무시",
        "btn_start": "🚀 번역 시작",
        "btn_stop": "⏹ 중지",
        "btn_log": "📋 로그",
        "btn_help_quick": "📖 사용 설명서",
        "prog_ready": "준비 완료 — PDF 문서를 추가한 후 '번역 시작'을 클릭하세요",
        "prog_stopping": "현재 번역 작업을 중지하는 중...",
        "prog_processing": "처리 중: {name}",
        "prog_all_done": "🎉 모든 대기열 작업이 완료되었습니다",
        "prog_error": "오류: {err}",
        "msg_no_files": "목록에 최소 하나 이상의 PDF 또는 Word 파일을 추가하세요.",
        "msg_unconfigured_title": "API 키 미설정",
        "msg_unconfigured_body": "선택한 '{svc}' 서비스의 API 키가 설정되지 않았습니다. 지금 설정 페이지로 이동하시겠습니까?",
        "msg_stop_first": "먼저 실행 중인 번역 작업을 중지하세요.",
        "msg_no_pdf_in_dir": "선택한 폴더에서 번역 가능한 PDF/Word 파일을 찾을 수 없습니다.",
        "dlg_add_url_title": "온라인 PDF URL 추가",
        "dlg_add_url_label": "http:// 또는 https://로 시작하는 온라인 PDF 주소를 입력하세요 (예: arXiv 논문 링크):",
        "pdf_orig": "원본",
        "pdf_mono": "번역본 (Mono)",
        "pdf_dual": "이중언어 (Dual)",
        "pdf_total_pages": "/ {count} 페이지",
        "pdf_open_ext": "외부 열기",
        "pdf_open_ext_tip": "시스템 기본 PDF 뷰어로 현재 문서 열기",
        "pdf_reveal": "폴더 열기",
        "pdf_reveal_tip": "파일 관리자에서 현재 파일 표시",
        "pdf_empty_hint": "왼쪽에서 PDF 파일을 선택하거나 드래그하면 원본과 번역본을 미리 볼 수 있습니다",
        "pdf_err_load": "문서를 미리 볼 수 없습니다: {err}",
        "status_free": "무료/설정 불필요",
        "status_ready": "준비됨",
        "status_need_key": "키 필요",
        "status_configured": "설정됨",
        "ai_list_title": "AI 및 번역 제공업체",
        "ai_search_ph": "🔍 서비스 검색 (예: DeepSeek, OpenAI, Gemini...)",
        "ai_btn_doc": "🔗 API 키 발급 / 공식 콘솔",
        "ai_current_default": " (현재 기본값)",
        "ai_no_key_needed": "✅ 이 번역 서비스는 API 키 설정이 필요 없으며 바로 사용할 수 있습니다.",
        "ai_cli_hint": "💡 팁: 설정은 ~/.config/PDFMathTranslate/config.json 에 자동 저장되며 CLI(-s {name})와 공유됩니다.",
        "ai_btn_save": "💾 현재 서비스 설정 저장",
        "ai_btn_test": "⚡ 연결 테스트",
        "ai_btn_testing": "⏳ 테스트 중...",
        "ai_btn_set_default": "⭐ 기본 번역 서비스로 설정",
        "ai_btn_reset": "기본값 복원",
        "btn_show": "표시",
        "btn_hide": "숨김",
        "ai_msg_saved": "✅ '{svc}' 설정이 저장되었습니다.",
        "ai_msg_default_set": "⭐ '{svc}' 서비스를 기본값으로 설정하고 저장했습니다.",
        "ai_msg_reset": "'{svc}' 설정이 기본값으로 복원되었습니다.",
        "ai_msg_testing": "'{svc}' 연결 및 번역 테스트 중입니다. 잠시만 기다려 주세요...",
        "ts_card1_title": "기본 언어 및 번역 엔진 모드",
        "ts_card1_sub": "시작 시 기본 원본 언어, 대상 언어 및 레이아웃 분석 엔진을 설정합니다.",
        "ts_lbl_source": "기본 원본 언어 (Source):",
        "ts_lbl_target": "기본 대상 언어 (Target):",
        "ts_lbl_mode": "기본 엔진 모드 (Mode):",
        "ts_mode_fast": "fast — 표준 모드 (DocLayout-YOLO 레이아웃 분석, 권장)",
        "ts_mode_ultrafast": "ultrafast — 초고속 모드 (신경망 생략, 네이티브 텍스트 스트림 분석)",
        "ts_mode_babeldoc": "babeldoc — BabelDOC 향상된 조판 백엔드 (복잡한 레이아웃 지원)",
        "ts_mode_precise": "precise — Precise v2 정밀 모드 (pdf2zh_next 필요)",
        "ts_card2_title": "수식 보호 및 글꼴 조판 설정",
        "ts_card2_sub": "수학 수식 글꼴/문자 정규식 규칙과 출력 PDF 글꼴 서브셋 및 호환성을 제어합니다.",
        "ts_vfont_ph": "비워두면 기본 수식 글꼴 규칙 사용, 예: (CM[^R]|MS.M|XY|MT|BL|RM|EU|LA|RS).*",
        "ts_btn_vfont_preset": "LaTeX 수학 글꼴 정규식 채우기",
        "ts_vchar_ph": "수식으로 간주할 사용자 지정 문자 정규식 (-c / --vchar)",
        "ts_chk_skip_subset": "글꼴 서브셋 건너뛰기 (--skip-subset-fonts, 뷰어 호환성 향상)",
        "ts_chk_compatible": "입력 문서를 PDF/A 형식으로 변환 (--compatible)",
        "ts_lbl_vfont": "수식 글꼴 정규식 (vfont):",
        "ts_lbl_vchar": "수식 문자 정규식 (vchar):",
        "ts_card3_title": "AI 모델 사용자 지정 프롬프트 (Custom Prompt)",
        "ts_card3_sub": "LLM용 번역 지침을 사용자 지정합니다. 지원 변수: ${lang_in}, ${lang_out}, ${text}.",
        "ts_chk_use_prompt": "사용자 지정 LLM 프롬프트 템플릿 활성화",
        "ts_btn_default_prompt": "기본 학술 번역 템플릿 채우기",
        "ts_btn_import_prompt": "파일에서 프롬프트 가져오기 (.txt/.md)",
        "ts_card4_title": "OCR 스캔 문서 인식 설정",
        "ts_card4_sub": "이미지 전용 스캔 페이지가 감지되면 PyMuPDF + Tesseract로 OCR을 수행합니다.",
        "ts_ocr_lang_ph": "비워두면 원본 언어에 따라 자동 매칭 (예: eng, kor, chi_sim)",
        "ts_tess_ph": "비워두면 ~/.cache/pdf2zh/tessdata 또는 TESSDATA_PREFIX 사용",
        "ts_btn_browse_dir": "폴더 선택...",
        "ts_lbl_ocr_lang": "OCR 언어 코드:",
        "ts_lbl_tess_dir": "TESSDATA 폴더:",
        "ts_btn_save": "💾 번역 및 조판 설정 저장",
        "ts_msg_saved": "✅ 번역 및 조판 설정이 저장되었습니다",
        "os_card1_title": "출력 폴더 설정",
        "os_card1_sub": "번역된 PDF 파일이 저장될 위치를 설정합니다.",
        "os_chk_save_next": "원본 PDF 파일과 동일한 폴더에 저장 (권장)",
        "os_lbl_fixed_dir": "고정 출력 폴더:",
        "os_dir_ph": "사용자 지정 출력 폴더 선택, 예: ~/Downloads/PDF_Translated",
        "os_btn_browse": "폴더 찾아보기...",
        "os_btn_open_dir": "폴더 열기",
        "os_card2_title": "출력 문서 유형",
        "os_card2_sub": "번역본(Mono)과 이중언어 대조본(Dual) 생성 여부를 선택합니다.",
        "os_chk_mono": "번역본 PDF 생성 (파일명 접미사 -mono.pdf)",
        "os_chk_dual": "이중언어 대조 PDF 생성 (파일명 접미사 -dual.pdf)",
        "os_card3_title": "동시성 스레드 및 자동화",
        "os_card3_sub": "번역 요청 동시 스레드 수를 제어합니다 (API 속도 제한에 주의하세요).",
        "os_lbl_threads": "기본 동시 스레드 수 (-t):",
        "os_chk_auto_preview": "번역 완료 후 오른쪽 내장 뷰어에서 자동으로 결과 미리보기",
        "os_chk_auto_open_dir": "모든 대기열 완료 후 자동으로 출력 폴더 열기",
        "os_btn_save": "💾 출력 및 작업 설정 저장",
        "os_msg_saved": "✅ 출력 및 작업 설정이 저장되었습니다",
        "ss_card1_title": "네트워크 프록시 설정 (HTTP / HTTPS Proxy)",
        "ss_card1_sub": "Google, OpenAI, Gemini 또는 HuggingFace 모델 다운로드 시 로컬 프록시를 설정합니다.",
        "ss_chk_proxy": "사용자 지정 네트워크 프록시 활성화 (HTTP_PROXY 및 HTTPS_PROXY)",
        "ss_lbl_proxy_url": "프록시 주소:",
        "ss_proxy_ph": "예: http://127.0.0.1:7890 또는 socks5://127.0.0.1:1080",
        "ss_card2_title": "번역 캐시 관리 (SQLite Cache)",
        "ss_card2_sub": "이미 번역된 문단을 자동으로 캐시하여 중복 API 토큰 소비를 방지합니다.",
        "ss_chk_ignore_cache": "번역 캐시 무시 (--ignore-cache, 매번 새로 번역 요청)",
        "ss_btn_refresh_cache": "🔄 캐시 통계 새로고침",
        "ss_btn_clear_cache": "🧹 번역 캐시 비우기",
        "ss_btn_reveal_cache": "캐시 파일 보기",
        "ss_card3_title": "ONNX 레이아웃 모델 및 하드웨어 가속",
        "ss_card3_sub": "DocLayout-YOLO 모델의 추론 백엔드 및 사용자 지정 모델 경로를 설정합니다.",
        "ss_lbl_onnx_backend": "ONNX 백엔드:",
        "ss_lbl_onnx_path": "사용자 지정 ONNX 모델:",
        "ss_onnx_ph": "비워두면 내장 DocLayout-YOLO ONNX 모델 사용",
        "ss_btn_browse_onnx": ".onnx 파일 선택...",
        "ss_card4_title": "설정 파일 관리 및 백업",
        "ss_btn_open_cfg": "📂 설정 파일 보기",
        "ss_btn_export_cfg": "📤 설정 백업 내보내기 (.json)",
        "ss_btn_import_cfg": "📥 설정 파일 가져오기 (.json)",
        "ss_btn_reset_all": "⚠️ 모든 설정 초기화",
        "ss_btn_save": "💾 시스템 및 고급 설정 저장",
        "ss_msg_saved": "✅ 시스템 및 고급 설정이 저장되었습니다",
        "help_title": "📖 PDFMathTranslate 데스크톱 사용 설명서",
        "help_subtitle": "수식, 표, 목차 및 코드 레이아웃을 완벽히 보존하는 AI 학술 PDF 번역 도구",
        "help_btn_go_workspace": "🚀 번역 작업 공간으로 이동",
        "help_btn_go_keys": "🔑 AI 키 설정하기",
        "help_btn_github": "🌐 GitHub 저장소 방문",
    },
    "fr": {
        "window_title": "PDFMathTranslate Desktop v{version} — Traducteur PDF Académique Bilingue IA",
        "nav_workspace": "📄  Espace de travail",
        "nav_ai_keys": "🔑  Clés API & Services IA",
        "nav_trans_settings": "⚙️  Traduction & Mise en page",
        "nav_output_settings": "📁  Sortie & File d'attente",
        "nav_system_settings": "🛠️  Système & Avancé",
        "nav_user_guide": "📖  Guide d'utilisation",
        "ui_lang_label": "🌐 Langue UI:",
        "sb_default_service": "Service par défaut : {svc}",
        "sb_default_mode": "Moteur : {mode} | Threads : {threads}",
        "sb_proxy_on": "Proxy : Activé",
        "sb_proxy_off": "Proxy : Désactivé",
        "status_config_path": "Fichier de configuration : {path}",
        "menu_file": "Fichier",
        "menu_add_files": "Ajouter des fichiers PDF/Word...",
        "menu_add_folder": "Ajouter un dossier...",
        "menu_settings": "Clés API & Paramètres...",
        "menu_help": "Aide",
        "menu_open_guide": "Ouvrir le guide d'utilisation...",
        "drop_hint": "📄 Glissez-déposez des fichiers PDF / Word ou des dossiers ici",
        "btn_add_file": "＋ Fichier",
        "btn_add_folder": "＋ Dossier",
        "btn_add_url": "＋ URL",
        "btn_clear": "Effacer",
        "col_filename": "Document",
        "col_status": "Statut",
        "col_progress": "Progression",
        "col_time": "Temps",
        "status_pending": "En attente",
        "status_running": "⏳ En cours",
        "status_done": "✅ Terminé",
        "status_failed": "❌ Échec",
        "opt_card_title": "Options de traduction",
        "lbl_ai_service": "Service IA / Traduction :",
        "btn_cfg_key": "🔑 Clé API",
        "tip_cfg_key": "Configurer la clé API et les paramètres de ce fournisseur",
        "lbl_model": "Modèle (Model) :",
        "model_default_none": "Par défaut (aucun modèle requis)",
        "lbl_trans_lang": "Langues :",
        "tip_swap_lang": "Inverser la langue source et la langue cible",
        "lbl_page_range": "Pages :",
        "pages_all": "Toutes les pages (All)",
        "pages_first": "Page 1 uniquement",
        "pages_first5": "5 premières pages (1-5)",
        "pages_custom": "Plage personnalisée",
        "pages_custom_ph": "ex. 1-3, 5, 8-10",
        "lbl_engine_mode": "Moteur :",
        "mode_fast_short": "fast (Analyse IA standard)",
        "mode_ultrafast_short": "ultrafast (Flux natif ultra-rapide)",
        "mode_babeldoc_short": "babeldoc (Moteur BabelDOC)",
        "mode_precise_short": "precise (Mode Precise v2)",
        "lbl_output_opt": "Sortie :",
        "chk_mono_short": "Traduit (Mono)",
        "chk_dual_short": "Bilingue (Dual)",
        "chk_ignore_cache_short": "Sans cache",
        "btn_start": "🚀 Traduire",
        "btn_stop": "⏹ Arrêter",
        "btn_log": "📋 Journal",
        "btn_help_quick": "📖 Guide",
        "prog_ready": "Prêt — Ajoutez des fichiers PDF puis cliquez sur « Traduire »",
        "prog_stopping": "Arrêt de la tâche en cours...",
        "prog_processing": "Traitement : {name}",
        "prog_all_done": "🎉 Toutes les tâches sont terminées",
        "prog_error": "Erreur : {err}",
        "msg_no_files": "Veuillez d'abord ajouter au moins un fichier PDF ou Word.",
        "msg_unconfigured_title": "Clé API manquante",
        "msg_unconfigured_body": "Le service « {svc} » n'a pas encore de clé API configurée. Ouvrir les paramètres maintenant ?",
        "msg_stop_first": "Veuillez d'abord arrêter la traduction en cours.",
        "msg_no_pdf_in_dir": "Aucun fichier PDF/Word trouvé dans le dossier sélectionné.",
        "dlg_add_url_title": "Ajouter une URL PDF en ligne",
        "dlg_add_url_label": "Entrez une URL PDF commençant par http:// ou https:// (ex. arXiv) :",
        "pdf_orig": "Original",
        "pdf_mono": "Traduit (Mono)",
        "pdf_dual": "Bilingue (Dual)",
        "pdf_total_pages": "/ {count} pages",
        "pdf_open_ext": "Ouvrir en externe",
        "pdf_open_ext_tip": "Ouvrir avec le lecteur PDF par défaut du système",
        "pdf_reveal": "Afficher le dossier",
        "pdf_reveal_tip": "Afficher le fichier dans le gestionnaire de fichiers",
        "pdf_empty_hint": "Sélectionnez ou déposez un fichier PDF à gauche pour prévisualiser l'original et la traduction",
        "pdf_err_load": "Impossible de prévisualiser le PDF : {err}",
        "status_free": "Gratuit",
        "status_ready": "Prêt",
        "status_need_key": "Clé requise",
        "status_configured": "Configuré",
        "ai_list_title": "Fournisseurs IA & Traduction",
        "ai_search_ph": "🔍 Rechercher un service (DeepSeek, OpenAI, Gemini...)",
        "ai_btn_doc": "🔗 Obtenir une clé API / Console",
        "ai_current_default": " (Par défaut)",
        "ai_no_key_needed": "✅ Ce service ne nécessite aucune clé API et peut être utilisé immédiatement.",
        "ai_cli_hint": "💡 Astuce : Enregistré dans ~/.config/PDFMathTranslate/config.json et partagé avec le CLI (-s {name}).",
        "ai_btn_save": "💾 Enregistrer la configuration",
        "ai_btn_test": "⚡ Tester la connexion",
        "ai_btn_testing": "⏳ Test en cours...",
        "ai_btn_set_default": "⭐ Définir par défaut",
        "ai_btn_reset": "Réinitialiser",
        "btn_show": "Voir",
        "btn_hide": "Masquer",
        "ai_msg_saved": "✅ Configuration enregistrée pour « {svc} ».",
        "ai_msg_default_set": "⭐ « {svc} » défini comme service par défaut.",
        "ai_msg_reset": "Paramètres par défaut restaurés pour « {svc} ».",
        "ai_msg_testing": "Test de connexion à « {svc} » en cours...",
        "ts_card1_title": "Langues par défaut & Mode du moteur",
        "ts_card1_sub": "Configurez la langue source, la langue cible et le moteur d'analyse de mise en page par défaut.",
        "ts_lbl_source": "Langue source par défaut :",
        "ts_lbl_target": "Langue cible par défaut :",
        "ts_lbl_mode": "Mode du moteur :",
        "ts_mode_fast": "fast — Mode standard (Analyse DocLayout-YOLO, recommandé)",
        "ts_mode_ultrafast": "ultrafast — Mode ultra-rapide (Flux de texte PDF natif)",
        "ts_mode_babeldoc": "babeldoc — Moteur de mise en page BabelDOC",
        "ts_mode_precise": "precise — Mode Precise v2 (nécessite pdf2zh_next)",
        "ts_card2_title": "Préservation des formules & Polices",
        "ts_card2_sub": "Contrôlez les expressions régulières des formules mathématiques et l'incorporation des polices PDF.",
        "ts_vfont_ph": "Laisser vide pour la règle intégrée, ex. (CM[^R]|MS.M|XY|MT|BL|RM|EU|LA|RS).*",
        "ts_btn_vfont_preset": "Remplir Regex LaTeX",
        "ts_vchar_ph": "Regex de caractères de formule personnalisée (-c / --vchar)",
        "ts_chk_skip_subset": "Ignorer le sous-ensemble de polices (--skip-subset-fonts)",
        "ts_chk_compatible": "Convertir l'entrée au format PDF/A (--compatible)",
        "ts_lbl_vfont": "Regex police (vfont) :",
        "ts_lbl_vchar": "Regex caractère (vchar) :",
        "ts_card3_title": "Prompt LLM personnalisé (Custom Prompt)",
        "ts_card3_sub": "Personnalisez les instructions pour les LLM. Variables : ${lang_in}, ${lang_out}, ${text}.",
        "ts_chk_use_prompt": "Activer le modèle de prompt LLM personnalisé",
        "ts_btn_default_prompt": "Charger le modèle académique par défaut",
        "ts_btn_import_prompt": "Importer un prompt (.txt/.md)",
        "ts_card4_title": "Paramètres OCR (Documents scannés)",
        "ts_card4_sub": "Détecte automatiquement les pages scannées via PyMuPDF + Tesseract.",
        "ts_ocr_lang_ph": "Laisser vide pour correspondance auto (ex. eng, fra, chi_sim)",
        "ts_tess_ph": "Laisser vide pour ~/.cache/pdf2zh/tessdata ou TESSDATA_PREFIX",
        "ts_btn_browse_dir": "Parcourir...",
        "ts_lbl_ocr_lang": "Langue OCR :",
        "ts_lbl_tess_dir": "Dossier TESSDATA :",
        "ts_btn_save": "💾 Enregistrer les paramètres de traduction",
        "ts_msg_saved": "✅ Paramètres de traduction enregistrés",
        "os_card1_title": "Dossier de sortie",
        "os_card1_sub": "Choisissez où enregistrer les fichiers PDF traduits.",
        "os_chk_save_next": "Enregistrer dans le même dossier que le fichier PDF source (Recommandé)",
        "os_lbl_fixed_dir": "Dossier fixe :",
        "os_dir_ph": "Dossier de sortie personnalisé, ex. ~/Downloads/PDF_Translated",
        "os_btn_browse": "Parcourir...",
        "os_btn_open_dir": "Ouvrir le dossier",
        "os_card2_title": "Variantes de fichiers générés",
        "os_card2_sub": "Générer la version traduite seule (Mono), la version bilingue côte à côte (Dual), ou les deux.",
        "os_chk_mono": "Générer le PDF traduit uniquement (suffixe -mono.pdf)",
        "os_chk_dual": "Générer le PDF bilingue côte à côte (suffixe -dual.pdf)",
        "os_card3_title": "Threads simultanés & Automatisation",
        "os_card3_sub": "Contrôlez le nombre de threads de traduction simultanés.",
        "os_lbl_threads": "Threads simultanés par défaut (-t) :",
        "os_chk_auto_preview": "Prévisualiser automatiquement le PDF généré une fois terminé",
        "os_chk_auto_open_dir": "Ouvrir automatiquement le dossier de sortie à la fin de la file",
        "os_btn_save": "💾 Enregistrer les paramètres de sortie",
        "os_msg_saved": "✅ Paramètres de sortie enregistrés",
        "ss_card1_title": "Proxy Réseau (HTTP / HTTPS Proxy)",
        "ss_card1_sub": "Configurez un proxy local pour accéder à OpenAI, Gemini, Google ou HuggingFace.",
        "ss_chk_proxy": "Activer le proxy réseau personnalisé (HTTP_PROXY & HTTPS_PROXY)",
        "ss_lbl_proxy_url": "URL du proxy :",
        "ss_proxy_ph": "ex. http://127.0.0.1:7890 ou socks5://127.0.0.1:1080",
        "ss_card2_title": "Cache de traduction (SQLite Cache)",
        "ss_card2_sub": "Met en cache les paragraphes déjà traduits pour économiser les tokens API.",
        "ss_chk_ignore_cache": "Ignorer le cache de traduction (--ignore-cache)",
        "ss_btn_refresh_cache": "🔄 Actualiser les statistiques",
        "ss_btn_clear_cache": "🧹 Vider le cache de traduction",
        "ss_btn_reveal_cache": "Afficher le fichier cache",
        "ss_card3_title": "Modèle ONNX & Accélération matérielle",
        "ss_card3_sub": "Configurez le moteur d'inférence ONNX pour DocLayout-YOLO.",
        "ss_lbl_onnx_backend": "Backend ONNX :",
        "ss_lbl_onnx_path": "Modèle ONNX personnalisé :",
        "ss_onnx_ph": "Laisser vide pour utiliser le modèle DocLayout-YOLO intégré",
        "ss_btn_browse_onnx": "Sélectionner .onnx...",
        "ss_card4_title": "Gestion & Sauvegarde de la configuration",
        "ss_btn_open_cfg": "📂 Afficher config.json",
        "ss_btn_export_cfg": "📤 Exporter la configuration (.json)",
        "ss_btn_import_cfg": "📥 Importer une configuration (.json)",
        "ss_btn_reset_all": "⚠️ Réinitialiser tous les paramètres",
        "ss_btn_save": "💾 Enregistrer les paramètres système",
        "ss_msg_saved": "✅ Paramètres système enregistrés",
        "help_title": "📖 Guide d'utilisation PDFMathTranslate Desktop",
        "help_subtitle": "Traduction PDF académique par IA préservant formules, figures, sommaires et code",
        "help_btn_go_workspace": "🚀 Aller à l'espace de travail",
        "help_btn_go_keys": "🔑 Configurer les clés IA",
        "help_btn_github": "🌐 Ouvrir le dépôt GitHub",
    },
    "de": {
        "window_title": "PDFMathTranslate Desktop v{version} — KI-gestützter zweisprachiger PDF-Übersetzer",
        "nav_workspace": "📄  Arbeitsbereich",
        "nav_ai_keys": "🔑  KI-Schlüssel & Anbieter",
        "nav_trans_settings": "⚙️  Übersetzung & Layout",
        "nav_output_settings": "📁  Ausgabe & Aufgaben",
        "nav_system_settings": "🛠️  System & Erweitert",
        "nav_user_guide": "📖  Benutzerhandbuch",
        "ui_lang_label": "🌐 UI-Sprache:",
        "sb_default_service": "Standarddienst: {svc}",
        "sb_default_mode": "Engine: {mode} | Threads: {threads}",
        "sb_proxy_on": "Proxy: Aktiviert",
        "sb_proxy_off": "Proxy: Deaktiviert",
        "status_config_path": "Konfigurationsdatei: {path}",
        "menu_file": "Datei",
        "menu_add_files": "PDF/Word-Dateien hinzufügen...",
        "menu_add_folder": "Ordner hinzufügen...",
        "menu_settings": "KI-Schlüssel & Einstellungen...",
        "menu_help": "Hilfe",
        "menu_open_guide": "Benutzerhandbuch öffnen...",
        "drop_hint": "📄 PDF- / Word-Dateien oder Ordner hierher ziehen",
        "btn_add_file": "＋ Datei",
        "btn_add_folder": "＋ Ordner",
        "btn_add_url": "＋ URL",
        "btn_clear": "Leeren",
        "col_filename": "Dokument",
        "col_status": "Status",
        "col_progress": "Fortschritt",
        "col_time": "Dauer",
        "status_pending": "Ausstehend",
        "status_running": "⏳ Läuft",
        "status_done": "✅ Fertig",
        "status_failed": "❌ Fehler",
        "opt_card_title": "Übersetzungsoptionen",
        "lbl_ai_service": "KI / Übersetzungsdienst:",
        "btn_cfg_key": "🔑 API-Key",
        "tip_cfg_key": "API-Schlüssel und Einstellungen für diesen Anbieter öffnen",
        "lbl_model": "Modell (Model):",
        "model_default_none": "Standard (kein Modell erforderlich)",
        "lbl_trans_lang": "Sprachen:",
        "tip_swap_lang": "Quell- und Zielsprache tauschen",
        "lbl_page_range": "Seiten:",
        "pages_all": "Alle Seiten (All)",
        "pages_first": "Nur Seite 1",
        "pages_first5": "Erste 5 Seiten (1-5)",
        "pages_custom": "Benutzerdefiniert",
        "pages_custom_ph": "z.B. 1-3, 5, 8-10",
        "lbl_engine_mode": "Engine:",
        "mode_fast_short": "fast (Standard-KI-Layoutanalyse)",
        "mode_ultrafast_short": "ultrafast (Ultraschneller Textstrom)",
        "mode_babeldoc_short": "babeldoc (BabelDOC-Backend)",
        "mode_precise_short": "precise (Precise v2 Modus)",
        "lbl_output_opt": "Ausgabe:",
        "chk_mono_short": "Nur Übersetzung (Mono)",
        "chk_dual_short": "Zweisprachig (Dual)",
        "chk_ignore_cache_short": "Ohne Cache",
        "btn_start": "🚀 Übersetzen",
        "btn_stop": "⏹ Stopp",
        "btn_log": "📋 Protokoll",
        "btn_help_quick": "📖 Anleitung",
        "prog_ready": "Bereit — PDF-Dateien hinzufügen und auf „Übersetzen“ klicken",
        "prog_stopping": "Aktuelle Aufgabe wird gestoppt...",
        "prog_processing": "Verarbeite: {name}",
        "prog_all_done": "🎉 Alle Aufgaben abgeschlossen",
        "prog_error": "Fehler: {err}",
        "msg_no_files": "Bitte fügen Sie zuerst mindestens eine PDF- oder Word-Datei hinzu.",
        "msg_unconfigured_title": "API-Schlüssel fehlt",
        "msg_unconfigured_body": "Für „{svc}“ ist noch kein API-Schlüssel konfiguriert. Jetzt konfigurieren?",
        "msg_stop_first": "Bitte stoppen Sie zuerst die laufende Übersetzung.",
        "msg_no_pdf_in_dir": "Keine übersetzbaren PDF/Word-Dateien im ausgewählten Ordner gefunden.",
        "dlg_add_url_title": "Online-PDF-URL hinzufügen",
        "dlg_add_url_label": "Geben Sie eine PDF-URL mit http:// oder https:// ein (z.B. arXiv):",
        "pdf_orig": "Original",
        "pdf_mono": "Übersetzt (Mono)",
        "pdf_dual": "Zweisprachig (Dual)",
        "pdf_total_pages": "/ {count} Seiten",
        "pdf_open_ext": "Extern öffnen",
        "pdf_open_ext_tip": "Mit dem Standard-PDF-Reader des Systems öffnen",
        "pdf_reveal": "Ordner zeigen",
        "pdf_reveal_tip": "Datei im Dateimanager anzeigen",
        "pdf_empty_hint": "Wählen Sie links eine PDF-Datei aus, um Original und Übersetzung anzuzeigen",
        "pdf_err_load": "PDF-Vorschau fehlgeschlagen: {err}",
        "status_free": "Kostenlos",
        "status_ready": "Bereit",
        "status_need_key": "Key fehlt",
        "status_configured": "Konfiguriert",
        "ai_list_title": "KI- & Übersetzungsanbieter",
        "ai_search_ph": "🔍 Anbieter suchen (DeepSeek, OpenAI, Gemini...)",
        "ai_btn_doc": "🔗 API-Schlüssel abrufen / Konsole",
        "ai_current_default": " (Standard)",
        "ai_no_key_needed": "✅ Dieser Dienst benötigt keinen API-Schlüssel und ist sofort einsatzbereit.",
        "ai_cli_hint": "💡 Hinweis: Wird in ~/.config/PDFMathTranslate/config.json gespeichert (CLI: -s {name}).",
        "ai_btn_save": "💾 Anbieterkonfiguration speichern",
        "ai_btn_test": "⚡ Verbindung testen",
        "ai_btn_testing": "⏳ Teste...",
        "ai_btn_set_default": "⭐ Als Standard festlegen",
        "ai_btn_reset": "Zurücksetzen",
        "btn_show": "Zeigen",
        "btn_hide": "Verbergen",
        "ai_msg_saved": "✅ Einstellungen für „{svc}“ gespeichert.",
        "ai_msg_default_set": "⭐ „{svc}“ als Standarddienst festgelegt.",
        "ai_msg_reset": "„{svc}“ auf Standardwerte zurückgesetzt.",
        "ai_msg_testing": "Verbindung zu „{svc}“ wird getestet...",
        "ts_card1_title": "Standardsprachen & Engine-Modus",
        "ts_card1_sub": "Konfigurieren Sie Standard-Quellsprache, Zielsprache und Layout-Engine.",
        "ts_lbl_source": "Standard-Quellsprache:",
        "ts_lbl_target": "Standard-Zielsprache:",
        "ts_lbl_mode": "Standard-Engine-Modus:",
        "ts_mode_fast": "fast — Standardmodus (DocLayout-YOLO Layoutanalyse, empfohlen)",
        "ts_mode_ultrafast": "ultrafast — Ultraschneller Modus (Nativer PDF-Textstrom)",
        "ts_mode_babeldoc": "babeldoc — BabelDOC Layout-Backend",
        "ts_mode_precise": "precise — Precise v2 Modus (erfordert pdf2zh_next)",
        "ts_card2_title": "Formelschutz & Schriftarten-Einstellungen",
        "ts_card2_sub": "Steuern Sie reguläre Ausdrücke für mathematische Formeln und PDF-Schrifteinbettung.",
        "ts_vfont_ph": "Leer lassen für Standardregel, z.B. (CM[^R]|MS.M|XY|MT|BL|RM|EU|LA|RS).*",
        "ts_btn_vfont_preset": "LaTeX-Mathe-Regex einfügen",
        "ts_vchar_ph": "Benutzerdefinierte Formelzeichen-Regex (-c / --vchar)",
        "ts_chk_skip_subset": "Schriftarten-Subsetting überspringen (--skip-subset-fonts)",
        "ts_chk_compatible": "Eingabedokument in PDF/A konvertieren (--compatible)",
        "ts_lbl_vfont": "Formelschrift-Regex (vfont):",
        "ts_lbl_vchar": "Formelzeichen-Regex (vchar):",
        "ts_card3_title": "Benutzerdefinierter LLM-Prompt (Custom Prompt)",
        "ts_card3_sub": "Passen Sie die Übersetzungsanweisungen für LLMs an. Variablen: ${lang_in}, ${lang_out}, ${text}.",
        "ts_chk_use_prompt": "Benutzerdefinierte LLM-Prompt-Vorlage aktivieren",
        "ts_btn_default_prompt": "Standard-Vorlage einfügen",
        "ts_btn_import_prompt": "Prompt aus Datei importieren (.txt/.md)",
        "ts_card4_title": "OCR-Einstellungen (Gescannte PDFs)",
        "ts_card4_sub": "Erkennt automatisch gescannte Bildseiten über PyMuPDF + Tesseract.",
        "ts_ocr_lang_ph": "Leer lassen für automatische Erkennung (z.B. eng, deu, chi_sim)",
        "ts_tess_ph": "Leer lassen für ~/.cache/pdf2zh/tessdata oder TESSDATA_PREFIX",
        "ts_btn_browse_dir": "Durchsuchen...",
        "ts_lbl_ocr_lang": "OCR-Sprache:",
        "ts_lbl_tess_dir": "TESSDATA-Ordner:",
        "ts_btn_save": "💾 Übersetzungseinstellungen speichern",
        "ts_msg_saved": "✅ Übersetzungseinstellungen gespeichert",
        "os_card1_title": "Ausgabeordner",
        "os_card1_sub": "Legen Sie fest, wo übersetzte PDF-Dateien gespeichert werden.",
        "os_chk_save_next": "Im selben Ordner wie die Quell-PDF speichern (Empfohlen)",
        "os_lbl_fixed_dir": "Fester Ausgabeordner:",
        "os_dir_ph": "Benutzerdefinierter Ordner, z.B. ~/Downloads/PDF_Translated",
        "os_btn_browse": "Durchsuchen...",
        "os_btn_open_dir": "Ordner öffnen",
        "os_card2_title": "Ausgabedokumenttypen",
        "os_card2_sub": "Wählen Sie, ob Mono-PDF, Dual-PDF oder beide erstellt werden sollen.",
        "os_chk_mono": "Übersetztes PDF erstellen (Suffix -mono.pdf)",
        "os_chk_dual": "Zweisprachiges PDF erstellen (Suffix -dual.pdf)",
        "os_card3_title": "Parallele Threads & Automatisierung",
        "os_card3_sub": "Steuern Sie die Anzahl gleichzeitiger Übersetzungsanfragen.",
        "os_lbl_threads": "Standard-Threads (-t):",
        "os_chk_auto_preview": "Nach Abschluss automatisch im integrierten PDF-Viewer anzeigen",
        "os_chk_auto_open_dir": "Ausgabeordner nach Abschluss aller Aufgaben öffnen",
        "os_btn_save": "💾 Ausgabeeinstellungen speichern",
        "os_msg_saved": "✅ Ausgabeeinstellungen gespeichert",
        "ss_card1_title": "Netzwerk-Proxy (HTTP / HTTPS Proxy)",
        "ss_card1_sub": "Lokalen Proxy für OpenAI, Gemini, Google oder HuggingFace konfigurieren.",
        "ss_chk_proxy": "Benutzerdefinierten Netzwerk-Proxy aktivieren (HTTP_PROXY & HTTPS_PROXY)",
        "ss_lbl_proxy_url": "Proxy-URL:",
        "ss_proxy_ph": "z.B. http://127.0.0.1:7890 oder socks5://127.0.0.1:1080",
        "ss_card2_title": "Übersetzungs-Cache (SQLite Cache)",
        "ss_card2_sub": "Speichert bereits übersetzte Absätze, um API-Tokens zu sparen.",
        "ss_chk_ignore_cache": "Übersetzungs-Cache ignorieren (--ignore-cache)",
        "ss_btn_refresh_cache": "🔄 Cache-Statistik aktualisieren",
        "ss_btn_clear_cache": "🧹 Cache leeren",
        "ss_btn_reveal_cache": "Cache-Datei zeigen",
        "ss_card3_title": "ONNX-Layoutmodell & Hardwarebeschleunigung",
        "ss_card3_sub": "Konfigurieren Sie das ONNX-Inferenz-Backend für DocLayout-YOLO.",
        "ss_lbl_onnx_backend": "ONNX-Backend:",
        "ss_lbl_onnx_path": "Benutzerdefiniertes ONNX-Modell:",
        "ss_onnx_ph": "Leer lassen für integriertes DocLayout-YOLO-Modell",
        "ss_btn_browse_onnx": ".onnx auswählen...",
        "ss_card4_title": "Konfigurationsverwaltung & Backup",
        "ss_btn_open_cfg": "📂 config.json zeigen",
        "ss_btn_export_cfg": "📤 Konfiguration exportieren (.json)",
        "ss_btn_import_cfg": "📥 Konfiguration importieren (.json)",
        "ss_btn_reset_all": "⚠️ Alle Einstellungen zurücksetzen",
        "ss_btn_save": "💾 Systemeinstellungen speichern",
        "ss_msg_saved": "✅ Systemeinstellungen gespeichert",
        "help_title": "📖 PDFMathTranslate Desktop Benutzerhandbuch",
        "help_subtitle": "KI-gestützte wissenschaftliche PDF-Übersetzung unter Beibehaltung von Formeln, Inhaltsverzeichnis & Code",
        "help_btn_go_workspace": "🚀 Zum Arbeitsbereich",
        "help_btn_go_keys": "🔑 KI-Schlüssel konfigurieren",
        "help_btn_github": "🌐 GitHub-Repository öffnen",
    },
    "ru": {
        "window_title": "PDFMathTranslate Desktop v{version} — ИИ-переводчик научных PDF",
        "nav_workspace": "📄  Рабочая область",
        "nav_ai_keys": "🔑  API-ключи и сервисы",
        "nav_trans_settings": "⚙️  Перевод и вёрстка",
        "nav_output_settings": "📁  Вывод и очередь",
        "nav_system_settings": "🛠️  Система и прокси",
        "nav_user_guide": "📖  Руководство пользователя",
        "ui_lang_label": "🌐 Язык интерфейса:",
        "sb_default_service": "Сервис: {svc}",
        "sb_default_mode": "Движок: {mode} | Потоки: {threads}",
        "sb_proxy_on": "Прокси: Вкл.",
        "sb_proxy_off": "Прокси: Выкл.",
        "status_config_path": "Файл конфигурации: {path}",
        "menu_file": "Файл",
        "menu_add_files": "Добавить файлы PDF/Word...",
        "menu_add_folder": "Добавить папку...",
        "menu_settings": "API-ключи и настройки...",
        "menu_help": "Справка",
        "menu_open_guide": "Открыть руководство...",
        "drop_hint": "📄 Перетащите файлы PDF / Word или папки сюда",
        "btn_add_file": "＋ Файл",
        "btn_add_folder": "＋ Папка",
        "btn_add_url": "＋ Ссылка",
        "btn_clear": "Очистить",
        "col_filename": "Документ",
        "col_status": "Статус",
        "col_progress": "Прогресс",
        "col_time": "Время",
        "status_pending": "В очереди",
        "status_running": "⏳ Перевод",
        "status_done": "✅ Готово",
        "status_failed": "❌ Ошибка",
        "opt_card_title": "Параметры перевода",
        "lbl_ai_service": "Сервис ИИ / перевода:",
        "btn_cfg_key": "🔑 Ключ API",
        "tip_cfg_key": "Открыть настройки API-ключа этого провайдера",
        "lbl_model": "Модель (Model):",
        "model_default_none": "По умолчанию (выбор модели не требуется)",
        "lbl_trans_lang": "Языки перевода:",
        "tip_swap_lang": "Поменять местами исходный и целевой языки",
        "lbl_page_range": "Страницы:",
        "pages_all": "Все страницы (All)",
        "pages_first": "Только 1-я страница",
        "pages_first5": "Первые 5 страниц (1-5)",
        "pages_custom": "Свой диапазон",
        "pages_custom_ph": "напр. 1-3, 5, 8-10",
        "lbl_engine_mode": "Движок вёрстки:",
        "mode_fast_short": "fast (Стандартный ИИ-анализ макета)",
        "mode_ultrafast_short": "ultrafast (Сверхбыстрый поток текста)",
        "mode_babeldoc_short": "babeldoc (Движок BabelDOC)",
        "mode_precise_short": "precise (Точный режим Precise v2)",
        "lbl_output_opt": "Файлы вывода:",
        "chk_mono_short": "Перевод (Mono)",
        "chk_dual_short": "Двуязычный (Dual)",
        "chk_ignore_cache_short": "Без кэша",
        "btn_start": "🚀 Начать перевод",
        "btn_stop": "⏹ Стоп",
        "btn_log": "📋 Журнал",
        "btn_help_quick": "📖 Справка",
        "prog_ready": "Готово — добавьте PDF-документы и нажмите «Начать перевод»",
        "prog_stopping": "Остановка текущей задачи...",
        "prog_processing": "Обработка: {name}",
        "prog_all_done": "🎉 Все задачи очереди выполнены",
        "prog_error": "Ошибка: {err}",
        "msg_no_files": "Сначала добавьте хотя бы один файл PDF или Word.",
        "msg_unconfigured_title": "API-ключ не настроен",
        "msg_unconfigured_body": "Для сервиса «{svc}» не указан API-ключ. Перейти к настройкам сейчас?",
        "msg_stop_first": "Сначала остановите выполняющийся перевод.",
        "msg_no_pdf_in_dir": "В выбранной папке не найдено файлов PDF/Word.",
        "dlg_add_url_title": "Добавить ссылку на PDF",
        "dlg_add_url_label": "Введите URL PDF-документа, начинающийся с http:// или https:// (например, arXiv):",
        "pdf_orig": "Оригинал",
        "pdf_mono": "Перевод (Mono)",
        "pdf_dual": "Двуязычный (Dual)",
        "pdf_total_pages": "/ {count} стр.",
        "pdf_open_ext": "Открыть внешне",
        "pdf_open_ext_tip": "Открыть в системной программе просмотра PDF",
        "pdf_reveal": "Показать в папке",
        "pdf_reveal_tip": "Показать файл в файловом менеджере",
        "pdf_empty_hint": "Выберите или перетащите PDF-файл слева для предпросмотра оригинала и перевода",
        "pdf_err_load": "Не удалось загрузить предпросмотр PDF: {err}",
        "status_free": "Бесплатно",
        "status_ready": "Готов",
        "status_need_key": "Нужен ключ",
        "status_configured": "Настроен",
        "ai_list_title": "Провайдеры ИИ и перевода",
        "ai_search_ph": "🔍 Поиск провайдера (DeepSeek, OpenAI, Gemini...)",
        "ai_btn_doc": "🔗 Получить API-ключ / Консоль",
        "ai_current_default": " (По умолчанию)",
        "ai_no_key_needed": "✅ Этому сервису не требуется API-ключ, он готов к работе.",
        "ai_cli_hint": "💡 Конфигурация сохраняется в ~/.config/PDFMathTranslate/config.json (CLI: -s {name}).",
        "ai_btn_save": "💾 Сохранить настройки",
        "ai_btn_test": "⚡ Проверить соединение",
        "ai_btn_testing": "⏳ Проверка...",
        "ai_btn_set_default": "⭐ Сделать сервисом по умолчанию",
        "ai_btn_reset": "Сбросить",
        "btn_show": "Показать",
        "btn_hide": "Скрыть",
        "ai_msg_saved": "✅ Настройки «{svc}» сохранены.",
        "ai_msg_default_set": "⭐ «{svc}» установлен по умолчанию.",
        "ai_msg_reset": "Параметры «{svc}» сброшены по умолчанию.",
        "ai_msg_testing": "Проверка соединения с «{svc}»...",
        "ts_card1_title": "Языки по умолчанию и режим движка",
        "ts_card1_sub": "Настройте исходный язык, язык перевода и режим анализа макета по умолчанию.",
        "ts_lbl_source": "Исходный язык (Source):",
        "ts_lbl_target": "Язык перевода (Target):",
        "ts_lbl_mode": "Режим движка (Mode):",
        "ts_mode_fast": "fast — Стандартный режим (анализ макета DocLayout-YOLO, рекомендуется)",
        "ts_mode_ultrafast": "ultrafast — Сверхбыстрый режим (прямой поток текста PDF)",
        "ts_mode_babeldoc": "babeldoc — Расширенный бэкенд вёрстки BabelDOC",
        "ts_mode_precise": "precise — Точный режим Precise v2 (требуется pdf2zh_next)",
        "ts_card2_title": "Сохранение формул и настройки шрифтов",
        "ts_card2_sub": "Настройка регулярных выражений для математических формул и подмножеств шрифтов PDF.",
        "ts_vfont_ph": "Оставьте пустым для встроенных правил, напр. (CM[^R]|MS.M|XY|MT|BL|RM|EU|LA|RS).*",
        "ts_btn_vfont_preset": "Вставить шаблон шрифтов LaTeX",
        "ts_vchar_ph": "Регулярное выражение символов формул (-c / --vchar)",
        "ts_chk_skip_subset": "Отключить подмножество шрифтов (--skip-subset-fonts)",
        "ts_chk_compatible": "Конвертировать входной PDF в формат PDF/A (--compatible)",
        "ts_lbl_vfont": "Шрифты формул (vfont):",
        "ts_lbl_vchar": "Символы формул (vchar):",
        "ts_card3_title": "Пользовательский промпт для ИИ (Custom Prompt)",
        "ts_card3_sub": "Настройте инструкции перевода для LLM. Переменные: ${lang_in}, ${lang_out}, ${text}.",
        "ts_chk_use_prompt": "Включить пользовательский шаблон промпта LLM",
        "ts_btn_default_prompt": "Заполнить академический шаблон по умолчанию",
        "ts_btn_import_prompt": "Импорт промпта из файла (.txt/.md)",
        "ts_card4_title": "Настройки OCR (Сканированные PDF)",
        "ts_card4_sub": "Автоматическое распознавание сканированных страниц через PyMuPDF + Tesseract.",
        "ts_ocr_lang_ph": "Оставьте пустым для автовыбора (напр. eng, rus, chi_sim)",
        "ts_tess_ph": "Оставьте пустым для ~/.cache/pdf2zh/tessdata или TESSDATA_PREFIX",
        "ts_btn_browse_dir": "Обзор...",
        "ts_lbl_ocr_lang": "Язык OCR:",
        "ts_lbl_tess_dir": "Папка TESSDATA:",
        "ts_btn_save": "💾 Сохранить настройки перевода",
        "ts_msg_saved": "✅ Настройки перевода сохранены",
        "os_card1_title": "Папка сохранения",
        "os_card1_sub": "Укажите папку для сохранения переведённых PDF-файлов.",
        "os_chk_save_next": "Сохранять в папке исходного PDF-файла (рекомендуется)",
        "os_lbl_fixed_dir": "Фиксированная папка:",
        "os_dir_ph": "Выберите папку вывода, напр. ~/Downloads/PDF_Translated",
        "os_btn_browse": "Обзор...",
        "os_btn_open_dir": "Открыть папку",
        "os_card2_title": "Варианты выходных документов",
        "os_card2_sub": "Выберите создание только перевода (Mono), двуязычной версии (Dual) или обеих.",
        "os_chk_mono": "Создавать PDF только с переводом (суффикс -mono.pdf)",
        "os_chk_dual": "Создавать двуязычный PDF (суффикс -dual.pdf)",
        "os_card3_title": "Многопоточность и автоматизация",
        "os_card3_sub": "Управляйте количеством параллельных потоков запросов к API.",
        "os_lbl_threads": "Потоков по умолчанию (-t):",
        "os_chk_auto_preview": "Автоматически открывать результат во встроенном просмотрщике",
        "os_chk_auto_open_dir": "Открывать выходную папку после завершения всей очереди",
        "os_btn_save": "💾 Сохранить настройки вывода",
        "os_msg_saved": "✅ Настройки вывода сохранены",
        "ss_card1_title": "Сетевой прокси (HTTP / HTTPS Proxy)",
        "ss_card1_sub": "Локальный прокси для доступа к OpenAI, Gemini, Google или HuggingFace.",
        "ss_chk_proxy": "Включить сетевой прокси (HTTP_PROXY и HTTPS_PROXY)",
        "ss_lbl_proxy_url": "Адрес прокси:",
        "ss_proxy_ph": "напр. http://127.0.0.1:7890 или socks5://127.0.0.1:1080",
        "ss_card2_title": "Кэш переводов (SQLite Cache)",
        "ss_card2_sub": "Кэширует переведённые абзацы для экономии токенов ИИ.",
        "ss_chk_ignore_cache": "Игнорировать кэш переводов (--ignore-cache)",
        "ss_btn_refresh_cache": "🔄 Обновить статистику кэша",
        "ss_btn_clear_cache": "🧹 Очистить кэш переводов",
        "ss_btn_reveal_cache": "Показать файл кэша",
        "ss_card3_title": "Модель ONNX и аппаратное ускорение",
        "ss_card3_sub": "Настройка бэкенда вывода ONNX для модели DocLayout-YOLO.",
        "ss_lbl_onnx_backend": "Бэкенд ONNX:",
        "ss_lbl_onnx_path": "Своя модель ONNX:",
        "ss_onnx_ph": "Оставьте пустым для встроенной модели DocLayout-YOLO",
        "ss_btn_browse_onnx": "Выбрать .onnx...",
        "ss_card4_title": "Управление конфигурацией и резервное копирование",
        "ss_btn_open_cfg": "📂 Показать config.json",
        "ss_btn_export_cfg": "📤 Экспорт конфигурации (.json)",
        "ss_btn_import_cfg": "📥 Импорт конфигурации (.json)",
        "ss_btn_reset_all": "⚠️ Сбросить все настройки",
        "ss_btn_save": "💾 Сохранить системные настройки",
        "ss_msg_saved": "✅ Системные настройки сохранены",
        "help_title": "📖 Руководство пользователя PDFMathTranslate Desktop",
        "help_subtitle": "ИИ-перевод научных PDF с сохранением формул, таблиц, оглавления и программного кода",
        "help_btn_go_workspace": "🚀 Перейти к переводу",
        "help_btn_go_keys": "🔑 Настроить ключи ИИ",
        "help_btn_github": "🌐 Открыть GitHub",
    },
    "es": {
        "window_title": "PDFMathTranslate Desktop v{version} — Traductor PDF Académico Bilingüe con IA",
        "nav_workspace": "📄  Espacio de trabajo",
        "nav_ai_keys": "🔑  Claves API y Proveedores",
        "nav_trans_settings": "⚙️  Traducción y Diseño",
        "nav_output_settings": "📁  Salida y Tareas",
        "nav_system_settings": "🛠️  Sistema y Avanzado",
        "nav_user_guide": "📖  Guía de usuario",
        "ui_lang_label": "🌐 Idioma UI:",
        "sb_default_service": "Servicio predeterminado: {svc}",
        "sb_default_mode": "Motor: {mode} | Hilos: {threads}",
        "sb_proxy_on": "Proxy: Activado",
        "sb_proxy_off": "Proxy: Desactivado",
        "status_config_path": "Archivo de configuración: {path}",
        "menu_file": "Archivo",
        "menu_add_files": "Añadir archivos PDF/Word...",
        "menu_add_folder": "Añadir carpeta...",
        "menu_settings": "Claves API y Ajustes...",
        "menu_help": "Ayuda",
        "menu_open_guide": "Abrir guía de usuario...",
        "drop_hint": "📄 Arrastre archivos PDF / Word o carpetas aquí",
        "btn_add_file": "＋ Archivo",
        "btn_add_folder": "＋ Carpeta",
        "btn_add_url": "＋ URL",
        "btn_clear": "Limpiar",
        "col_filename": "Documento",
        "col_status": "Estado",
        "col_progress": "Progreso",
        "col_time": "Tiempo",
        "status_pending": "Pendiente",
        "status_running": "⏳ Traduciendo",
        "status_done": "✅ Completado",
        "status_failed": "❌ Error",
        "opt_card_title": "Opciones de traducción",
        "lbl_ai_service": "Servicio IA / Traducción:",
        "btn_cfg_key": "🔑 Clave API",
        "tip_cfg_key": "Configurar la clave API y ajustes de este proveedor",
        "lbl_model": "Modelo (Model):",
        "model_default_none": "Predeterminado (no requiere modelo)",
        "lbl_trans_lang": "Idiomas:",
        "tip_swap_lang": "Intercambiar idioma de origen y destino",
        "lbl_page_range": "Páginas:",
        "pages_all": "Todas las páginas (All)",
        "pages_first": "Solo página 1",
        "pages_first5": "Primeras 5 páginas (1-5)",
        "pages_custom": "Rango personalizado",
        "pages_custom_ph": "ej. 1-3, 5, 8-10",
        "lbl_engine_mode": "Motor:",
        "mode_fast_short": "fast (Análisis de diseño IA estándar)",
        "mode_ultrafast_short": "ultrafast (Flujo nativo ultrarrápido)",
        "mode_babeldoc_short": "babeldoc (Motor BabelDOC)",
        "mode_precise_short": "precise (Modo Precise v2)",
        "lbl_output_opt": "Salida:",
        "chk_mono_short": "Traducido (Mono)",
        "chk_dual_short": "Bilingüe (Dual)",
        "chk_ignore_cache_short": "Sin caché",
        "btn_start": "🚀 Traducir",
        "btn_stop": "⏹ Detener",
        "btn_log": "📋 Registro",
        "btn_help_quick": "📖 Guía",
        "prog_ready": "Listo — Añada documentos PDF y haga clic en «Traducir»",
        "prog_stopping": "Deteniendo la tarea actual...",
        "prog_processing": "Procesando: {name}",
        "prog_all_done": "🎉 Todas las tareas de la cola han finalizado",
        "prog_error": "Error: {err}",
        "msg_no_files": "Por favor, añada al menos un archivo PDF o Word a la lista.",
        "msg_unconfigured_title": "Clave API no configurada",
        "msg_unconfigured_body": "El proveedor «{svc}» aún no tiene una clave API configurada. ¿Ir a ajustes ahora?",
        "msg_stop_first": "Detenga primero la tarea de traducción en curso.",
        "msg_no_pdf_in_dir": "No se encontraron archivos PDF/Word traducibles en la carpeta seleccionada.",
        "dlg_add_url_title": "Añadir URL de PDF en línea",
        "dlg_add_url_label": "Introduzca una URL de PDF con http:// o https:// (ej. arXiv):",
        "pdf_orig": "Original",
        "pdf_mono": "Traducido (Mono)",
        "pdf_dual": "Bilingüe (Dual)",
        "pdf_total_pages": "/ {count} págs.",
        "pdf_open_ext": "Abrir externo",
        "pdf_open_ext_tip": "Abrir con el visor PDF predeterminado del sistema",
        "pdf_reveal": "Mostrar carpeta",
        "pdf_reveal_tip": "Mostrar archivo en el explorador de archivos",
        "pdf_empty_hint": "Seleccione o arrastre un archivo PDF a la izquierda para previsualizar el original y la traducción",
        "pdf_err_load": "No se pudo previsualizar el PDF: {err}",
        "status_free": "Gratis",
        "status_ready": "Listo",
        "status_need_key": "Falta clave",
        "status_configured": "Configurado",
        "ai_list_title": "Proveedores de IA y Traducción",
        "ai_search_ph": "🔍 Buscar proveedor (DeepSeek, OpenAI, Gemini...)",
        "ai_btn_doc": "🔗 Obtener clave API / Consola",
        "ai_current_default": " (Predeterminado)",
        "ai_no_key_needed": "✅ Este servicio no requiere clave API y está listo para usarse.",
        "ai_cli_hint": "💡 Guardado en ~/.config/PDFMathTranslate/config.json y compartido con CLI (-s {name}).",
        "ai_btn_save": "💾 Guardar configuración",
        "ai_btn_test": "⚡ Probar conexión",
        "ai_btn_testing": "⏳ Probando...",
        "ai_btn_set_default": "⭐ Establecer como predeterminado",
        "ai_btn_reset": "Restablecer",
        "btn_show": "Mostrar",
        "btn_hide": "Ocultar",
        "ai_msg_saved": "✅ Configuración guardada para «{svc}».",
        "ai_msg_default_set": "⭐ «{svc}» establecido como servicio predeterminado.",
        "ai_msg_reset": "Valores predeterminados restaurados para «{svc}».",
        "ai_msg_testing": "Probando conexión con «{svc}»...",
        "ts_card1_title": "Idiomas predeterminados y Modo del motor",
        "ts_card1_sub": "Configure el idioma de origen, idioma de destino y motor de diseño predeterminados.",
        "ts_lbl_source": "Idioma de origen:",
        "ts_lbl_target": "Idioma de destino:",
        "ts_lbl_mode": "Modo del motor:",
        "ts_mode_fast": "fast — Modo estándar (Análisis DocLayout-YOLO, recomendado)",
        "ts_mode_ultrafast": "ultrafast — Modo ultrarrápido (Flujo de texto PDF nativo)",
        "ts_mode_babeldoc": "babeldoc — Motor de diseño BabelDOC",
        "ts_mode_precise": "precise — Modo Precise v2 (requiere pdf2zh_next)",
        "ts_card2_title": "Protección de fórmulas y Fuentes",
        "ts_card2_sub": "Controle las expresiones regulares para fórmulas matemáticas y el subconjunto de fuentes PDF.",
        "ts_vfont_ph": "Dejar vacío para regla integrada, ej. (CM[^R]|MS.M|XY|MT|BL|RM|EU|LA|RS).*",
        "ts_btn_vfont_preset": "Rellenar Regex LaTeX",
        "ts_vchar_ph": "Regex de caracteres de fórmula personalizada (-c / --vchar)",
        "ts_chk_skip_subset": "Omitir subconjunto de fuentes (--skip-subset-fonts)",
        "ts_chk_compatible": "Convertir documento de entrada a PDF/A (--compatible)",
        "ts_lbl_vfont": "Regex de fuente (vfont):",
        "ts_lbl_vchar": "Regex de carácter (vchar):",
        "ts_card3_title": "Prompt LLM personalizado (Custom Prompt)",
        "ts_card3_sub": "Personalice las instrucciones para LLMs. Variables: ${lang_in}, ${lang_out}, ${text}.",
        "ts_chk_use_prompt": "Habilitar plantilla de prompt LLM personalizada",
        "ts_btn_default_prompt": "Cargar plantilla académica predeterminada",
        "ts_btn_import_prompt": "Importar prompt desde archivo (.txt/.md)",
        "ts_card4_title": "Ajustes OCR (PDFs escaneados)",
        "ts_card4_sub": "Detecta automáticamente páginas escaneadas mediante PyMuPDF + Tesseract.",
        "ts_ocr_lang_ph": "Dejar vacío para detección automática (ej. eng, spa, chi_sim)",
        "ts_tess_ph": "Dejar vacío para ~/.cache/pdf2zh/tessdata o TESSDATA_PREFIX",
        "ts_btn_browse_dir": "Examinar...",
        "ts_lbl_ocr_lang": "Idioma OCR:",
        "ts_lbl_tess_dir": "Carpeta TESSDATA:",
        "ts_btn_save": "💾 Guardar ajustes de traducción",
        "ts_msg_saved": "✅ Ajustes de traducción guardados",
        "os_card1_title": "Carpeta de salida",
        "os_card1_sub": "Configure dónde se guardarán los archivos PDF traducidos.",
        "os_chk_save_next": "Guardar en la misma carpeta que el PDF original (Recomendado)",
        "os_lbl_fixed_dir": "Carpeta fija:",
        "os_dir_ph": "Carpeta personalizada, ej. ~/Downloads/PDF_Translated",
        "os_btn_browse": "Examinar...",
        "os_btn_open_dir": "Abrir carpeta",
        "os_card2_title": "Variantes de archivos de salida",
        "os_card2_sub": "Elija generar solo la versión traducida (Mono), la versión bilingüe (Dual) o ambas.",
        "os_chk_mono": "Generar PDF solo traducido (sufijo -mono.pdf)",
        "os_chk_dual": "Generar PDF bilingüe comparativo (sufijo -dual.pdf)",
        "os_card3_title": "Hilos simultáneos y Automatización",
        "os_card3_sub": "Controle la concurrencia de solicitudes de traducción.",
        "os_lbl_threads": "Hilos simultáneos (-t):",
        "os_chk_auto_preview": "Previsualizar automáticamente en el lector integrado al finalizar",
        "os_chk_auto_open_dir": "Abrir carpeta de salida automáticamente al terminar la cola",
        "os_btn_save": "💾 Guardar ajustes de salida",
        "os_msg_saved": "✅ Ajustes de salida guardados",
        "ss_card1_title": "Proxy de red (HTTP / HTTPS Proxy)",
        "ss_card1_sub": "Configure un proxy local para acceder a OpenAI, Gemini, Google o HuggingFace.",
        "ss_chk_proxy": "Habilitar proxy de red personalizado (HTTP_PROXY y HTTPS_PROXY)",
        "ss_lbl_proxy_url": "URL del proxy:",
        "ss_proxy_ph": "ej. http://127.0.0.1:7890 o socks5://127.0.0.1:1080",
        "ss_card2_title": "Caché de traducción (SQLite Cache)",
        "ss_card2_sub": "Almacena en caché los párrafos traducidos para ahorrar tokens de API.",
        "ss_chk_ignore_cache": "Ignorar caché de traducción (--ignore-cache)",
        "ss_btn_refresh_cache": "🔄 Actualizar estadísticas",
        "ss_btn_clear_cache": "🧹 Borrar caché de traducción",
        "ss_btn_reveal_cache": "Mostrar archivo de caché",
        "ss_card3_title": "Modelo ONNX y Aceleración por hardware",
        "ss_card3_sub": "Configure el backend de inferencia ONNX para DocLayout-YOLO.",
        "ss_lbl_onnx_backend": "Backend ONNX:",
        "ss_lbl_onnx_path": "Modelo ONNX personalizado:",
        "ss_onnx_ph": "Dejar vacío para usar el modelo DocLayout-YOLO integrado",
        "ss_btn_browse_onnx": "Seleccionar .onnx...",
        "ss_card4_title": "Gestión y Copia de seguridad de configuración",
        "ss_btn_open_cfg": "📂 Mostrar config.json",
        "ss_btn_export_cfg": "📤 Exportar configuración (.json)",
        "ss_btn_import_cfg": "📥 Importar configuración (.json)",
        "ss_btn_reset_all": "⚠️ Restablecer todos los ajustes",
        "ss_btn_save": "💾 Guardar ajustes del sistema",
        "ss_msg_saved": "✅ Ajustes del sistema guardados",
        "help_title": "📖 Guía de usuario de PDFMathTranslate Desktop",
        "help_subtitle": "Traducción de PDFs académicos con IA preservando fórmulas, tablas, índice y código",
        "help_btn_go_workspace": "🚀 Ir al espacio de trabajo",
        "help_btn_go_keys": "🔑 Configurar claves IA",
        "help_btn_github": "🌐 Abrir repositorio GitHub",
    },
    "it": {
        "window_title": "PDFMathTranslate Desktop v{version} — Traduttore PDF Accademico Bilingue con IA",
        "nav_workspace": "📄  Area di lavoro",
        "nav_ai_keys": "🔑  Chiavi API e Provider",
        "nav_trans_settings": "⚙️  Traduzione e Layout",
        "nav_output_settings": "📁  Output e Coda",
        "nav_system_settings": "🛠️  Sistema e Avanzate",
        "nav_user_guide": "📖  Guida per l'utente",
        "ui_lang_label": "🌐 Lingua UI:",
        "sb_default_service": "Servizio predefinito: {svc}",
        "sb_default_mode": "Motore: {mode} | Thread: {threads}",
        "sb_proxy_on": "Proxy: Attivo",
        "sb_proxy_off": "Proxy: Disattivato",
        "status_config_path": "File di configurazione: {path}",
        "menu_file": "File",
        "menu_add_files": "Aggiungi file PDF/Word...",
        "menu_add_folder": "Aggiungi cartella...",
        "menu_settings": "Chiavi API e Impostazioni...",
        "menu_help": "Aiuto",
        "menu_open_guide": "Apri guida per l'utente...",
        "drop_hint": "📄 Trascina qui file PDF / Word o cartelle",
        "btn_add_file": "＋ File",
        "btn_add_folder": "＋ Cartella",
        "btn_add_url": "＋ URL",
        "btn_clear": "Svuota",
        "col_filename": "Documento",
        "col_status": "Stato",
        "col_progress": "Progresso",
        "col_time": "Tempo",
        "status_pending": "In attesa",
        "status_running": "⏳ In corso",
        "status_done": "✅ Completato",
        "status_failed": "❌ Fallito",
        "opt_card_title": "Opzioni di traduzione",
        "lbl_ai_service": "Servizio IA / Traduzione:",
        "btn_cfg_key": "🔑 Chiave API",
        "tip_cfg_key": "Configura la chiave API e i parametri per questo provider",
        "lbl_model": "Modello (Model):",
        "model_default_none": "Predefinito (nessun modello richiesto)",
        "lbl_trans_lang": "Lingue:",
        "tip_swap_lang": "Scambia lingua di origine e di destinazione",
        "lbl_page_range": "Pagine:",
        "pages_all": "Tutte le pagine (All)",
        "pages_first": "Solo pagina 1",
        "pages_first5": "Prime 5 pagine (1-5)",
        "pages_custom": "Intervallo personalizzato",
        "pages_custom_ph": "es. 1-3, 5, 8-10",
        "lbl_engine_mode": "Motore:",
        "mode_fast_short": "fast (Analisi layout IA standard)",
        "mode_ultrafast_short": "ultrafast (Flusso nativo ultraveloce)",
        "mode_babeldoc_short": "babeldoc (Motore BabelDOC)",
        "mode_precise_short": "precise (Modalità Precise v2)",
        "lbl_output_opt": "Output:",
        "chk_mono_short": "Solo tradotto (Mono)",
        "chk_dual_short": "Bilingue (Dual)",
        "chk_ignore_cache_short": "Senza cache",
        "btn_start": "🚀 Traduci",
        "btn_stop": "⏹ Ferma",
        "btn_log": "📋 Log",
        "btn_help_quick": "📖 Guida",
        "prog_ready": "Pronto — Aggiungi file PDF e clicca su «Traduci»",
        "prog_stopping": "Arresto dell'attività in corso...",
        "prog_processing": "Elaborazione: {name}",
        "prog_all_done": "🎉 Tutte le attività della coda sono state completate",
        "prog_error": "Errore: {err}",
        "msg_no_files": "Aggiungi almeno un file PDF o Word all'elenco.",
        "msg_unconfigured_title": "Chiave API non configurata",
        "msg_unconfigured_body": "Il servizio «{svc}» non ha ancora una chiave API configurata. Aprire le impostazioni ora?",
        "msg_stop_first": "Ferma prima la traduzione in corso.",
        "msg_no_pdf_in_dir": "Nessun file PDF/Word traducibile trovato nella cartella selezionata.",
        "dlg_add_url_title": "Aggiungi URL PDF online",
        "dlg_add_url_label": "Inserisci un URL PDF che inizia con http:// o https:// (es. arXiv):",
        "pdf_orig": "Originale",
        "pdf_mono": "Tradotto (Mono)",
        "pdf_dual": "Bilingue (Dual)",
        "pdf_total_pages": "/ {count} pag.",
        "pdf_open_ext": "Apri esterno",
        "pdf_open_ext_tip": "Apri con il lettore PDF predefinito di sistema",
        "pdf_reveal": "Mostra cartella",
        "pdf_reveal_tip": "Mostra file nel gestore file di sistema",
        "pdf_empty_hint": "Seleziona o trascina un file PDF a sinistra per vedere l'anteprima dell'originale e della traduzione",
        "pdf_err_load": "Impossibile caricare l'anteprima PDF: {err}",
        "status_free": "Gratuito",
        "status_ready": "Pronto",
        "status_need_key": "Chiave richiesta",
        "status_configured": "Configurato",
        "ai_list_title": "Provider IA e Traduzione",
        "ai_search_ph": "🔍 Cerca provider (DeepSeek, OpenAI, Gemini...)",
        "ai_btn_doc": "🔗 Ottieni chiave API / Console",
        "ai_current_default": " (Predefinito)",
        "ai_no_key_needed": "✅ Questo servizio non richiede una chiave API ed è subito pronto all'uso.",
        "ai_cli_hint": "💡 Salvato in ~/.config/PDFMathTranslate/config.json e condiviso con la CLI (-s {name}).",
        "ai_btn_save": "💾 Salva configurazione",
        "ai_btn_test": "⚡ Testa connessione",
        "ai_btn_testing": "⏳ Test in corso...",
        "ai_btn_set_default": "⭐ Imposta come predefinito",
        "ai_btn_reset": "Ripristina",
        "btn_show": "Mostra",
        "btn_hide": "Nascondi",
        "ai_msg_saved": "✅ Configurazione salvata per «{svc}».",
        "ai_msg_default_set": "⭐ «{svc}» impostato come servizio predefinito.",
        "ai_msg_reset": "Valori predefiniti ripristinati per «{svc}».",
        "ai_msg_testing": "Test di connessione a «{svc}» in corso...",
        "ts_card1_title": "Lingue predefinite e Modalità motore",
        "ts_card1_sub": "Configura lingua di origine, lingua di destinazione e motore di layout predefiniti.",
        "ts_lbl_source": "Lingua di origine:",
        "ts_lbl_target": "Lingua di destinazione:",
        "ts_lbl_mode": "Modalità motore:",
        "ts_mode_fast": "fast — Modalità standard (Analisi DocLayout-YOLO, consigliata)",
        "ts_mode_ultrafast": "ultrafast — Modalità ultraveloce (Flusso testo PDF nativo)",
        "ts_mode_babeldoc": "babeldoc — Backend di layout BabelDOC",
        "ts_mode_precise": "precise — Modalità Precise v2 (richiede pdf2zh_next)",
        "ts_card2_title": "Protezione formule e Impostazioni font",
        "ts_card2_sub": "Controlla le espressioni regolari per le formule matematiche e il subsetting dei font PDF.",
        "ts_vfont_ph": "Lascia vuoto per la regola predefinita, es. (CM[^R]|MS.M|XY|MT|BL|RM|EU|LA|RS).*",
        "ts_btn_vfont_preset": "Inserisci Regex LaTeX",
        "ts_vchar_ph": "Regex personalizzata caratteri formula (-c / --vchar)",
        "ts_chk_skip_subset": "Salta subsetting dei font (--skip-subset-fonts)",
        "ts_chk_compatible": "Converti documento di input in formato PDF/A (--compatible)",
        "ts_lbl_vfont": "Regex font formule (vfont):",
        "ts_lbl_vchar": "Regex caratteri formule (vchar):",
        "ts_card3_title": "Prompt LLM personalizzato (Custom Prompt)",
        "ts_card3_sub": "Personalizza le istruzioni di traduzione per gli LLM. Variabili: ${lang_in}, ${lang_out}, ${text}.",
        "ts_chk_use_prompt": "Abilita modello di prompt LLM personalizzato",
        "ts_btn_default_prompt": "Inserisci modello accademico predefinito",
        "ts_btn_import_prompt": "Importa prompt da file (.txt/.md)",
        "ts_card4_title": "Impostazioni OCR (PDF scansionati)",
        "ts_card4_sub": "Rileva automaticamente le pagine scansionate tramite PyMuPDF + Tesseract.",
        "ts_ocr_lang_ph": "Lascia vuoto per rilevamento automatico (es. eng, ita, chi_sim)",
        "ts_tess_ph": "Lascia vuoto per ~/.cache/pdf2zh/tessdata o TESSDATA_PREFIX",
        "ts_btn_browse_dir": "Sfoglia...",
        "ts_lbl_ocr_lang": "Lingua OCR:",
        "ts_lbl_tess_dir": "Cartella TESSDATA:",
        "ts_btn_save": "💾 Salva impostazioni di traduzione",
        "ts_msg_saved": "✅ Impostazioni di traduzione salvate",
        "os_card1_title": "Cartella di output",
        "os_card1_sub": "Scegli dove salvare i file PDF tradotti.",
        "os_chk_save_next": "Salva nella stessa cartella del file PDF originale (Consigliato)",
        "os_lbl_fixed_dir": "Cartella fissa:",
        "os_dir_ph": "Cartella personalizzata, es. ~/Downloads/PDF_Translated",
        "os_btn_browse": "Sfoglia...",
        "os_btn_open_dir": "Apri cartella",
        "os_card2_title": "Varianti file di output",
        "os_card2_sub": "Scegli se generare solo la versione tradotta (Mono), la versione bilingue (Dual) o entrambe.",
        "os_chk_mono": "Genera PDF solo tradotto (suffisso -mono.pdf)",
        "os_chk_dual": "Genera PDF bilingue a fronte (suffisso -dual.pdf)",
        "os_card3_title": "Thread simultanei e Automazione",
        "os_card3_sub": "Controlla il numero di richieste di traduzione simultanee.",
        "os_lbl_threads": "Thread simultanei (-t):",
        "os_chk_auto_preview": "Mostra automaticamente l'anteprima nel lettore integrato al termine",
        "os_chk_auto_open_dir": "Apri automaticamente la cartella di output al termine della coda",
        "os_btn_save": "💾 Salva impostazioni di output",
        "os_msg_saved": "✅ Impostazioni di output salvate",
        "ss_card1_title": "Proxy di rete (HTTP / HTTPS Proxy)",
        "ss_card1_sub": "Configura un proxy locale per accedere a OpenAI, Gemini, Google o HuggingFace.",
        "ss_chk_proxy": "Abilita proxy di rete personalizzato (HTTP_PROXY e HTTPS_PROXY)",
        "ss_lbl_proxy_url": "URL Proxy:",
        "ss_proxy_ph": "es. http://127.0.0.1:7890 o socks5://127.0.0.1:1080",
        "ss_card2_title": "Cache di traduzione (SQLite Cache)",
        "ss_card2_sub": "Memorizza nella cache i paragrafi tradotti per risparmiare token API.",
        "ss_chk_ignore_cache": "Ignora cache di traduzione (--ignore-cache)",
        "ss_btn_refresh_cache": "🔄 Aggiorna statistiche cache",
        "ss_btn_clear_cache": "🧹 Svuota cache di traduzione",
        "ss_btn_reveal_cache": "Mostra file cache",
        "ss_card3_title": "Modello ONNX e Accelerazione hardware",
        "ss_card3_sub": "Configura il backend di inferenza ONNX per DocLayout-YOLO.",
        "ss_lbl_onnx_backend": "Backend ONNX:",
        "ss_lbl_onnx_path": "Modello ONNX personalizzato:",
        "ss_onnx_ph": "Lascia vuoto per usare il modello DocLayout-YOLO integrato",
        "ss_btn_browse_onnx": "Seleziona .onnx...",
        "ss_card4_title": "Gestione configurazione e Backup",
        "ss_btn_open_cfg": "📂 Mostra config.json",
        "ss_btn_export_cfg": "📤 Esporta configurazione (.json)",
        "ss_btn_import_cfg": "📥 Importa configurazione (.json)",
        "ss_btn_reset_all": "⚠️ Ripristina tutte le impostazioni",
        "ss_btn_save": "💾 Salva impostazioni di sistema",
        "ss_msg_saved": "✅ Impostazioni di sistema salvate",
        "help_title": "📖 Guida per l'utente PDFMathTranslate Desktop",
        "help_subtitle": "Traduzione PDF accademica con IA preservando formule, tabelle, indice e codice",
        "help_btn_go_workspace": "🚀 Vai all'area di lavoro",
        "help_btn_go_keys": "🔑 Configura chiavi IA",
        "help_btn_github": "🌐 Apri repository GitHub",
    },
}


class I18nManager:
    """Manages active UI language and string lookups."""

    @classmethod
    def get_lang(cls) -> str:
        lang = str(AppSettings.get("PDF2ZH_UI_LANG", "zh") or "zh")
        return lang if lang in UI_LANGUAGES else "zh"

    @classmethod
    def set_lang(cls, lang: str) -> None:
        if lang in UI_LANGUAGES:
            AppSettings.set("PDF2ZH_UI_LANG", lang)

    @classmethod
    def tr(cls, key: str, **kwargs: Any) -> str:
        lang = cls.get_lang()
        table = TRANSLATIONS.get(lang, TRANSLATIONS["zh"])
        template = table.get(key) or TRANSLATIONS["zh"].get(key) or key
        if kwargs:
            try:
                return template.format(**kwargs)
            except Exception:
                return template
        return template


def tr(key: str, **kwargs: Any) -> str:
    return I18nManager.tr(key, **kwargs)


# Localized display names for source/target languages across all 10 UI languages
LOCALIZED_LANG_LABELS: dict[str, dict[str, str]] = {
    "zh": {
        "zh": "简体中文 (Simplified Chinese)",
        "zh-TW": "繁体中文 (Traditional Chinese)",
        "en": "英语 (English)",
        "ja": "日语 (Japanese)",
        "ko": "韩语 (Korean)",
        "fr": "法语 (French)",
        "de": "德语 (German)",
        "ru": "俄语 (Russian)",
        "es": "西班牙语 (Spanish)",
        "it": "意大利语 (Italian)",
    },
    "zh-TW": {
        "zh": "簡體中文 (Simplified Chinese)",
        "zh-TW": "繁體中文 (Traditional Chinese)",
        "en": "英語 (English)",
        "ja": "日語 (Japanese)",
        "ko": "韓語 (Korean)",
        "fr": "法語 (French)",
        "de": "德語 (German)",
        "ru": "俄語 (Russian)",
        "es": "西班牙語 (Spanish)",
        "it": "義大利語 (Italian)",
    },
    "en": {
        "zh": "Simplified Chinese (简体中文)",
        "zh-TW": "Traditional Chinese (繁體中文)",
        "en": "English",
        "ja": "Japanese (日本語)",
        "ko": "Korean (한국어)",
        "fr": "French (Français)",
        "de": "German (Deutsch)",
        "ru": "Russian (Русский)",
        "es": "Spanish (Español)",
        "it": "Italian (Italiano)",
    },
    "ja": {
        "zh": "簡体字中国語 (简体中文)",
        "zh-TW": "繁体字中国語 (繁體中文)",
        "en": "英語 (English)",
        "ja": "日本語 (Japanese)",
        "ko": "韓国語 (한국어)",
        "fr": "フランス語 (Français)",
        "de": "ドイツ語 (Deutsch)",
        "ru": "ロシア語 (Русский)",
        "es": "スペイン語 (Español)",
        "it": "イタリア語 (Italiano)",
    },
    "ko": {
        "zh": "중국어 간체 (简体中文)",
        "zh-TW": "중국어 번체 (繁體中文)",
        "en": "영어 (English)",
        "ja": "일본어 (日本語)",
        "ko": "한국어 (Korean)",
        "fr": "프랑스어 (Français)",
        "de": "독일어 (Deutsch)",
        "ru": "러시아어 (Русский)",
        "es": "스페인어 (Español)",
        "it": "이탈리아어 (Italiano)",
    },
    "fr": {
        "zh": "Chinois simplifié (简体中文)",
        "zh-TW": "Chinois traditionnel (繁體中文)",
        "en": "Anglais (English)",
        "ja": "Japonais (日本語)",
        "ko": "Coréen (한국어)",
        "fr": "Français (French)",
        "de": "Allemand (Deutsch)",
        "ru": "Russe (Русский)",
        "es": "Espagnol (Español)",
        "it": "Italien (Italiano)",
    },
    "de": {
        "zh": "Chinesisch vereinfacht (简体中文)",
        "zh-TW": "Chinesisch traditionell (繁體中文)",
        "en": "Englisch (English)",
        "ja": "Japanisch (日本語)",
        "ko": "Koreanisch (한국어)",
        "fr": "Französisch (Français)",
        "de": "Deutsch (German)",
        "ru": "Russisch (Русский)",
        "es": "Spanisch (Español)",
        "it": "Italienisch (Italiano)",
    },
    "ru": {
        "zh": "Китайский упрощённый (简体中文)",
        "zh-TW": "Китайский традиционный (繁體中文)",
        "en": "Английский (English)",
        "ja": "Японский (日本語)",
        "ko": "Корейский (한국어)",
        "fr": "Французский (Français)",
        "de": "Немецкий (Deutsch)",
        "ru": "Русский (Russian)",
        "es": "Испанский (Español)",
        "it": "Итальянский (Italiano)",
    },
    "es": {
        "zh": "Chino simplificado (简体中文)",
        "zh-TW": "Chino tradicional (繁體中文)",
        "en": "Inglés (English)",
        "ja": "Japonés (日本語)",
        "ko": "Coreano (한국어)",
        "fr": "Francés (Français)",
        "de": "Alemán (Deutsch)",
        "ru": "Ruso (Русский)",
        "es": "Español (Spanish)",
        "it": "Italiano (Italian)",
    },
    "it": {
        "zh": "Cinese semplificato (简体中文)",
        "zh-TW": "Cinese tradizionale (繁體中文)",
        "en": "Inglese (English)",
        "ja": "Giapponese (日本語)",
        "ko": "Coreano (한국어)",
        "fr": "Francese (Français)",
        "de": "Tedesco (Deutsch)",
        "ru": "Russo (Русский)",
        "es": "Spagnolo (Español)",
        "it": "Italiano (Italian)",
    },
}

CATEGORY_TRANSLATIONS: dict[str, dict[str, str]] = {
    "AI 大模型": {
        "zh": "AI 大模型",
        "zh-TW": "AI 大模型",
        "en": "AI LLM",
        "ja": "AI 大規模言語モデル",
        "ko": "AI 대규모 모델",
        "fr": "Modèle IA (LLM)",
        "de": "KI-Sprachmodell",
        "ru": "ИИ-модель (LLM)",
        "es": "Modelo IA (LLM)",
        "it": "Modello IA (LLM)",
    },
    "本地部署": {
        "zh": "本地部署",
        "zh-TW": "本地部署",
        "en": "Local / Offline",
        "ja": "ローカル実行",
        "ko": "로컬 실행",
        "fr": "Local / Hors ligne",
        "de": "Lokal / Offline",
        "ru": "Локально",
        "es": "Local / Sin conexión",
        "it": "Locale / Offline",
    },
    "AI 应用编排": {
        "zh": "AI 应用编排",
        "zh-TW": "AI 應用編排",
        "en": "AI Workflow",
        "ja": "AI ワークフロー",
        "ko": "AI 워크플로",
        "fr": "Flux de travail IA",
        "de": "KI-Workflow",
        "ru": "ИИ-воркфлоу",
        "es": "Flujo IA",
        "it": "Workflow IA",
    },
    "传统机器翻译": {
        "zh": "传统机器翻译",
        "zh-TW": "傳統機器翻譯",
        "en": "Machine Translation",
        "ja": "機械翻訳",
        "ko": "기계 번역",
        "fr": "Traduction automatique",
        "de": "Maschinenübersetzung",
        "ru": "Машинный перевод",
        "es": "Traducción automática",
        "it": "Traduzione automatica",
    },
}

PROVIDER_DESC_EN: dict[str, str] = {
    "OpenAI": "Official OpenAI API or compatible endpoint supporting GPT-4o / GPT-4.1 models.",
    "DeepSeek": "Official DeepSeek API — high accuracy and great cost efficiency for academic PDFs.",
    "Gemini": "Google Gemini OpenAI-compatible API with fast inference and large context window.",
    "Ali Qwen-Translation": "Alibaba Cloud Bailian Qwen-MT model optimized for scientific document translation.",
    "Silicon (硅基流动)": "SiliconFlow cloud inference platform offering Qwen2.5, DeepSeek-V3, and more.",
    "Zhipu (智谱 GLM)": "Zhipu AI open platform (glm-4-flash offers fast and free inference).",
    "ModelScope (魔搭)": "ModelScope API-Inference community endpoint.",
    "OpenAI-liked (自定义兼容接口)": "Supports any third-party OpenAI Chat Completions compatible relay, OneAPI, vLLM, or LM Studio.",
    "Ollama (本地模型)": "Local Ollama server — runs 100% offline without an API key for full privacy.",
    "AzureOpenAI": "Microsoft Azure OpenAI enterprise service.",
    "Grok (xAI)": "xAI Grok LLM API.",
    "Groq": "Groq LPU ultra-fast inference platform.",
    "MiniMax": "MiniMax Open Platform LLM API.",
    "302.AI": "302.AI aggregated AI gateway.",
    "Xinference": "Xorbits Inference local / private model serving.",
    "Dify": "Connect to self-hosted or cloud Dify workflow / app API.",
    "AnythingLLM": "Connect to AnythingLLM local or private workspace chat API.",
    "Google": "Free Google web translation API (requires network access to Google).",
    "Bing": "Free Microsoft Bing translator — works out-of-the-box with no API key required.",
    "DeepL": "Official DeepL Pro / Free API (requires DeepL Auth Key).",
    "DeepLX": "Self-hosted or third-party DeepLX endpoint.",
    "Azure Translator": "Microsoft Azure Cognitive Services Text Translation API.",
    "Tencent (腾讯云翻译)": "Tencent Cloud Machine Translation (TMT) requiring SecretId & SecretKey.",
    "Argos Translate": "Offline open-source neural translation via argostranslate.",
}


def get_localized_lang_label(code: str) -> str:
    lang = I18nManager.get_lang()
    lang_map = LOCALIZED_LANG_LABELS.get(lang, LOCALIZED_LANG_LABELS["zh"])
    return lang_map.get(code, LOCALIZED_LANG_LABELS["zh"].get(code, code))


def get_localized_category(cat_zh: str) -> str:
    lang = I18nManager.get_lang()
    entry = CATEGORY_TRANSLATIONS.get(cat_zh)
    if not entry:
        return cat_zh
    return entry.get(lang, entry.get("en", cat_zh))


def get_localized_provider_desc(service_key: str, default_desc: str = "") -> str:
    lang = I18nManager.get_lang()
    if lang == "zh":
        return default_desc
    if lang == "zh-TW":
        # Traditional Chinese mapping for common terms
        return (
            default_desc.replace("官方接口或兼容代理，支持", "官方介面或相容代理，支援")
            .replace("模型", "模型")
            .replace("性价比极高，非常适合学术论文中英互译", "性價比極高，非常適合學術論文翻譯")
            .replace("兼容接口", "相容介面")
            .replace("阿里云百炼", "阿里雲百煉")
            .replace("专业翻译大模型，针对科技文献专门优化", "專業翻譯大模型，針對科技文獻專門最佳化")
            .replace("无需配置密钥", "無需設定金鑰")
            .replace("传统机器翻译", "傳統機器翻譯")
            .replace("无需 API Key，保护数据隐私", "無需 API Key，保護資料隱私")
        )
    return PROVIDER_DESC_EN.get(service_key, default_desc)


def get_localized_field_label(env_key: str, default_label: str = "") -> str:
    lang = I18nManager.get_lang()
    if lang == "zh":
        return default_label
    upper = env_key.upper()
    if upper.endswith("BASE_URL") or upper.endswith("_ENDPOINT") or upper.endswith("_URL") or upper.endswith("_HOST"):
        labels = {
            "zh-TW": f"API 介面網址 ({env_key})",
            "en": f"API Endpoint / Base URL ({env_key})",
            "ja": f"API エンドポイント URL ({env_key})",
            "ko": f"API 엔드포인트 URL ({env_key})",
            "fr": f"URL du point de terminaison ({env_key})",
            "de": f"API-Basis-URL ({env_key})",
            "ru": f"Базовый URL API ({env_key})",
            "es": f"URL base de API ({env_key})",
            "it": f"URL base API ({env_key})",
        }
        return labels.get(lang, default_label)
    if upper.endswith("MODEL"):
        labels = {
            "zh-TW": f"模型名稱 ({env_key})",
            "en": f"Model Name ({env_key})",
            "ja": f"モデル名 ({env_key})",
            "ko": f"모델 이름 ({env_key})",
            "fr": f"Nom du modèle ({env_key})",
            "de": f"Modellname ({env_key})",
            "ru": f"Имя модели ({env_key})",
            "es": f"Nombre del modelo ({env_key})",
            "it": f"Nome modello ({env_key})",
        }
        return labels.get(lang, default_label)
    if any(k in upper for k in ("KEY", "TOKEN", "SECRET")):
        labels = {
            "zh-TW": f"API 金鑰 ({env_key})",
            "en": f"API Key / Secret ({env_key})",
            "ja": f"API キー / トークン ({env_key})",
            "ko": f"API 키 / 시크릿 ({env_key})",
            "fr": f"Clé API / Jeton ({env_key})",
            "de": f"API-Schlüssel / Token ({env_key})",
            "ru": f"API-ключ / Токен ({env_key})",
            "es": f"Clave API / Token ({env_key})",
            "it": f"Chiave API / Token ({env_key})",
        }
        return labels.get(lang, default_label)
    return env_key if lang != "zh-TW" else default_label


def get_user_guide_html(lang: str) -> str:
    """Return rich HTML user guide for the selected UI language."""
    css = """
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif;
            color: #1E293B;
            line-height: 1.65;
            font-size: 13.5px;
        }
        h2 {
            color: #0F172A;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 6px;
            margin-top: 22px;
            margin-bottom: 10px;
            font-size: 17px;
        }
        h3 {
            color: #1D4ED8;
            margin-top: 14px;
            margin-bottom: 6px;
            font-size: 14.5px;
        }
        .box {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 12px;
        }
        .tip {
            background-color: #EFF6FF;
            border-left: 4px solid #2563EB;
            padding: 10px 14px;
            margin: 10px 0;
            color: #1E3A8A;
        }
        code {
            background-color: #F1F5F9;
            color: #0F172A;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: Menlo, Monaco, Consolas, monospace;
            font-size: 12.5px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
        }
        th, td {
            border: 1px solid #CBD5E1;
            padding: 8px 10px;
            text-align: left;
        }
        th {
            background-color: #F1F5F9;
            font-weight: 600;
        }
    </style>
    """

    if lang == "en":
        return css + """
        <h2>🚀 1. Quick Start (3 Steps)</h2>
        <div class="box">
            <ol>
                <li><b>Configure Translation Service (Optional for Bing/Google):</b>
                    Click <b>🔑 AI Keys & Providers</b> in the left sidebar. Select your preferred AI provider (e.g., <b>DeepSeek</b>, <b>OpenAI</b>, <b>Gemini</b>, <b>Ali Qwen-Translation</b>, or local <b>Ollama</b>), enter your API Key, click <b>⚡ Test Connection</b>, and click <b>⭐ Set as Default</b>.
                    <br><i>Tip: If you don't have an API Key yet, <b>Bing</b> works out-of-the-box for free!</i>
                </li>
                <li><b>Add PDF / Word Documents:</b>
                    In <b>📄 Workspace</b>, drag & drop one or more <code>.pdf</code> / <code>.docx</code> files (or an entire folder) into the queue, or click <b>＋ URL</b> to translate an online paper (such as an arXiv PDF link).
                </li>
                <li><b>Translate & Preview Side-by-Side:</b>
                    Choose your source/target languages and click <b>🚀 Translate</b>. Once finished, use the right-hand preview pane to switch between <b>Original</b>, <b>Translated (Mono)</b>, and <b>Bilingual (Dual)</b> PDFs!
                </li>
            </ol>
        </div>

        <h2>🔑 2. Recommended AI Providers</h2>
        <table>
            <tr>
                <th>Provider</th>
                <th>Recommended Model</th>
                <th>Highlights</th>
            </tr>
            <tr>
                <td><b>DeepSeek</b></td>
                <td><code>deepseek-chat</code></td>
                <td>Extremely low cost, high accuracy for STEM & academic papers.</td>
            </tr>
            <tr>
                <td><b>Ali Qwen-Translation</b></td>
                <td><code>qwen-mt-turbo</code> / <code>qwen-mt-plus</code></td>
                <td>Purpose-built scientific translation model from Alibaba Cloud Bailian.</td>
            </tr>
            <tr>
                <td><b>OpenAI / OpenAI-liked</b></td>
                <td><code>gpt-4o-mini</code> / Custom</td>
                <td>Supports official OpenAI API as well as any third-party OpenAI-compatible relay, OneAPI, vLLM, or LM Studio.</td>
            </tr>
            <tr>
                <td><b>Gemini</b></td>
                <td><code>gemini-2.0-flash</code> / <code>gemini-1.5-flash</code></td>
                <td>Fast speed and generous free tier via Google AI Studio.</td>
            </tr>
            <tr>
                <td><b>Ollama (Local)</b></td>
                <td><code>qwen2.5:7b</code> / <code>gemma2</code></td>
                <td>100% offline local inference, zero API cost, complete data privacy.</td>
            </tr>
        </table>

        <h2>⚡ 3. Engine Modes Comparison</h2>
        <ul>
            <li><b><code>fast</code> (Standard AI Layout — Recommended):</b> Uses the DocLayout-YOLO neural model to accurately detect paragraphs, formulas, figures, and tables, preserving mathematical notation <code>{v*}</code> intact.</li>
            <li><b><code>ultrafast</code> (Ultrafast Native Stream):</b> Skips neural layout detection and OCR, parsing PDF text streams directly. Up to 10x faster for clean digital PDFs.</li>
            <li><b><code>babeldoc</code> (BabelDOC Backend):</b> Experimental layout engine for complex multi-column layouts and rich-text styling.</li>
            <li><b><code>precise</code> (Precise v2 Kernel):</b> Uses the isolated <code>pdf2zh_next</code> environment if provisioned.</li>
        </ul>

        <h2>📐 4. Formula Preservation & Custom Prompts</h2>
        <div class="tip">
            <b>Formula Protection:</b> Inline and display math formulas are automatically replaced with placeholders like <code>{v0}</code>, <code>{v1}</code> before sending to the LLM, and restored in their exact positions afterward.
            If certain special math fonts are not recognized as formulas, go to <b>⚙️ Translation & Layout</b> and click <b>"Fill Common LaTeX Math Font Regex"</b> under <code>vfont</code>.
        </div>
        <ul>
            <li><b>Custom LLM Prompt:</b> In <b>⚙️ Translation & Layout</b>, you can enable a custom prompt template to specify domain terminology (e.g., Computer Science, Medicine, Finance). Make sure to keep <code>${lang_out}</code> and <code>${text}</code> in your template.</li>
        </ul>

        <h2>❓ 5. Troubleshooting & FAQ</h2>
        <ul>
            <li><b>Network / Timeout Errors:</b> If using OpenAI, Gemini, or Google Translate from behind a firewall, enable your local proxy (e.g., <code>http://127.0.0.1:7890</code>) in <b>🛠️ System & Advanced</b>.</li>
            <li><b>Rate Limit (429 Too Many Requests):</b> Lower the <b>Concurrent Threads (-t)</b> value (e.g. from 4 to 1 or 2) in <b>📁 Output & Tasks</b>.</li>
            <li><b>Retranslating with a New Prompt/Model:</b> Check <b>No Cache</b> in the Workspace or clear the SQLite cache in <b>🛠️ System & Advanced</b>.</li>
        </ul>
        """

    if lang == "zh-TW":
        return css + """
        <h2>🚀 1. 快速上手（三步完成論文翻譯）</h2>
        <div class="box">
            <ol>
                <li><b>設定 AI 金鑰（若使用必應 Bing 可略過）：</b>
                    點擊左側導覽列的 <b>🔑 AI 金鑰與服務商</b>，選擇您常用的服務商（如 <b>DeepSeek</b>、<b>OpenAI</b>、<b>Gemini</b>、<b>阿里雲百煉 Qwen-MT</b> 或本地 <b>Ollama</b>），填入 API Key 後點擊 <b>⚡ 測試連線</b>，測試成功後點擊 <b>⭐ 設為預設翻譯服務</b>。
                </li>
                <li><b>加入 PDF / Word 文件：</b>
                    在 <b>📄 翻譯工作台</b> 中，直接將一個或多個 <code>.pdf</code> / <code>.docx</code> 檔案（或整個資料夾）拖入視窗，或點擊 <b>＋ 連結</b> 輸入線上 PDF 網址（如 arXiv 論文連結）。
                </li>
                <li><b>開始翻譯與雙語對照預覽：</b>
                    選擇來源語言與目標語言後點擊 <b>🚀 開始翻譯</b>。完成後可在右側內建高解析度閱讀器中一鍵切換 <b>原文</b>、<b>純譯文 (Mono)</b> 與 <b>雙語對照 (Dual)</b>！
                </li>
            </ol>
        </div>

        <h2>🔑 2. 主流 AI 翻譯服務推薦</h2>
        <table>
            <tr>
                <th>服務商</th>
                <th>推薦模型</th>
                <th>特點說明</th>
            </tr>
            <tr>
                <td><b>DeepSeek</b></td>
                <td><code>deepseek-chat</code></td>
                <td>性價比極高，中英學術論文術語翻譯準確自然。</td>
            </tr>
            <tr>
                <td><b>Ali Qwen-Translation</b></td>
                <td><code>qwen-mt-turbo</code> / <code>qwen-mt-plus</code></td>
                <td>阿里雲百煉專為科技文獻打造的翻譯模型。</td>
            </tr>
            <tr>
                <td><b>OpenAI-liked (自訂相容介面)</b></td>
                <td>自訂模型名稱</td>
                <td>支援所有相容 OpenAI 協定的第三方中轉站、OneAPI、vLLM、LM Studio。</td>
            </tr>
            <tr>
                <td><b>Ollama (本地模型)</b></td>
                <td><code>qwen2.5:7b</code> / <code>gemma2</code></td>
                <td>本機離線執行，無需 API Key，完全保護私密文件安全。</td>
            </tr>
        </table>

        <h2>⚡ 3. 四種排版引擎模式對比</h2>
        <ul>
            <li><b><code>fast</code>（標準模式，推薦）：</b>使用 DocLayout-YOLO 深度學習模型精準辨識段落、公式、圖表與表格，完整保留數學公式與目錄結構。</li>
            <li><b><code>ultrafast</code>（極速模式）：</b>略過神經網路版面分析與 OCR，直接解析原生 PDF 文字流，速度提升數倍（適合原生文字版 PDF）。</li>
            <li><b><code>babeldoc</code>（BabelDOC 增強後端）：</b>適合複雜多欄排版與富文本樣式還原。</li>
            <li><b><code>precise</code>（Precise v2 精準模式）：</b>呼叫獨立的 <code>pdf2zh_next</code> 核心。</li>
        </ul>

        <h2>📐 4. 公式保護與自訂提示詞技巧</h2>
        <div class="tip">
            <b>公式保護機制：</b>程式會在發送給 AI 之前將行內與獨立公式替換為 <code>{v0}</code>、<code>{v1}</code> 標記，並在翻譯後精準還原字型與位置。若發現個別特殊數學字型被誤翻，可在 <b>⚙️ 翻譯與排版設定</b> 中點擊 <b>「填入 LaTeX 常用數學字型正則」</b>。
        </div>
        """

    if lang == "ja":
        return css + """
        <h2>🚀 1. クイックスタート（3ステップ）</h2>
        <div class="box">
            <ol>
                <li><b>AI キーの設定（Bing / Google の場合は不要）：</b>
                    左サイドバーの <b>🔑 AI キー・プロバイダー設定</b> を開き、利用したい AI サービス（<b>DeepSeek</b>、<b>OpenAI</b>、<b>Gemini</b>、<b>Qwen-MT</b>、ローカルの <b>Ollama</b> など）を選択して API キーを入力します。<b>⚡ 接続テスト</b> で確認し、<b>⭐ 既定サービスに設定</b> をクリックします。
                </li>
                <li><b>PDF / Word ファイルの追加：</b>
                    <b>📄 翻訳ワークスペース</b> に <code>.pdf</code> / <code>.docx</code> ファイルまたはフォルダをドラッグ＆ドロップするか、<b>＋ URL</b> から arXiv などのオンライン PDF リンクを追加します。
                </li>
                <li><b>翻訳とプレビュー：</b>
                    言語を選択して <b>🚀 翻訳開始</b> をクリックします。完了後、右側のプレビュー画面で <b>原文</b>・<b>翻訳文 (Mono)</b>・<b>対訳 (Dual)</b> をワンクリックで切り替えられます。
                </li>
            </ol>
        </div>

        <h2>⚡ 2. 組版エンジンモードの比較</h2>
        <ul>
            <li><b><code>fast</code>（標準モード・推奨）：</b>DocLayout-YOLO モデルで段落・数式・図表を正確に検出し、数式 <code>{v*}</code> やレイアウトを維持します。</li>
            <li><b><code>ultrafast</code>（超高速モード）：</b>ニューラルレイアウト解析を省略し、PDF のネイティブテキストストリームを直接高速処理します。</li>
            <li><b><code>babeldoc</code>（BabelDOC バックエンド）：</b>複雑な段組みレイアウト向けの拡張バックエンドです。</li>
        </ul>
        """

    if lang == "ko":
        return css + """
        <h2>🚀 1. 빠른 시작 가이드 (3단계)</h2>
        <div class="box">
            <ol>
                <li><b>AI 키 설정 (Bing 사용 시 생략 가능):</b>
                    왼쪽 사이드바에서 <b>🔑 AI 키 및 서비스 설정</b>을 열고 원하는 서비스(<b>DeepSeek</b>, <b>OpenAI</b>, <b>Gemini</b>, <b>Qwen-MT</b> 또는 로컬 <b>Ollama</b>)를 선택한 후 API 키를 입력합니다. <b>⚡ 연결 테스트</b> 후 <b>⭐ 기본 서비스로 설정</b>을 클릭하세요.
                </li>
                <li><b>PDF / Word 파일 추가:</b>
                    <b>📄 번역 작업 공간</b>에 <code>.pdf</code> / <code>.docx</code> 파일이나 폴더를 드래그 앤 드롭하거나 <b>＋ 링크</b> 버튼으로 arXiv 등 온라인 PDF URL을 추가합니다.
                </li>
                <li><b>번역 시작 및 대조 미리보기:</b>
                    언어를 선택하고 <b>🚀 번역 시작</b>을 클릭합니다. 완료 후 오른쪽 미리보기 창에서 <b>원문</b>, <b>단일 번역본 (Mono)</b>, <b>이중 언어 대조본 (Dual)</b>을 즉시 전환하여 확인할 수 있습니다.
                </li>
            </ol>
        </div>
        <h2>⚡ 2. 조판 엔진 모드 비교</h2>
        <ul>
            <li><b><code>fast</code> (표준 AI 레이아웃 — 권장):</b> DocLayout-YOLO 모델로 문단, 수식, 표, 목차 및 코드 블록을 정확히 인식하고 수식 <code>{v*}</code>과 레이아웃을 보존합니다.</li>
            <li><b><code>ultrafast</code> (초고속 모드):</b> 딥러닝 레이아웃 분석을 생략하고 네이티브 PDF 스트림을 직접 분석합니다.</li>
            <li><b><code>babeldoc</code> (BabelDOC 백엔드):</b> 복잡한 다단 레이아웃을 위한 확장 렌더링 파이프라인입니다.</li>
        </ul>
        """

    if lang == "fr":
        return css + """
        <h2>🚀 1. Démarrage rapide (en 3 étapes)</h2>
        <div class="box">
            <ol>
                <li><b>Configurer la clé IA (optionnel pour Bing) :</b>
                    Ouvrez <b>🔑 Clés IA & Fournisseurs</b> dans la barre latérale, choisissez un fournisseur (<b>DeepSeek</b>, <b>OpenAI</b>, <b>Gemini</b>, <b>Qwen-MT</b> ou <b>Ollama</b> en local), saisissez votre clé API, cliquez sur <b>⚡ Tester la connexion</b> puis sur <b>⭐ Définir par défaut</b>.
                </li>
                <li><b>Ajouter des fichiers PDF / Word :</b>
                    Dans <b>📄 Espace de travail</b>, glissez-déposez vos fichiers <code>.pdf</code> / <code>.docx</code> ou un dossier complet, ou cliquez sur <b>＋ URL</b> pour traduire un article en ligne (ex. arXiv).
                </li>
                <li><b>Traduire et prévisualiser :</b>
                    Sélectionnez les langues source/cible et cliquez sur <b>🚀 Traduire</b>. Basculez ensuite entre <b>Original</b>, <b>Traduit (Mono)</b> et <b>Bilingue (Dual)</b> dans l'aperçu à droite.
                </li>
            </ol>
        </div>
        <h2>⚡ 2. Comparaison des moteurs de mise en page</h2>
        <ul>
            <li><b><code>fast</code> (Standard — Recommandé) :</b> Utilise DocLayout-YOLO pour préserver intégralement les formules mathématiques <code>{v*}</code>, la table des matières et les blocs de code.</li>
            <li><b><code>ultrafast</code> (Ultra-rapide) :</b> Analyse directement le flux PDF natif sans modèle neuronal ni OCR.</li>
            <li><b><code>babeldoc</code> (Backend BabelDOC) :</b> Moteur expérimental pour les mises en page multicolonnes complexes.</li>
        </ul>
        """

    if lang == "de":
        return css + """
        <h2>🚀 1. Schnellstart (in 3 Schritten)</h2>
        <div class="box">
            <ol>
                <li><b>KI-Schlüssel konfigurieren (optional für Bing):</b>
                    Öffnen Sie <b>🔑 KI-Schlüssel & Anbieter</b> in der Seitenleiste, wählen Sie einen Anbieter (z. B. <b>DeepSeek</b>, <b>OpenAI</b>, <b>Gemini</b>, <b>Qwen-MT</b> oder lokal <b>Ollama</b>), geben Sie Ihren API-Schlüssel ein, klicken Sie auf <b>⚡ Verbindung testen</b> und <b>⭐ Als Standard festlegen</b>.
                </li>
                <li><b>PDF- / Word-Dateien hinzufügen:</b>
                    Ziehen Sie im <b>📄 Arbeitsbereich</b> <code>.pdf</code>- / <code>.docx</code>-Dateien oder Ordner per Drag & Drop in die Warteschlange oder fügen Sie über <b>＋ URL</b> einen Online-Link (z. B. arXiv) hinzu.
                </li>
                <li><b>Übersetzen & Vorschau:</b>
                    Wählen Sie Quell- und Zielsprache und klicken Sie auf <b>🚀 Übersetzen</b>. Wechseln Sie anschließend rechts zwischen <b>Original</b>, <b>Übersetzt (Mono)</b> und <b>Zweisprachig (Dual)</b>.
                </li>
            </ol>
        </div>
        <h2>⚡ 2. Layout-Engine-Modi im Vergleich</h2>
        <ul>
            <li><b><code>fast</code> (Standard — Empfohlen):</b> Nutzt DocLayout-YOLO zur präzisen Erkennung von Absätzen, Formeln <code>{v*}</code>, Inhaltsverzeichnissen und Programmcode.</li>
            <li><b><code>ultrafast</code> (Ultraschnell):</b> Überspringt neuronale Layout-Analyse und OCR und verarbeitet native PDF-Textströme direkt.</li>
            <li><b><code>babeldoc</code> (BabelDOC-Backend):</b> Erweiterte Layout-Pipeline für komplexe mehrspaltige Dokumente.</li>
        </ul>
        """

    if lang == "ru":
        return css + """
        <h2>🚀 1. Быстрый старт (3 шага)</h2>
        <div class="box">
            <ol>
                <li><b>Настройте API-ключ ИИ (необязательно для Bing):</b>
                    Откройте <b>🔑 Ключи ИИ и провайдеры</b> на боковой панели, выберите провайдера (<b>DeepSeek</b>, <b>OpenAI</b>, <b>Gemini</b>, <b>Qwen-MT</b> или локальный <b>Ollama</b>), введите ключ API, нажмите <b>⚡ Проверить соединение</b> и <b>⭐ Сделать по умолчанию</b>.
                </li>
                <li><b>Добавьте файлы PDF / Word:</b>
                    Перетащите файлы <code>.pdf</code> / <code>.docx</code> или папку в <b>📄 Рабочую область</b> либо нажмите <b>＋ URL</b> для перевода статьи по ссылке (например, arXiv).
                </li>
                <li><b>Перевод и предпросмотр:</b>
                    Выберите языки и нажмите <b>🚀 Начать перевод</b>. После завершения переключайтесь между режимами <b>Оригинал</b>, <b>Перевод (Mono)</b> и <b>Двуязычный (Dual)</b>.
                </li>
            </ol>
        </div>
        <h2>⚡ 2. Режимы движка вёрстки</h2>
        <ul>
            <li><b><code>fast</code> (Стандартный — Рекомендуется):</b> Использует нейросеть DocLayout-YOLO для сохранения математических формул <code>{v*}</code>, оглавления и блоков программного кода.</li>
            <li><b><code>ultrafast</code> (Ультрабыстрый):</b> Прямой разбор текстового потока PDF без нейросетевого анализа макета.</li>
            <li><b><code>babeldoc</code> (Бэкенд BabelDOC):</b> Расширенный движок для сложной многоколоночной вёрстки.</li>
        </ul>
        """

    if lang == "es":
        return css + """
        <h2>🚀 1. Inicio rápido (3 pasos)</h2>
        <div class="box">
            <ol>
                <li><b>Configurar clave de IA (opcional para Bing):</b>
                    Abra <b>🔑 Claves IA y Proveedores</b> en la barra lateral, elija su proveedor (<b>DeepSeek</b>, <b>OpenAI</b>, <b>Gemini</b>, <b>Qwen-MT</b> u <b>Ollama</b> local), introduzca su API Key, pulse <b>⚡ Probar conexión</b> y <b>⭐ Establecer por defecto</b>.
                </li>
                <li><b>Añadir documentos PDF / Word:</b>
                    En <b>📄 Espacio de trabajo</b>, arrastre y suelte archivos <code>.pdf</code> / <code>.docx</code> o carpetas, o pulse <b>＋ URL</b> para traducir un PDF en línea (como arXiv).
                </li>
                <li><b>Traducir y previsualizar:</b>
                    Seleccione los idiomas de origen y destino y pulse <b>🚀 Traducir</b>. Al finalizar, alterne entre <b>Original</b>, <b>Traducido (Mono)</b> y <b>Bilingüe (Dual)</b> en el visor derecho.
                </li>
            </ol>
        </div>
        <h2>⚡ 2. Modos de motor de maquetación</h2>
        <ul>
            <li><b><code>fast</code> (Estándar — Recomendado):</b> Usa DocLayout-YOLO para conservar fórmulas matemáticas <code>{v*}</code>, tablas de contenido y bloques de código.</li>
            <li><b><code>ultrafast</code> (Ultrarrápido):</b> Procesa directamente el flujo de texto PDF nativo sin modelo neuronal ni OCR.</li>
            <li><b><code>babeldoc</code> (Backend BabelDOC):</b> Motor avanzado para diseños multicolumna complejos.</li>
        </ul>
        """

    if lang == "it":
        return css + """
        <h2>🚀 1. Guida rapida (3 passaggi)</h2>
        <div class="box">
            <ol>
                <li><b>Configura la chiave IA (opzionale per Bing):</b>
                    Apri <b>🔑 Chiavi IA e Provider</b> nella barra laterale, seleziona un provider (<b>DeepSeek</b>, <b>OpenAI</b>, <b>Gemini</b>, <b>Qwen-MT</b> o <b>Ollama</b> locale), inserisci la tua API Key, clicca su <b>⚡ Testa connessione</b> e <b>⭐ Imposta come predefinito</b>.
                </li>
                <li><b>Aggiungi file PDF / Word:</b>
                    Nell'<b>📄 Area di lavoro</b>, trascina file <code>.pdf</code> / <code>.docx</code> o cartelle, oppure clicca su <b>＋ URL</b> per tradurre un PDF online (es. arXiv).
                </li>
                <li><b>Traduci e visualizza l'anteprima:</b>
                    Scegli le lingue di origine/destinazione e clicca su <b>🚀 Traduci</b>. Al termine, passa tra <b>Originale</b>, <b>Tradotto (Mono)</b> e <b>Bilingue (Dual)</b> nel pannello di destra.
                </li>
            </ol>
        </div>
        <h2>⚡ 2. Confronto modalità motore di layout</h2>
        <ul>
            <li><b><code>fast</code> (Standard — Consigliato):</b> Usa DocLayout-YOLO per preservare formule matematiche <code>{v*}</code>, indice (TOC) e blocchi di codice.</li>
            <li><b><code>ultrafast</code> (Ultraveloce):</b> Analizza direttamente il flusso di testo PDF nativo senza analisi neurale né OCR.</li>
            <li><b><code>babeldoc</code> (Backend BabelDOC):</b> Motore avanzato per layout multicolonna complessi.</li>
        </ul>
        """

    # Default: Simplified Chinese ("zh")
    return css + """
    <h2>🚀 一、快速上手（三步完成论文翻译）</h2>
    <div class="box">
        <ol>
            <li><b>第一步：配置 AI 密钥（如使用必应 Bing 可直接跳过）</b><br>
                点击左侧导航栏的 <b>「🔑 AI 密钥与服务商」</b>，在列表中选择您常用的服务商（推荐 <b>DeepSeek</b>、<b>OpenAI</b>、<b>Gemini</b>、<b>阿里云百炼 Ali Qwen-Translation</b>、<b>硅基流动 Silicon</b> 或本地免费的 <b>Ollama</b>）。<br>
                填入 API Key 后点击 <b>「⚡ 测试连接」</b>，验证成功后点击 <b>「⭐ 设为默认翻译服务」</b>。
            </li>
            <li><b>第二步：添加 PDF / Word 文档</b><br>
                切回 <b>「📄 翻译工作台」</b>，直接将一个或多个 <code>.pdf</code> / <code>.doc</code> / <code>.docx</code> 文件或整个文件夹拖入左侧列表；也可以点击 <b>「＋ 链接」</b> 直接输入在线 PDF 地址（例如 arXiv 论文链接）。
            </li>
            <li><b>第三步：开始翻译与双语对照预览</b><br>
                确认源语言与目标语言后，点击 <b>「🚀 开始翻译」</b>。翻译完成后，右侧内置高清阅读器会自动加载结果，您可以随时在顶部切换查看 <b>「原文」</b>、<b>「纯译文 (Mono)」</b> 和 <b>「双语对照 (Dual)」</b>，也可以点击「外部打开」调用系统默认阅读器查看。
            </li>
        </ol>
    </div>

    <h2>🔑 二、主流 AI 翻译服务商配置指南</h2>
    <table>
        <tr>
            <th>服务商名称</th>
            <th>推荐模型 (Model)</th>
            <th>适用场景与配置说明</th>
        </tr>
        <tr>
            <td><b>DeepSeek</b></td>
            <td><code>deepseek-chat</code></td>
            <td>国内直连、价格极低、中英科技论文翻译准确流畅，强烈推荐。</td>
        </tr>
        <tr>
            <td><b>Ali Qwen-Translation</b></td>
            <td><code>qwen-mt-turbo</code> / <code>qwen-mt-plus</code></td>
            <td>阿里云百炼专为学术与多语种翻译优化的垂类模型，自带科技论文领域提示。</td>
        </tr>
        <tr>
            <td><b>Silicon (硅基流动) / 智谱 GLM</b></td>
            <td><code>Qwen/Qwen2.5-7B-Instruct</code> / <code>glm-4-flash</code></td>
            <td>提供免费额度或高性价比推理接口，适合大批量文献快速翻译。</td>
        </tr>
        <tr>
            <td><b>OpenAI-liked (自定义兼容接口)</b></td>
            <td>任意兼容模型名</td>
            <td>支持所有兼容 OpenAI 协议的第三方 API 中转站、OneAPI、NewAPI、vLLM、LM Studio 等，只需填写 Base URL、API Key 和模型名称。</td>
        </tr>
        <tr>
            <td><b>Ollama (本地大模型)</b></td>
            <td><code>qwen2.5:7b</code> / <code>gemma2</code></td>
            <td>完全本地离线运行，无需 API Key，零费用且保障涉密/未发表论文的数据隐私。</td>
        </tr>
        <tr>
            <td><b>Bing / Google</b></td>
            <td>无需选择模型</td>
            <td>传统网页机器翻译，<b>免配置 API Key</b>，开箱即用（Google 需开启网络代理）。</td>
        </tr>
    </table>

    <h2>⚡ 三、四大排版引擎模式对比</h2>
    <ul>
        <li><b><code>fast</code> — 标准模式（推荐默认）：</b>使用 DocLayout-YOLO 视觉布局模型精准识别正文段落、行内/独立数学公式、图片、表格与页眉页脚，原样保留公式与排版。</li>
        <li><b><code>ultrafast</code> — 极速无模型模式：</b>跳过神经网络视觉分析与 OCR，直接通过原生 PDF 指令流提取文本（需安装 <code>pdf-inspector</code>，未安装时自动回退至 <code>fast</code>），速度极快。</li>
        <li><b><code>babeldoc</code> — BabelDOC 增强排版后端：</b>采用实验性 BabelDOC 渲染管线，对复杂多栏样式及富文本加粗/斜体还原更佳。</li>
        <li><b><code>precise</code> — Precise v2 精准模式：</b>调用隔离的 <code>pdf2zh_next</code> 核心（需先运行 <code>pdf2zh-setup-precise</code> 初始化环境）。</li>
    </ul>

    <h2>📐 四、公式保护、自定义提示词与常见问题 (FAQ)</h2>
    <div class="tip">
        <b>💡 公式保护原理：</b>程序在调用大模型前会将数学公式替换为 <code>{v0}</code>、<code>{v1}</code> 等占位符，翻译完成后再将原公式精准回填。如果遇到特殊排版的 PDF 中个别符号被误翻译，可前往 <b>「⚙️ 翻译与排版设置」</b> 点击 <b>「填入 LaTeX 常用数学字体正则」</b>。
    </div>
    <ul>
        <li><b>如何自定义专业领域翻译风格？</b><br>
            在 <b>「⚙️ 翻译与排版设置」</b> 中勾选「启用自定义大模型翻译提示词」，可在提示词中补充您的学科背景要求（请务必保留模板中的 <code>${lang_out}</code> 和 <code>${text}</code> 变量）。
        </li>
        <li><b>遇到 429 Rate Limit（请求过于频繁）报错怎么办？</b><br>
            前往 <b>「📁 输出与任务设置」</b>，将「默认并发线程数 (-t)」从 <code>4</code> 调低至 <code>1</code> 或 <code>2</code>。
        </li>
        <li><b>扫描版 PDF（纯图片无文字层）可以翻译吗？</b><br>
            可以！在标准 <code>fast</code> 模式下会自动检测纯图片页并调用 PyMuPDF + Tesseract 进行 OCR 识别（可在「⚙️ 翻译与排版设置」中配置 OCR 语言代码与 <code>TESSDATA</code> 目录）。
        </li>
        <li><b>修改了提示词或更换了模型，为什么翻译结果没变？</b><br>
            因为默认开启了 SQLite 段落级翻译缓存以节省 Token。您可以在工作台勾选 <b>「忽略缓存」</b>，或在 <b>「🛠️ 系统与高级设置」</b> 中点击 <b>「🧹 一键清空翻译缓存」</b>。
        </li>
    </ul>
    """

