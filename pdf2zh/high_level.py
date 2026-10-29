"""Functions that can be used for the most common use-cases for pdf2zh.six"""

from __future__ import annotations

import asyncio
import io
import os
import re
import sys
import tempfile
import logging
from time import perf_counter
from asyncio import CancelledError
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import nullcontext
from pathlib import Path
from string import Template
from typing import Any, BinaryIO, List, Optional, Dict, TYPE_CHECKING

import numpy as np
import requests
import tqdm

from pdf2zh.converter_docx import convert_to_pdf, is_convertible
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfexceptions import PDFValueError
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pymupdf import Document, Font

from pdf2zh.converter import TranslateConverter

if TYPE_CHECKING:
    from pdf2zh.doclayout import OnnxModel
from pdf2zh.pdfinterp import PDFPageInterpreterEx

from pdf2zh.config import ConfigManager

NOTO_NAME = "noto"
PROMO_URL = "https://www.aireadcode.com"

PROMO_TEXT_MAP: dict[str, str] = {
    "zh": "AI 帮你写代码，AiReadCode 帮你读懂代码。https://www.aireadcode.com",
    "zh-cn": "AI 帮你写代码，AiReadCode 帮你读懂代码。https://www.aireadcode.com",
    "zh-hans": "AI 帮你写代码，AiReadCode 帮你读懂代码。https://www.aireadcode.com",
    "zh-sg": "AI 帮你写代码，AiReadCode 帮你读懂代码。https://www.aireadcode.com",
    "zh-tw": "AI 幫你寫程式碼，AiReadCode 幫你讀懂程式碼。https://www.aireadcode.com",
    "zh-hant": "AI 幫你寫程式碼，AiReadCode 幫你讀懂程式碼。https://www.aireadcode.com",
    "zh-hk": "AI 幫你寫程式碼，AiReadCode 幫你讀懂程式碼。https://www.aireadcode.com",
    "en": "AI writes code for you, AiReadCode helps you understand it. https://www.aireadcode.com",
    "ja": "AI がコードを書き、AiReadCode がコードの理解を助けます。https://www.aireadcode.com",
    "ko": "AI가 코드를 작성하고, AiReadCode가 코드 이해를 도와줍니다. https://www.aireadcode.com",
    "fr": "L'IA écrit le code pour vous, AiReadCode vous aide à le comprendre. https://www.aireadcode.com",
    "de": "KI schreibt den Code für Sie, AiReadCode hilft Ihnen, ihn zu verstehen. https://www.aireadcode.com",
    "ru": "ИИ пишет код за вас, AiReadCode помогает его понять. https://www.aireadcode.com",
    "es": "La IA escribe el código por ti, AiReadCode te ayuda a entenderlo. https://www.aireadcode.com",
    "it": "L'IA scrive il codice per te, AiReadCode ti aiuta a capirlo. https://www.aireadcode.com",
    "pt": "A IA escreve o código para você, o AiReadCode ajuda você a entendê-lo. https://www.aireadcode.com",
    "ar": "الذكاء الاصطناعي يكتب الكود لك، و AiReadCode يساعدك على فهمه. https://www.aireadcode.com",
}


def get_promo_text(lang_out: str) -> str:
    """Return the localized AiReadCode promotional footer text for target language."""
    code = (lang_out or "zh").strip().lower().replace("_", "-")
    if code in PROMO_TEXT_MAP:
        return PROMO_TEXT_MAP[code]
    if code.startswith("zh"):
        if any(tag in code for tag in ("tw", "hant", "hk", "mo")):
            return PROMO_TEXT_MAP["zh-tw"]
        return PROMO_TEXT_MAP["zh"]
    prefix = code.split("-", 1)[0]
    if prefix in PROMO_TEXT_MAP:
        return PROMO_TEXT_MAP[prefix]
    return PROMO_TEXT_MAP["zh"]


def _build_promo_ops(
    page,
    noto: Font,
    noto_name: str,
    lang_out: str,
) -> tuple[str, tuple[float, float, float, float]]:
    """Build PDF content stream operators and rect (in PyMuPDF top-down coords) for the promo footer."""
    text = get_promo_text(lang_out)
    # If font lacks non-ASCII glyphs (e.g. Latin-only test font), fall back to English promo text
    if any(ord(c) > 127 and not noto.has_glyph(ord(c)) for c in text):
        text = PROMO_TEXT_MAP["en"]

    cbox = page.cropbox
    page_w = float(cbox.width)
    page_h = float(cbox.height)
    x0_box = float(cbox.x0)
    y0_box = float(cbox.y0)

    fontsize = 8.5

    def _measure(sz: float) -> float:
        total = 0.0
        for ch in text:
            if noto.has_glyph(ord(ch)):
                total += noto.char_lengths(ch, sz)[0]
            else:
                total += sz * 0.5
        return total

    est_w = _measure(fontsize)
    avail_w = max(80.0, page_w - 24.0)
    if est_w > avail_w and est_w > 0:
        fontsize = max(5.5, fontsize * (avail_w / est_w) * 0.96)
        est_w = _measure(fontsize)

    start_x = x0_box + max(12.0, (page_w - est_w) / 2.0)
    y_pdf = y0_box + 9.0

    ops_parts: list[str] = []
    cur_font: Optional[str] = None
    cur_hex: list[str] = []
    run_x = start_x
    cur_x = start_x

    def _flush() -> None:
        nonlocal cur_hex
        if cur_hex and cur_font:
            rtxt = "".join(cur_hex)
            ops_parts.append(
                f"/{cur_font} {fontsize:f} Tf 1 0 0 1 {run_x:f} {y_pdf:f} Tm [<{rtxt}>] TJ "
            )
            cur_hex = []

    for ch in text:
        gid = noto.has_glyph(ord(ch))
        if gid:
            f_use = noto_name
            h_val = "%04x" % gid
            adv = noto.char_lengths(ch, fontsize)[0]
        else:
            f_use = "tiro"
            c_ord = ord(ch) if ord(ch) < 256 else ord("?")
            h_val = "%02x" % c_ord
            adv = fontsize * 0.5
        if f_use != cur_font:
            _flush()
            cur_font = f_use
            run_x = cur_x
        cur_hex.append(h_val)
        cur_x += adv
    _flush()

    ops_str = f"q 0.15 0.39 0.92 rg BT {''.join(ops_parts)}ET Q "
    # PyMuPDF top-down rectangle for clickable URI link
    link_rect = (
        start_x,
        page_h - (y_pdf - y0_box) - fontsize - 2.0,
        cur_x,
        page_h - (y_pdf - y0_box) + 3.0,
    )
    return ops_str, link_rect


def append_promo_to_pdf_file(
    pdf_path: str,
    lang_out: str,
    font_path: str = "",
) -> None:
    """Append the localized AiReadCode promotional footer to the last page of a PDF file on disk."""
    if not pdf_path or not os.path.exists(pdf_path):
        return
    try:
        import pymupdf as _fitz

        if not font_path or not os.path.exists(font_path):
            font_path = download_remote_fonts((lang_out or "zh").lower())
        text = get_promo_text(lang_out)
        with _fitz.open(pdf_path) as doc:
            if len(doc) == 0:
                return
            page = doc[-1]
            font = Font(NOTO_NAME, font_path)
            page.insert_font(fontname=NOTO_NAME, fontfile=font_path)
            fontsize = 8.5
            tw = font.text_length(text, fontsize=fontsize)
            avail_w = max(80.0, float(page.rect.width) - 24.0)
            if tw > avail_w and tw > 0:
                fontsize = max(5.5, fontsize * (avail_w / tw) * 0.96)
                tw = font.text_length(text, fontsize=fontsize)
            x = float(page.rect.x0) + max(12.0, (float(page.rect.width) - tw) / 2.0)
            y = float(page.rect.y1) - 10.0
            page.insert_text(
                (x, y),
                text,
                fontsize=fontsize,
                fontname=NOTO_NAME,
                color=(0.15, 0.39, 0.92),
            )
            page.insert_link(
                {
                    "kind": _fitz.LINK_URI,
                    "from": _fitz.Rect(x, y - fontsize - 2.0, x + tw, y + 3.0),
                    "uri": PROMO_URL,
                }
            )
            try:
                doc.subset_fonts(fallback=True)
            except Exception:
                pass
            tmp_out = f"{pdf_path}.promo.tmp"
            doc.save(tmp_out, deflate=True, garbage=3)
        os.replace(tmp_out, pdf_path)
    except Exception as exc:
        logger.debug("append_promo_to_pdf_file skipped: %s", exc)



logger = logging.getLogger(__name__)

noto_list = [
    "am",  # Amharic
    "ar",  # Arabic
    "bn",  # Bengali
    "bg",  # Bulgarian
    "chr",  # Cherokee
    "el",  # Greek
    "gu",  # Gujarati
    "iw",  # Hebrew
    "hi",  # Hindi
    "kn",  # Kannada
    "ml",  # Malayalam
    "mr",  # Marathi
    "ru",  # Russian
    "sr",  # Serbian
    "ta",  # Tamil
    "te",  # Telugu
    "th",  # Thai
    "ur",  # Urdu
    "uk",  # Ukrainian
]


def check_files(files: List[str]) -> List[str]:
    files = [
        f for f in files if not f.startswith("http://")
    ]  # exclude online files, http
    files = [
        f for f in files if not f.startswith("https://")
    ]  # exclude online files, https
    missing_files = [file for file in files if not os.path.exists(file)]
    return missing_files


def translate_patch(
    inf: BinaryIO,
    pages: Optional[list[int]] = None,
    vfont: str = "",
    vchar: str = "",
    thread: int = 0,
    doc_zh: Document = None,
    lang_in: str = "",
    lang_out: str = "",
    service: str = "",
    noto_name: str = "",
    noto: Font = None,
    callback: object = None,
    cancellation_event: asyncio.Event = None,
    model: OnnxModel = None,
    envs: Dict = None,
    prompt: Template = None,
    ignore_cache: bool = False,
    ocr_pages: Optional[set[int]] = None,
    ultrafast: bool = False,
    perf=None,
    text_items=None,
    **kwarg: Any,
) -> None:
    if ultrafast and not thread:
        thread = 16
    rsrcmgr = PDFResourceManager()
    layout = {}
    device = TranslateConverter(
        rsrcmgr,
        vfont,
        vchar,
        thread,
        layout,
        lang_in,
        lang_out,
        service,
        noto_name,
        noto,
        envs,
        prompt,
        ignore_cache,
    )

    assert device is not None
    device.perf = perf
    device.translator.no_cache = ultrafast and ignore_cache
    obj_patch = {}
    interpreter = PDFPageInterpreterEx(rsrcmgr, device, obj_patch)
    if pages:
        total_pages = len(pages)
    else:
        total_pages = doc_zh.page_count

    parser = PDFParser(inf)
    doc = PDFDocument(parser)
    if ultrafast:
        from pdf2zh.ultrafast import extract_layout, layout_mask

        if text_items is None:
            inf.seek(0)
            started = perf_counter()
            text_items = extract_layout(inf.read(), pages)
            if perf:
                perf.add("layout_extract", perf_counter() - started)
            inf.seek(0)
    pending_pages = []
    with (
        tqdm.tqdm(total=total_pages) as progress,
        ThreadPoolExecutor(max_workers=thread) if ultrafast else nullcontext() as pool,
    ):
        if ultrafast:
            device.translation_pool = pool
            device.translation_futures = deque()
        for pageno, page in enumerate(PDFPage.create_pages(doc)):
            if cancellation_event and cancellation_event.is_set():
                raise CancelledError("task cancelled")
            if pages and (pageno not in pages):
                continue
            progress.update()
            if callback:
                callback(progress)
            page.pageno = pageno
            page_started = perf_counter() if perf else 0
            if ultrafast:
                if not text_items.get(pageno):
                    logger.info(
                        "[ultrafast perf] page_scan %d: skipped (no native text)",
                        pageno + 1,
                    )
                    continue
                # Inspector coordinates ignore /Rotate; keep content in that frame.
                # The output page retains its original rotation metadata.
                page.rotate = 0
                started = perf_counter()
                layout[page.pageno] = layout_mask(page, text_items.get(pageno, []))
                if perf:
                    perf.add("layout_mask", perf_counter() - started)
            else:
                pix = doc_zh[page.pageno].get_pixmap()
                image = np.frombuffer(pix.samples, np.uint8).reshape(
                    pix.height, pix.width, 3
                )[:, :, ::-1]
                page_layout = model.predict(image, imgsz=int(pix.height / 32) * 32)[0]
                if ocr_pages and pageno in ocr_pages:
                    from pdf2zh.ocr import translate_ocr_page

                    translate_ocr_page(
                        doc_zh[pageno],
                        page_layout,
                        device.translator,
                        noto,
                        thread,
                        cancellation_event,
                    )
                    continue
                # kdtree 是不可能 kdtree 的，不如直接渲染成图片，用空间换时间
                box = np.ones((pix.height, pix.width))
                h, w = box.shape
                vcls = [
                    "abandon",
                    "figure",
                    "table",
                    "isolate_formula",
                    "formula_caption",
                ]
                for i, d in enumerate(page_layout.boxes):
                    if page_layout.names[int(d.cls)] not in vcls:
                        x0, y0, x1, y1 = d.xyxy.squeeze()
                        x0, y0, x1, y1 = (
                            np.clip(int(x0 - 1), 0, w - 1),
                            np.clip(int(h - y1 - 1), 0, h - 1),
                            np.clip(int(x1 + 1), 0, w - 1),
                            np.clip(int(h - y0 + 1), 0, h - 1),
                        )
                        box[y0:y1, x0:x1] = i + 2
                for i, d in enumerate(page_layout.boxes):
                    if page_layout.names[int(d.cls)] in vcls:
                        x0, y0, x1, y1 = d.xyxy.squeeze()
                        x0, y0, x1, y1 = (
                            np.clip(int(x0 - 1), 0, w - 1),
                            np.clip(int(h - y1 - 1), 0, h - 1),
                            np.clip(int(x1 + 1), 0, w - 1),
                            np.clip(int(h - y0 + 1), 0, h - 1),
                        )
                        box[y0:y1, x0:x1] = 0
                layout[page.pageno] = box
            # 新建一个 xref 存放新指令流
            page.page_xref = doc_zh.get_new_xref()  # hack 插入页面的新 xref
            doc_zh.update_object(page.page_xref, "<<>>")
            doc_zh.update_stream(page.page_xref, b"")
            doc_zh[page.pageno].set_contents(page.page_xref)
            interpreter.process_page(page)
            if ultrafast:
                pending_pages.append(page)
            if perf:
                logger.info(
                    "[ultrafast perf] page_scan %d: %.3fs",
                    pageno + 1,
                    perf_counter() - page_started,
                )
        if ultrafast:
            logger.info(
                "[ultrafast perf] document pool: %d tasks, %d workers",
                len(device.translation_futures),
                thread,
            )
            started = perf_counter()
            progress.reset(total=len(device.translation_futures))
            progress.set_description("Translate paragraphs")
            for future in as_completed(device.translation_futures):
                future.result()  # Surface failures before the interpreter's form guards.
                if cancellation_event and cancellation_event.is_set():
                    raise CancelledError("task cancelled")
                progress.update()
                if callback:
                    callback(progress)
            if perf:
                perf.add("translation", perf_counter() - started)
            device.translation_pool = None
            # ponytail: replay the cheap parser to retain per-page/form font state.
            # A stored paragraph plan is only worthwhile if parsing becomes costly.
            progress.reset(total=len(pending_pages))
            progress.set_description("Typeset pages")
            for page in pending_pages:
                if cancellation_event and cancellation_event.is_set():
                    raise CancelledError("task cancelled")
                started = perf_counter()
                interpreter.process_page(page)
                progress.update()
                if callback:
                    callback(progress)
                if perf:
                    logger.info(
                        "[ultrafast perf] page_render %d: %.3fs",
                        page.pageno + 1,
                        perf_counter() - started,
                    )
            assert not device.translation_futures

    device.close()
    return obj_patch


def _ocr_tessdata(language):
    """Use explicit local data, or download requested languages once on demand."""
    if not re.fullmatch(r"[A-Za-z0-9_]+(?:\+[A-Za-z0-9_]+)*", language):
        raise ValueError("Invalid OCR language; use Tesseract codes such as eng+deu")
    if tessdata := os.environ.get("TESSDATA_PREFIX"):
        return tessdata
    try:
        import pooch
    except ImportError as exc:
        raise RuntimeError(
            "Automatic OCR downloads require pip install 'pdf2zh[ocr]'. "
            "Alternatively, set TESSDATA_PREFIX to existing language data."
        ) from exc
    cache = Path.home() / ".cache/pdf2zh/tessdata/4.1.0"
    for code in dict.fromkeys(language.split("+")):
        filename = f"{code}.traineddata"
        try:
            pooch.retrieve(
                url=f"https://raw.githubusercontent.com/tesseract-ocr/tessdata_fast/4.1.0/{filename}",
                known_hash=None,
                fname=filename,
                path=cache,
                downloader=pooch.HTTPDownloader(timeout=60),
            )
        except (requests.RequestException, OSError) as exc:
            raise RuntimeError(
                f"Could not download OCR data for '{code}'. Check the language code "
                "and network connection, or set TESSDATA_PREFIX to local data."
            ) from exc
    return str(cache)


def _ocr_pages(doc, pages, lang_in, cancellation_event):
    """Add a text layer only to selected image-only pages in the working copy."""
    language = os.environ.get("PDF2ZH_OCR_LANGUAGE") or {
        "en": "eng",
        "zh": "chi_sim",
        "zh-cn": "chi_sim",
        "zh-tw": "chi_tra",
        "ja": "jpn",
        "ko": "kor",
        "de": "deu",
        "fr": "fra",
        "es": "spa",
        "it": "ita",
        "pt": "por",
        "ru": "rus",
    }.get(lang_in.lower(), lang_in or "eng")
    ocr_pages = set()
    tessdata = None
    for pageno in range(len(doc)):
        if cancellation_event and cancellation_event.is_set():
            raise CancelledError("task cancelled")
        if pages and pageno not in pages:
            continue
        page = doc[pageno]
        # ponytail: image-only pages; partial scans need region-level OCR later.
        if page.get_text().strip() or not page.get_image_info():
            continue
        logger.info("OCR page %d (%s)", pageno + 1, language)
        if tessdata is None:
            tessdata = _ocr_tessdata(language)
        try:
            data = page.get_pixmap(dpi=300, alpha=False, annots=False).pdfocr_tobytes(
                language=language,
                tessdata=tessdata,
            )
        except RuntimeError as exc:
            raise RuntimeError(
                f"OCR failed on page {pageno + 1} using '{language}' data in {tessdata}. "
                "Check the language data and any TESSDATA_PREFIX override. "
                "Use PDF2ZH_OCR_LANGUAGE to override the OCR language."
            ) from exc
        with Document(stream=data) as recognized:
            if not recognized[0].get_text().strip():
                logger.warning("OCR found no text on page %d", pageno + 1)
                continue
            contents = doc.get_new_xref()
            doc.update_object(contents, "<<>>")
            doc.update_stream(contents, b"")
            page.set_contents(contents)
            page.show_pdf_page(
                page.rect * page.derotation_matrix,
                recognized,
                0,
                rotate=page.rotation,
            )
        ocr_pages.add(pageno)
    return ocr_pages


def translate_stream(
    stream: bytes,
    pages: Optional[list[int]] = None,
    lang_in: str = "",
    lang_out: str = "",
    service: str = "",
    thread: int = 0,
    vfont: str = "",
    vchar: str = "",
    callback: object = None,
    cancellation_event: asyncio.Event = None,
    model: OnnxModel = None,
    envs: Dict = None,
    prompt: Template = None,
    skip_subset_fonts: bool = False,
    ignore_cache: bool = False,
    ultrafast: bool = False,
    perf=None,
    **kwarg: Any,
):
    if ultrafast and not thread:
        thread = 16
    own_perf = perf is None
    text_items = None
    if ultrafast:
        from pdf2zh.ultrafast import PerfTimer, extract_layout

        if own_perf:
            perf = PerfTimer()
        logger.info(
            "[ultrafast perf] skipped: layout models, rasterization, OCR, font subsetting; "
            "translation cache: %s",
            "off (read/write)" if ignore_cache else "on",
        )
        text_items = extract_layout(stream, pages)
        perf.step("layout_extract")
    font_list = [("tiro", None)]

    font_path = download_remote_fonts(lang_out.lower())
    noto_name = NOTO_NAME
    noto = Font(noto_name, font_path)
    font_list.append((noto_name, font_path))
    if perf:
        perf.step("font_setup")

    doc_en = Document(stream=stream)
    if ultrafast:
        doc_zh = Document(stream=stream)
    else:
        stream = io.BytesIO()
        doc_en.save(stream)
        doc_zh = Document(stream=stream)
    ocr_pages = (
        set() if ultrafast else _ocr_pages(doc_zh, pages, lang_in, cancellation_event)
    )
    page_count = doc_zh.page_count
    if perf:
        perf.step("document_open")
    # font_list = [("GoNotoKurrent-Regular.ttf", font_path), ("tiro", None)]
    font_id = {}
    for pageno, page in enumerate(doc_zh):
        if ultrafast and (
            (pages and pageno not in pages) or not text_items.get(pageno)
        ):
            continue
        for font in font_list:
            font_id[font[0]] = page.insert_font(font[0], font[1])
    xreflen = doc_zh.xref_length()
    for xref in range(1, xreflen):
        for label in ["Resources/", ""]:  # 可能是基于 xobj 的 res
            try:  # xref 读写可能出错
                font_res = doc_zh.xref_get_key(xref, f"{label}Font")
                target_key_prefix = f"{label}Font/"
                if font_res[0] == "xref":
                    resource_xref_id = re.search("(\\d+) 0 R", font_res[1]).group(1)
                    xref = int(resource_xref_id)
                    font_res = ("dict", doc_zh.xref_object(xref))
                    target_key_prefix = ""

                if font_res[0] == "dict":
                    for font in font_list:
                        target_key = f"{target_key_prefix}{font[0]}"
                        font_exist = doc_zh.xref_get_key(xref, target_key)
                        if font_exist[0] == "null":
                            doc_zh.xref_set_key(
                                xref,
                                target_key,
                                f"{font_id[font[0]]} 0 R",
                            )
            except Exception:
                pass

    if perf:
        perf.step("font_resources")
    fp = io.BytesIO()

    doc_zh.save(fp)
    if perf:
        perf.step("working_copy_save")
    obj_patch: dict = translate_patch(fp, **locals())
    if perf:
        perf.step("page_processing")

    if obj_patch and page_count > 0:
        try:
            target_pno = page_count - 1
            target_xref = None
            for pno in range(page_count - 1, -1, -1):
                for c_xref in doc_zh[pno].get_contents():
                    if c_xref in obj_patch:
                        target_pno = pno
                        target_xref = c_xref
                        break
                if target_xref is not None:
                    break
            if target_xref is None:
                target_xref = list(obj_patch.keys())[-1]
            promo_ops, link_rect = _build_promo_ops(
                doc_zh[target_pno], noto, noto_name, lang_out
            )
            obj_patch[target_xref] = f"{obj_patch[target_xref]}{promo_ops}"
            if doc_zh[target_pno].rotation == 0:
                import pymupdf as _fitz

                doc_zh[target_pno].insert_link(
                    {
                        "kind": _fitz.LINK_URI,
                        "from": _fitz.Rect(*link_rect),
                        "uri": PROMO_URL,
                    }
                )
        except Exception as exc:
            logger.debug("Skipping promo footer insertion: %s", exc)

    for obj_id, ops_new in obj_patch.items():
        # ops_old=doc_en.xref_stream(obj_id)
        # print(obj_id)
        # print(ops_old)
        # print(ops_new.encode())
        doc_zh.update_stream(obj_id, ops_new.encode())
    if perf:
        perf.step("apply_patches")

    doc_en.insert_file(doc_zh)
    for id in range(page_count):
        doc_en.move_page(page_count + id, id * 2 + 1)
    if perf:
        perf.step("bilingual_assembly")
    if not (skip_subset_fonts or ultrafast):
        try:
            doc_zh.subset_fonts(fallback=True)
            doc_en.subset_fonts(fallback=True)
        except Exception as e:
            logger.warning("subset_fonts failed, skipping font subsetting: %s", e)
    if perf:
        perf.step("font_subset")
    result = (
        doc_zh.write(deflate=True, garbage=3, use_objstms=1),
        doc_en.write(deflate=True, garbage=3, use_objstms=1),
    )
    if perf:
        perf.step("pdf_serialize")
        if own_perf:
            perf.report()
    return result


def convert_to_pdfa(input_path, output_path):
    """
    Convert PDF to PDF/A format

    Args:
        input_path: Path to source PDF file
        output_path: Path to save PDF/A file
    """
    from pikepdf import Dictionary, Name, Pdf

    # Open the PDF file
    pdf = Pdf.open(input_path)

    # Add PDF/A conformance metadata
    metadata = {
        "pdfa_part": "2",
        "pdfa_conformance": "B",
        "title": pdf.docinfo.get("/Title", ""),
        "author": pdf.docinfo.get("/Author", ""),
        "creator": "PDF Math Translate",
    }

    with pdf.open_metadata() as meta:
        meta.load_from_docinfo(pdf.docinfo)
        meta["pdfaid:part"] = metadata["pdfa_part"]
        meta["pdfaid:conformance"] = metadata["pdfa_conformance"]

    # Create OutputIntent dictionary
    output_intent = Dictionary(
        {
            "/Type": Name("/OutputIntent"),
            "/S": Name("/GTS_PDFA1"),
            "/OutputConditionIdentifier": "sRGB IEC61966-2.1",
            "/RegistryName": "http://www.color.org",
            "/Info": "sRGB IEC61966-2.1",
        }
    )

    # Add output intent to PDF root
    if "/OutputIntents" not in pdf.Root:
        pdf.Root.OutputIntents = [output_intent]
    else:
        pdf.Root.OutputIntents.append(output_intent)

    # Save as PDF/A
    pdf.save(output_path, linearize=True)
    pdf.close()


def translate(
    files: list[str],
    output: str = "",
    pages: Optional[list[int]] = None,
    lang_in: str = "",
    lang_out: str = "",
    service: str = "",
    thread: int = 0,
    vfont: str = "",
    vchar: str = "",
    callback: object = None,
    compatible: bool = False,
    cancellation_event: asyncio.Event = None,
    model: OnnxModel = None,
    envs: Dict = None,
    prompt: Template = None,
    skip_subset_fonts: bool = False,
    ignore_cache: bool = False,
    ultrafast: bool = False,
    **kwarg: Any,
):
    if not files:
        raise PDFValueError("No files to process.")

    missing_files = check_files(files)

    if missing_files:
        print("The following files do not exist:", file=sys.stderr)
        for file in missing_files:
            print(f"  {file}", file=sys.stderr)
        raise PDFValueError("Some files do not exist.")

    result_files = []

    for file in files:
        perf = None
        if ultrafast:
            from pdf2zh.ultrafast import PerfTimer

            perf = PerfTimer()
        if type(file) is str and (
            file.startswith("http://") or file.startswith("https://")
        ):
            print("Online files detected, downloading...")
            try:
                r = requests.get(file, allow_redirects=True)
                if r.status_code == 200:
                    with tempfile.NamedTemporaryFile(
                        suffix=".pdf", delete=False
                    ) as tmp_file:
                        print(f"Writing the file: {file}...")
                        tmp_file.write(r.content)
                        file = tmp_file.name
                else:
                    r.raise_for_status()
            except Exception as e:
                raise PDFValueError(
                    f"Errors occur in downloading the PDF file. Please check the link(s).\nError:\n{e}"
                )

        # Convert doc/docx to PDF if needed
        _converted_pdf = None
        if is_convertible(file):
            _converted_pdf = convert_to_pdf(file)
            filename = os.path.splitext(os.path.basename(file))[0]
            file = _converted_pdf
        else:
            filename = os.path.splitext(os.path.basename(file))[0]

        # If the commandline has specified converting to PDF/A format
        # --compatible / -cp
        if compatible:
            with tempfile.NamedTemporaryFile(
                suffix="-pdfa.pdf", delete=False
            ) as tmp_pdfa:
                print(f"Converting {file} to PDF/A format...")
                convert_to_pdfa(file, tmp_pdfa.name)
                doc_raw = open(tmp_pdfa.name, "rb")
                os.unlink(tmp_pdfa.name)
        else:
            doc_raw = open(file, "rb")
        s_raw = doc_raw.read()
        doc_raw.close()
        if perf:
            perf.step("input_read")

        temp_dir = Path(tempfile.gettempdir())
        file_path = Path(file)
        try:
            if file_path.exists() and file_path.resolve().is_relative_to(
                temp_dir.resolve()
            ):
                file_path.unlink(missing_ok=True)
                logger.debug(f"Cleaned temp file: {file_path}")
        except Exception:
            logger.warning(f"Failed to clean temp file {file_path}", exc_info=True)

        s_mono, s_dual = translate_stream(
            s_raw,
            **locals(),
        )
        file_mono = Path(output) / f"{filename}-mono.pdf"
        file_dual = Path(output) / f"{filename}-dual.pdf"
        doc_mono = open(file_mono, "wb")
        doc_dual = open(file_dual, "wb")
        doc_mono.write(s_mono)
        doc_dual.write(s_dual)
        doc_mono.close()
        doc_dual.close()
        if perf:
            perf.step("output_write")
            perf.report()
        result_files.append((str(file_mono), str(file_dual)))

    return result_files


def download_remote_fonts(lang: str):
    lang = lang.lower()
    LANG_NAME_MAP = {
        **{la: "GoNotoKurrent-Regular.ttf" for la in noto_list},
        **{
            la: f"SourceHanSerif{region}-Regular.ttf"
            for region, langs in {
                "CN": ["zh-cn", "zh-hans", "zh"],
                "TW": ["zh-tw", "zh-hant"],
                "JP": ["ja"],
                "KR": ["ko"],
            }.items()
            for la in langs
        },
    }
    font_name = LANG_NAME_MAP.get(lang, "GoNotoKurrent-Regular.ttf")

    # docker
    font_path = ConfigManager.get("NOTO_FONT_PATH", Path("/app", font_name).as_posix())
    if not Path(font_path).exists():
        from babeldoc.assets.assets import get_font_and_metadata

        font_path, _ = get_font_and_metadata(font_name)
        font_path = font_path.as_posix()

    logger.info(f"use font: {font_path}")

    return font_path
