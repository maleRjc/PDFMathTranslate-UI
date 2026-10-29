"""Background QThread workers for PDF translation and AI provider connection testing."""

from __future__ import annotations

import asyncio
import logging
import os
import shutil
import time
import traceback
from asyncio import CancelledError
from pathlib import Path
from string import Template
from typing import Any, Optional

from PySide6.QtCore import QThread, Signal

from pdf2zh.config import ConfigManager
from pdf2zh.desktop.metadata import (
     SERVICE_MAP,
    AppSettings,
    get_provider_envs,
)

logger = logging.getLogger(__name__)


def parse_page_range_string(page_str: str) -> Optional[list[int]]:
    """Parse user page specification like '1-3, 5, 8-10' into 0-based page list."""
    s = (page_str or "").strip()
    if not s:
        return None
    pages: list[int] = []
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = max(1, int(start_s.strip()))
            end = max(start, int(end_s.strip()))
            pages.extend(range(start - 1, end))
        else:
            p = max(1, int(part))
            pages.append(p - 1)
    return sorted(set(pages))


class QtLogHandler(logging.Handler):
    """Forwards Python logging records to a Qt signal."""

    def __init__(self, signal_Callback):
        super().__init__()
        self._callback = signal_Callback

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self._callback(msg)
        except Exception:
            pass


class ConnectionTestWorker(QThread):
    """Tests an AI / translation provider in the background."""

    result_ready = Signal(bool, str)

    def __init__(
        self,
        service_key: str,
        envs: dict[str, str],
        parent=None,
    ):
        super().__init__(parent)
        self.service_key = service_key
        self.envs = envs

    def run(self) -> None:
        AppSettings.apply_runtime_settings()
        t0 = time.perf_counter()
        try:
            translator_cls = SERVICE_MAP[self.service_key]
            clean_envs = {
                k: (v.strip() if v and v.strip() != "" else None)
                for k, v in self.envs.items()
            }
            # Determine model parameter if present
            model = ""
            for k, v in clean_envs.items():
                if k.upper().endswith("MODEL") and v:
                    model = v
                    break

            translator = translator_cls(
                "en",
                "zh",
                model,
                envs=clean_envs,
                ignore_cache=True,
            )
            sample = "Artificial intelligence is transforming scientific research."
            translated = translator.do_translate(sample)
            elapsed_ms = int((time.perf_counter() - t0) * 1000)
            if not translated or not str(translated).strip():
                self.result_ready.emit(
                    False, f"接口返回为空（耗时 {elapsed_ms} ms），请检查模型名称或配置。"
                )
                return
            self.result_ready.emit(
                True,
                f"连接成功 ({elapsed_ms} ms)\n测试原文: {sample}\n测试译文: {translated.strip()}",
            )
        except Exception as exc:
            elapsed_ms = int((time.perf_counter() - t0) * 1000)
            self.result_ready.emit(
                False,
                f"连接测试失败 ({elapsed_ms} ms): {exc}",
            )


class TranslationQueueWorker(QThread):
    """Executes a batch of PDF translation tasks sequentially in a background thread."""

    task_started = Signal(int, str)  # row_index, file_path
    task_progress = Signal(int, int, str)  # row_index, percent (0-100), desc
    task_finished = Signal(
        int, str, str, float
    )  # row_index, mono_path, dual_path, seconds
    task_failed = Signal(int, str)  # row_index, error_message
    log_message = Signal(str)
    queue_finished = Signal()

    def __init__(
        self,
        tasks: list[dict[str, Any]],
        options: dict[str, Any],
        parent=None,
    ):
        super().__init__(parent)
        self.tasks = tasks
        self.options = options
        self._cancel_event = asyncio.Event()
        self._is_cancelled = False

    def cancel(self) -> None:
        self._is_cancelled = True
        self._cancel_event.set()

    def _emit_log(self, text: str) -> None:
        self.log_message.emit(text)

    def _ensure_layout_model(self, mode: str) -> None:
        if mode == "ultrafast":
            return
        from pdf2zh.doclayout import ModelInstance, OnnxModel, set_backend

        backend = str(AppSettings.get("PDF2ZH_ONNX_BACKEND") or "auto")
        set_backend(backend)
        custom_onnx = str(AppSettings.get("PDF2ZH_ONNX_MODEL_PATH") or "").strip()
        if custom_onnx and os.path.exists(custom_onnx):
            if (
                ModelInstance.value is None
                or getattr(ModelInstance.value, "model_path", None) != custom_onnx
            ):
                self._emit_log(f"正在加载自定义 ONNX 布局模型: {custom_onnx}")
                ModelInstance.value = OnnxModel(custom_onnx)
        else:
            if ModelInstance.value is None:
                self._emit_log("正在加载 DocLayout-YOLO 布局分析模型...")
                ModelInstance.value = OnnxModel.load_available()

    def run(self) -> None:
        AppSettings.apply_runtime_settings()

        log_handler = QtLogHandler(self._emit_log)
        log_handler.setFormatter(
            logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%H:%M:%S")
        )
        root_logger = logging.getLogger("pdf2zh")
        root_logger.addHandler(log_handler)

        try:
            service_key = self.options["service_key"]
            translator_cls = SERVICE_MAP[service_key]
            envs = get_provider_envs(service_key)
            # Allow workspace model override
            model_override = (self.options.get("model_override") or "").strip()
            if model_override:
                for k in envs:
                    if k.upper().endswith("MODEL"):
                        envs[k] = model_override
                ConfigManager.set_translator_by_name(translator_cls.name, envs)

            lang_in = self.options["lang_in"]
            lang_out = self.options["lang_out"]
            mode = self.options["mode"]  # fast, ultrafast, precise, babeldoc
            pages = self.options.get("pages")  # list[int] or None
            raw_pages_str = self.options.get("raw_pages_str") or ""
            threads = int(self.options.get("threads") or 4)
            vfont = self.options.get("vfont") or ""
            vchar = self.options.get("vchar") or ""
            prompt_str = self.options.get("prompt") or ""
            skip_subset_fonts = bool(self.options.get("skip_subset_fonts"))
            ignore_cache = bool(self.options.get("ignore_cache"))
            compatible = bool(self.options.get("compatible"))
            gen_mono = bool(self.options.get("gen_mono", True))
            gen_dual = bool(self.options.get("gen_dual", True))

            if mode == "ultrafast":
                try:
                    import pdf_inspector  # noqa: F401
                except ImportError:
                    self._emit_log(
                        "提示: 当前环境未安装 pdf-inspector，自动从 ultrafast 回退至 fast 标准模式。"
                    )
                    mode = "fast"

            self._ensure_layout_model(mode)

            for task in self.tasks:
                if self._is_cancelled:
                    break
                row_idx = task["row"]
                source_path = task["path"]
                self.task_started.emit(row_idx, source_path)
                t_start = time.perf_counter()

                try:
                    # Determine output folder
                    output_dir_opt = (self.options.get("output_dir") or "").strip()
                    save_next_to_source = bool(
                        self.options.get("save_next_to_source", True)
                    )
                    if (
                        not save_next_to_source
                        and output_dir_opt
                        and not source_path.startswith(("http://", "https://"))
                    ):
                        out_dir = Path(output_dir_opt)
                    elif not source_path.startswith(("http://", "https://")):
                        if output_dir_opt and not save_next_to_source:
                            out_dir = Path(output_dir_opt)
                        else:
                            out_dir = Path(source_path).resolve().parent
                    else:
                        out_dir = (
                            Path(output_dir_opt)
                            if output_dir_opt
                            else (Path.cwd() / "pdf2zh_files")
                        )
                    out_dir.mkdir(parents=True, exist_ok=True)

                    self._emit_log(
                        f"开始翻译 [{Path(source_path).name}] -> 服务: {service_key} ({translator_cls.name}), 模式: {mode}, 输出目录: {out_dir}"
                    )

                    def on_progress(t_bar):
                        if self._is_cancelled:
                            raise CancelledError("Translation cancelled by user")
                        total = getattr(t_bar, "total", 0) or 1
                        current = getattr(t_bar, "n", 0) or 0
                        pct = min(99, max(1, int(current * 100 / total)))
                        desc = getattr(t_bar, "desc", "") or f"正在翻译 ({current}/{total})"
                        self.task_progress.emit(row_idx, pct, desc)

                    if mode == "babeldoc":
                        mono_file, dual_file = self._run_babeldoc(
                            source_path=source_path,
                            out_dir=out_dir,
                            translator_cls=translator_cls,
                            envs=envs,
                            lang_in=lang_in,
                            lang_out=lang_out,
                            raw_pages_str=raw_pages_str,
                            threads=threads,
                            prompt_str=prompt_str,
                            skip_subset_fonts=skip_subset_fonts,
                            ignore_cache=ignore_cache,
                            gen_mono=gen_mono,
                            gen_dual=gen_dual,
                            row_idx=row_idx,
                        )
                    else:
                        from pdf2zh.kernel import KernelRegistry
                        from pdf2zh.kernel.protocol import TranslateRequest

                        kernel_mode = "precise" if mode == "precise" else "fast"
                        KernelRegistry.switch(kernel_mode)
                        kernel = KernelRegistry.get()
                        if kernel_mode == "precise" and not kernel.is_available():
                            self._emit_log(
                                "提示: precise (v2) 虚拟环境未初始化，自动回退至 fast 模式。"
                            )
                            KernelRegistry.switch("fast")
                            kernel = KernelRegistry.get()

                        service_spec = translator_cls.name
                        if model_override:
                            service_spec = f"{translator_cls.name}:{model_override}"

                        req = TranslateRequest(
                            files=[source_path],
                            output=str(out_dir),
                            pages=pages,
                            lang_in=lang_in,
                            lang_out=lang_out,
                            service=service_spec,
                            thread=threads,
                            vfont=vfont,
                            vchar=vchar,
                            envs=envs,
                            prompt=prompt_str if prompt_str else None,
                            skip_subset_fonts=skip_subset_fonts,
                            ignore_cache=ignore_cache,
                            compatible=compatible,
                            ultrafast=(mode == "ultrafast"),
                        )
                        results = kernel.translate(
                            req,
                            callback=on_progress,
                            cancellation_event=self._cancel_event,
                        )
                        if results and len(results) > 0:
                            mono_file = (
                                str(results[0].mono_pdf) if results[0].mono_pdf else ""
                            )
                            dual_file = (
                                str(results[0].dual_pdf) if results[0].dual_pdf else ""
                            )
                        else:
                            stem = os.path.splitext(os.path.basename(source_path))[0]
                            mono_file = str(out_dir / f"{stem}-mono.pdf")
                            dual_file = str(out_dir / f"{stem}-dual.pdf")

                        # Apply mono/dual retention preferences
                        if not gen_mono and gen_dual and os.path.exists(mono_file):
                            try:
                                os.unlink(mono_file)
                                mono_file = ""
                            except OSError:
                                pass
                        elif not gen_dual and gen_mono and os.path.exists(dual_file):
                            try:
                                os.unlink(dual_file)
                                dual_file = ""
                            except OSError:
                                pass

                    elapsed = time.perf_counter() - t_start
                    self.task_progress.emit(row_idx, 100, "翻译完成")
                    self._emit_log(
                        f"已完成 [{Path(source_path).name}] (耗时 {elapsed:.1f}s)"
                    )
                    self.task_finished.emit(row_idx, mono_file, dual_file, elapsed)

                except CancelledError:
                    self._emit_log(f"任务已取消: {Path(source_path).name}")
                    self.task_failed.emit(row_idx, "已取消")
                    break
                except Exception as exc:
                    err_detail = traceback.format_exc()
                    self._emit_log(f"翻译失败 [{Path(source_path).name}]: {exc}\n{err_detail}")
                    self.task_failed.emit(row_idx, str(exc))

        finally:
            root_logger.removeHandler(log_handler)
            self.queue_finished.emit()

    def _run_babeldoc(
        self,
        source_path: str,
        out_dir: Path,
        translator_cls,
        envs: dict[str, Any],
        lang_in: str,
        lang_out: str,
        raw_pages_str: str,
        threads: int,
        prompt_str: str,
        skip_subset_fonts: bool,
        ignore_cache: bool,
        gen_mono: bool,
        gen_dual: bool,
        row_idx: int,
    ) -> tuple[str, str]:
        from babeldoc.high_level import async_translate as babeldoc_translate
        from babeldoc.high_level import init as babeldoc_init
        from babeldoc.main import create_progress_handler
        from babeldoc.translation_config import TranslationConfig as YadtConfig
        from pdf2zh.converter_docx import convert_to_pdf, is_convertible
        from pdf2zh.high_level import download_remote_fonts
        from pdf2zh.translator import OpenAITranslator

        babeldoc_init()
        font_path = download_remote_fonts(lang_out.lower())

        model = ""
        for k, v in envs.items():
            if k.upper().endswith("MODEL") and v:
                model = v
                break

        prompt_tmpl = Template(prompt_str) if prompt_str else None
        translator = translator_cls(
            lang_in,
            lang_out,
            model,
            envs=envs,
            prompt=prompt_tmpl,
            ignore_cache=ignore_cache,
        )

        actual_file = source_path
        converted_pdf = None
        if is_convertible(actual_file):
            converted_pdf = convert_to_pdf(actual_file)
            actual_file = converted_pdf

        yadt_config = YadtConfig(
            input_file=actual_file,
            font=font_path,
            pages=raw_pages_str,
            output_dir=str(out_dir),
            doc_layout_model=None,
            translator=translator,
            debug=False,
            lang_in=lang_in,
            lang_out=lang_out,
            no_dual=not gen_dual,
            no_mono=not gen_mono,
            qps=threads,
            use_rich_pbar=False,
            disable_rich_text_translate=not isinstance(translator, OpenAITranslator),
            skip_clean=skip_subset_fonts,
            report_interval=0.4,
        )

        mono_res = ""
        dual_res = ""

        async def _coro():
            nonlocal mono_res, dual_res
            progress_context, progress_handler = create_progress_handler(yadt_config)
            with progress_context:
                async for event in babeldoc_translate(yadt_config):
                    progress_handler(event)
                    if self._cancel_event.is_set():
                        yadt_config.cancel_translation()
                        raise CancelledError("Cancelled")
                    pct = int(event.get("overall_progress", 0))
                    stage = event.get("stage", "BabelDOC 翻译中...")
                    self.task_progress.emit(row_idx, min(99, max(1, pct)), str(stage))
                    if event.get("type") == "finish":
                        result = event["translate_result"]
                        mono_res = str(result.mono_pdf_path or "")
                        dual_res = str(result.dual_pdf_path or "")
                        break

        try:
            asyncio.run(_coro())
        finally:
            if converted_pdf:
                try:
                    os.unlink(converted_pdf)
                except OSError:
                    pass

        return mono_res, dual_res

