import concurrent.futures
import logging
import re
import unicodedata
from time import perf_counter
from enum import Enum
from string import Template
from typing import Dict

import numpy as np
from pdfminer.converter import PDFConverter
from pdfminer.layout import LTChar, LTFigure, LTLine, LTPage
from pdfminer.pdffont import PDFCIDFont, PDFUnicodeNotDefined
from pdfminer.pdfinterp import PDFGraphicState, PDFResourceManager
from pdfminer.utils import apply_matrix_pt, mult_matrix
from pymupdf import Font
from tenacity import retry, wait_fixed

from pdf2zh.text_spacing import add_cjk_latin_spacing
from pdf2zh.translator import (
    AnythingLLMTranslator,
    ArgosTranslator,
    AzureOpenAITranslator,
    AzureTranslator,
    BaseTranslator,
    BingTranslator,
    DeepLTranslator,
    DeepLXTranslator,
    DeepseekTranslator,
    DifyTranslator,
    GeminiTranslator,
    GoogleTranslator,
    GrokTranslator,
    GroqTranslator,
    MiniMaxTranslator,
    ModelScopeTranslator,
    OllamaTranslator,
    OpenAIlikedTranslator,
    OpenAITranslator,
    QwenMtTranslator,
    SiliconTranslator,
    TencentTranslator,
    XinferenceTranslator,
    ZhipuTranslator,
    X302AITranslator,
)

log = logging.getLogger(__name__)


class PDFConverterEx(PDFConverter):
    def __init__(
        self,
        rsrcmgr: PDFResourceManager,
    ) -> None:
        PDFConverter.__init__(self, rsrcmgr, None, "utf-8", 1, None)

    def begin_page(self, page, ctm) -> None:
        # 重载替换 cropbox
        x0, y0, x1, y1 = page.cropbox
        x0, y0 = apply_matrix_pt(ctm, (x0, y0))
        x1, y1 = apply_matrix_pt(ctm, (x1, y1))
        mediabox = (0, 0, abs(x0 - x1), abs(y0 - y1))
        self.cur_item = LTPage(page.pageno, mediabox)

    def end_page(self, page):
        # 重载返回指令流
        return self.receive_layout(self.cur_item)

    def begin_figure(self, name, bbox, matrix) -> None:
        # 重载设置 pageid
        self._stack.append(self.cur_item)
        self.cur_item = LTFigure(name, bbox, mult_matrix(matrix, self.ctm))
        self.cur_item.pageid = self._stack[-1].pageid

    def end_figure(self, _: str) -> None:
        # 重载返回指令流
        fig = self.cur_item
        assert isinstance(self.cur_item, LTFigure), str(type(self.cur_item))
        self.cur_item = self._stack.pop()
        self.cur_item.add(fig)
        return self.receive_layout(fig)

    def render_char(
        self,
        matrix,
        font,
        fontsize: float,
        scaling: float,
        rise: float,
        cid: int,
        ncs,
        graphicstate: PDFGraphicState,
    ) -> float:
        # 重载设置 cid 和 font
        try:
            text = font.to_unichr(cid)
            assert isinstance(text, str), str(type(text))
        except PDFUnicodeNotDefined:
            text = self.handle_undefined_char(font, cid)
        textwidth = font.char_width(cid)
        textdisp = font.char_disp(cid)
        item = LTChar(
            matrix,
            font,
            fontsize,
            scaling,
            rise,
            text,
            textwidth,
            textdisp,
            ncs,
            graphicstate,
        )
        self.cur_item.add(item)
        item.cid = cid  # hack 插入原字符编码
        item.font = font  # hack 插入原字符字体
        return item.adv


class Paragraph:
    def __init__(self, y, x, x0, x1, y0, y1, size, brk):
        self.y: float = y  # 初始纵坐标
        self.x: float = x  # 初始横坐标
        self.x0: float = x0  # 左边界
        self.x1: float = x1  # 右边界
        self.y0: float = y0  # 上边界
        self.y1: float = y1  # 下边界
        self.size: float = size  # 字体大小
        self.brk: bool = brk  # 换行标记


# fmt: off
class TranslateConverter(PDFConverterEx):
    def __init__(
        self,
        rsrcmgr,
        vfont: str = None,
        vchar: str = None,
        thread: int = 0,
        layout={},
        lang_in: str = "",
        lang_out: str = "",
        service: str = "",
        noto_name: str = "",
        noto: Font = None,
        envs: Dict = None,
        prompt: Template = None,
        ignore_cache: bool = False,
    ) -> None:
        super().__init__(rsrcmgr)
        self.vfont = vfont
        self.vchar = vchar
        self.thread = thread
        self.layout = layout
        self.noto_name = noto_name
        self.noto = noto
        self.perf = None
        self.translation_pool = None
        self.translation_futures = None
        self.translator: BaseTranslator = None
        # e.g. "ollama:gemma2:9b" -> ["ollama", "gemma2:9b"]
        param = service.split(":", 1)
        service_name = param[0]
        service_model = param[1] if len(param) > 1 else None
        if not envs:
            envs = {}
        for translator in [GoogleTranslator, BingTranslator, DeepLTranslator, DeepLXTranslator, OllamaTranslator, XinferenceTranslator, AzureOpenAITranslator,
                           OpenAITranslator, ZhipuTranslator, ModelScopeTranslator, SiliconTranslator, GeminiTranslator, AzureTranslator, TencentTranslator, DifyTranslator, AnythingLLMTranslator, ArgosTranslator, GrokTranslator, GroqTranslator, DeepseekTranslator, MiniMaxTranslator, OpenAIlikedTranslator, QwenMtTranslator, X302AITranslator]:
            if service_name == translator.name:
                self.translator = translator(lang_in, lang_out, service_model, envs=envs, prompt=prompt, ignore_cache=ignore_cache)
        if not self.translator:
            raise ValueError("Unsupported translation service")

    def receive_layout(self, ltpage: LTPage):
        started = perf_counter() if self.perf else 0
        # 段落
        sstk: list[str] = []            # 段落文字栈
        pstk: list[Paragraph] = []      # 段落属性栈
        vbkt: int = 0                   # 段落公式括号计数
        # 公式组
        vstk: list[LTChar] = []         # 公式符号组
        vlstk: list[LTLine] = []        # 公式线条组
        vfix: float = 0                 # 公式纵向偏移
        # 公式组栈
        var: list[list[LTChar]] = []    # 公式符号组栈
        varl: list[list[LTLine]] = []   # 公式线条组栈
        varf: list[float] = []          # 公式纵向偏移栈
        vlen: list[float] = []          # 公式宽度栈
        # 全局
        lstk: list[LTLine] = []         # 全局线条栈
        xt: LTChar = None               # 上一个字符
        xt_cls: int = -1                # 上一个字符所属段落，保证无论第一个字符属于哪个类别都可以触发新段落
        vmax: float = ltpage.width / 4  # 行内公式最大宽度
        ops: str = ""                   # 渲染结果

        def normalize_font(font) -> str:
            if isinstance(font, bytes):
                try:
                    font = font.decode("utf-8")
                except UnicodeDecodeError:
                    font = ""
            elif not isinstance(font, str):
                font = str(font)
            return font.split("+")[-1]

        def is_code_font(font) -> bool:
            fname = normalize_font(font)
            if self.vfont and re.match(self.vfont, fname):
                return True
            return bool(
                re.search(
                    r"(?:mono|code|cour|consolas|menlo|monaco|inconsolata|lucidaconsole|"
                    r"fira\s*code|jetbrains|source\s*code|ubuntu\s*mono|roboto\s*mono|"
                    r"cascadia|hack|nimbusmon|texgyrecursor|lmmono|lmtt|cmtt|txtt|pxtt|"
                    r"ectt|typewriter|fixed|berasansmono|dejavusansmono|liberationmono|"
                    r"sfmono|dina|proggy|terminus|iosevka)",
                    fname,
                    re.IGNORECASE,
                )
            )

        def vflag(font: str, char: str):    # 匹配公式（和角标）字体
            font = normalize_font(font)
            if isinstance(char, str) and re.match(r"\(cid:", char):
                return True
            # 基于字体名规则的判定
            if self.vfont:
                if re.match(self.vfont, font):
                    return True
            else:
                if re.match(                                            # latex 字体
                    r"(CM[^R]|MS.M|XY|MT|BL|RM|EU|LA|RS|LINE|LCIRCLE|TeX-|rsfs|txsy|wasy|stmary|.*Mono|.*Code|.*Ital|.*Sym|.*Math)",
                    font,
                ) or is_code_font(font):
                    return True
            # 基于字符集规则的判定
            if self.vchar:
                if isinstance(char, str) and re.match(self.vchar, char):
                    return True
            else:
                if (
                    char
                    and isinstance(char, str)
                    and char != " "                                     # 非空格
                    and (
                        unicodedata.category(char[0])
                        in ["Lm", "Mn", "Sk", "Sm", "Zl", "Zp", "Zs"]   # 文字修饰符、数学符号、分隔符号
                        or ord(char[0]) in range(0x370, 0x400)          # 希腊字母
                    )
                ):
                    return True
            return False

        ############################################################
        # A0. 页面视觉行预分析（解决目录排版错乱 & 跨页/行号程序代码乱码）
        layout_map = self.layout[ltpage.pageid]
        h_map, w_map = layout_map.shape
        char_cls_override: dict[int, int] = {}
        char_force_text: set[int] = set()
        char_vgroup: dict[int, int] = {}
        cls_max_x1: dict[int, float] = {}
        toc_vgroup_meta: dict[int, dict] = {}
        para_cls_list: list[int] = []
        toc_dots_para_map: dict[int, dict] = {}
        toc_title_para_ids: set[int] = set()

        real_chars = [
            c for c in ltpage
            if isinstance(c, LTChar)
            and isinstance(getattr(c, "x0", None), (int, float))
            and isinstance(getattr(c, "y0", None), (int, float))
            and isinstance(getattr(c, "size", None), (int, float))
            and isinstance(c.get_text(), str)
        ]

        if real_chars:
            def _char_raw_cls(ch: LTChar) -> int:
                cx_ = int(np.clip(int(ch.x0), 0, w_map - 1))
                cy_ = int(np.clip(int(ch.y0), 0, h_map - 1))
                val = layout_map[cy_, cx_]
                return int(val) if isinstance(val, (int, np.integer)) else int(val)

            # 按垂直基线聚类为视觉行，再按双栏布局切分
            y_sorted = sorted(real_chars, key=lambda c: (-round(c.y0, 1), c.x0))
            y_bands: list[list[LTChar]] = []
            for ch in y_sorted:
                placed = False
                for band in reversed(y_bands[-4:]):
                    ref_y0 = band[0].y0
                    ref_sz = max(band[0].size, ch.size, 1.0)
                    if abs(ch.y0 - ref_y0) <= ref_sz * 0.48:
                        band.append(ch)
                        placed = True
                        break
                if not placed:
                    y_bands.append([ch])

            visual_lines: list[list[LTChar]] = []
            for band in y_bands:
                band.sort(key=lambda c: c.x0)
                # 检查是否需要按多栏不同 layout box 拆分
                sub_lines: list[list[LTChar]] = [[band[0]]]
                for ch in band[1:]:
                    prev_ch = sub_lines[-1][-1]
                    gap = ch.x0 - prev_ch.x1
                    ref_sz = max(ch.size, prev_ch.size, 1.0)
                    if gap > ref_sz * 2.5:
                        c1 = _char_raw_cls(prev_ch)
                        c2 = _char_raw_cls(ch)
                        if c1 > 1 and c2 > 1 and c1 != c2:
                            sub_lines.append([ch])
                            continue
                    sub_lines[-1].append(ch)
                # 如果右侧子段只是短页码（如目录页最右侧的页码），合并回同一视觉行
                if len(sub_lines) >= 2:
                    merged_subs: list[list[LTChar]] = [sub_lines[0]]
                    for sub in sub_lines[1:]:
                        sub_txt = "".join(c.get_text() for c in sub).strip()
                        if re.match(r"^(?:\d{1,4}|[ivxlcdmIVXLCDM]{1,6})$", sub_txt):
                            merged_subs[-1].extend(sub)
                        else:
                            merged_subs.append(sub)
                    sub_lines = merged_subs
                visual_lines.extend(sub_lines)

            visual_lines.sort(key=lambda ln: (-ln[0].y0, ln[0].x0))

            _syn_cls_counter = 100000
            _vgroup_counter = 1

            def _next_syn_cls() -> int:
                nonlocal _syn_cls_counter
                _syn_cls_counter += 1
                return _syn_cls_counter

            def _next_vgroup() -> int:
                nonlocal _vgroup_counter
                _vgroup_counter += 1
                return _vgroup_counter

            line_infos: list[dict] = []
            has_toc_heading = False
            num_toc_leader = 0
            num_toc_wide_gap_cand = 0

            for ln in visual_lines:
                txt = "".join(c.get_text() for c in ln)
                stripped = txt.strip()
                non_space = [c for c in ln if c.get_text().strip()]
                ln_size = max((c.size for c in non_space), default=ln[0].size)
                raw_classes = [_char_raw_cls(c) for c in non_space if _char_raw_cls(c) > 0]
                dom_cls = max(set(raw_classes), key=raw_classes.count) if raw_classes else 0

                info = {
                    "chars": ln,
                    "non_space": non_space,
                    "text": txt,
                    "stripped": stripped,
                    "size": ln_size,
                    "y0": float(np.median([c.y0 for c in ln])),
                    "x0": ln[0].x0,
                    "x1": ln[-1].x1,
                    "dom_cls": dom_cls,
                    "kind": None,
                    "code_tag": "PROSE",
                    "is_code": False,
                }
                line_infos.append(info)

                if not stripped:
                    continue

                if re.match(
                    r"^(?:table\s+of\s+contents|contents|目\s*录|目\s*次)$",
                    stripped,
                    re.IGNORECASE,
                ):
                    has_toc_heading = True

                # 1. 跨页代码/表格续页提示行（如 Sphinx/LaTeX 的 continued from previous page / continues on next page）
                if re.match(
                    r"^\(?\s*(?:continued\s+from\s+previous\s+page|continues\s+on\s+next\s+page)\s*\)?\.?$",
                    stripped,
                    re.IGNORECASE,
                ) or (
                    len(stripped) < 65
                    and re.search(
                        r"continued\s+from\s+previous\s+page|continues\s+on\s+next\s+page",
                        stripped,
                        re.IGNORECASE,
                    )
                ):
                    info["kind"] = "CONTINUATION"
                    continue

                # 2. 检测带引导点（. . . . . 42）的目录行
                idx = len(ln) - 1
                while idx >= 0 and not ln[idx].get_text().strip():
                    idx -= 1
                page_end = idx
                while (
                    idx >= 0
                    and ln[idx].get_text().strip()
                    and re.match(r"^[0-9ivxlcdmIVXLCDM\-–—]$", ln[idx].get_text())
                ):
                    idx -= 1
                page_start = idx + 1
                page_chars = [c for c in ln[page_start : page_end + 1] if c.get_text().strip()]
                if len(page_chars) > 8:
                    page_chars = []
                    idx = page_end

                while idx >= 0 and not ln[idx].get_text().strip():
                    idx -= 1
                dots_end = idx
                while idx >= 0 and (
                    not ln[idx].get_text().strip()
                    or ln[idx].get_text() in {".", "·", "…", "•"}
                ):
                    idx -= 1
                dots_start = idx + 1
                dot_region = ln[dots_start : dots_end + 1]
                dot_only = [c for c in dot_region if c.get_text().strip() in {".", "·", "…", "•"}]
                title_part = ln[:dots_start]
                while title_part and not title_part[-1].get_text().strip():
                    title_part = title_part[:-1]

                if len(dot_only) >= 3 and any(c.get_text().strip() for c in title_part):
                    info["kind"] = "TOC_LEADER"
                    info["title_chars"] = title_part
                    info["dot_only_chars"] = dot_only
                    info["page_chars"] = page_chars
                    info["tail_chars"] = ln[len(title_part) :]
                    num_toc_leader += 1
                    continue

                # 3. 检测无引导点但右侧大间距对齐页码的目录候选行（如 "1  Introduction to CUDA          3"）
                if 1 <= len(page_chars) <= 6:
                    page_str = "".join(c.get_text() for c in page_chars)
                    title_cand = ln[:page_start]
                    while title_cand and not title_cand[-1].get_text().strip():
                        title_cand = title_cand[:-1]
                    title_non_space = [c for c in title_cand if c.get_text().strip()]
                    has_alpha = any(c.get_text().isalpha() for c in title_non_space)
                    if (
                        len(title_non_space) >= 2
                        and has_alpha
                        and re.match(r"^(?:\d{1,4}|[ivxlcdmIVXLCDM]{1,6})$", page_str)
                    ):
                        gap_to_page = page_chars[0].x0 - title_non_space[-1].x1
                        if gap_to_page > max(ln_size * 3.5, ltpage.width * 0.08):
                            info["kind"] = "TOC_WIDE_CAND"
                            info["title_chars"] = title_cand
                            info["dot_only_chars"] = []
                            info["page_chars"] = page_chars
                            info["tail_chars"] = ln[len(title_cand) :]
                            info["gap_to_page"] = gap_to_page
                            num_toc_wide_gap_cand += 1

            is_toc_page = (
                num_toc_leader >= 2
                or (num_toc_leader >= 1 and has_toc_heading)
                or (num_toc_wide_gap_cand >= 3 and has_toc_heading)
                or num_toc_wide_gap_cand >= 5
            )

            for info in line_infos:
                if info["kind"] == "TOC_WIDE_CAND":
                    if is_toc_page or (
                        re.match(
                            r"^\s*(?:chapter|part|section|appendix|\d+(?:\.\d+)*)\b",
                            info["stripped"],
                            re.IGNORECASE,
                        )
                        and info.get("gap_to_page", 0) > ltpage.width * 0.18
                        and (num_toc_leader + num_toc_wide_gap_cand) >= 2
                    ):
                        info["kind"] = "TOC_WIDE"
                    else:
                        info["kind"] = None

            # 4. 检测程序代码行（支持带行号代码、语法高亮代码、跨页代码段）
            for info in line_infos:
                if info["kind"] is not None or not info["non_space"]:
                    continue
                ns = info["non_space"]
                # 检测左侧行号 + 代码字体（如 "1 __global__ void ..."）
                lead_digits: list[LTChar] = []
                for c in ns:
                    if c.get_text().isdigit():
                        lead_digits.append(c)
                    else:
                        break
                rest_ns = ns[len(lead_digits) :]
                if (
                    1 <= len(lead_digits) <= 4
                    and rest_ns
                    and (rest_ns[0].x0 - lead_digits[-1].x1) > 0.5
                ):
                    rest_code_cnt = sum(1 for c in rest_ns if is_code_font(c.fontname))
                    if rest_code_cnt / len(rest_ns) >= 0.5:
                        info["code_tag"] = "DEFINITE"
                        info["is_code"] = True
                        continue

                code_cnt = sum(1 for c in ns if is_code_font(c.fontname))
                code_ratio = code_cnt / len(ns)
                if code_ratio >= 0.75:
                    info["code_tag"] = "CANDIDATE"
                elif code_ratio >= 0.45:
                    info["code_tag"] = "SEMI"
                elif all(
                    c.get_text() in "{}()[];,.:+-*/=&|<>!~%^\"'\\0123456789_#@$"
                    for c in ns
                ):
                    info["code_tag"] = "PUNCT"
                else:
                    info["code_tag"] = "PROSE"

            for idx_ln, info in enumerate(line_infos):
                if info["code_tag"] == "CANDIDATE":
                    prev_info = line_infos[idx_ln - 1] if idx_ln > 0 else None
                    next_info = (
                        line_infos[idx_ln + 1] if idx_ln + 1 < len(line_infos) else None
                    )
                    # 判断是否只是普通正文段落末尾换行落单的一个行内代码词
                    is_wrapped_inline = False
                    if (
                        prev_info is not None
                        and prev_info["kind"] is None
                        and prev_info["code_tag"] == "PROSE"
                        and prev_info["dom_cls"] > 0
                        and prev_info["dom_cls"] == info["dom_cls"]
                        and abs(prev_info["y0"] - info["y0"]) <= info["size"] * 2.2
                        and not prev_info["stripped"].endswith((":", ".", ";", "{", "}"))
                        and (
                            next_info is None
                            or next_info["code_tag"]
                            not in ("DEFINITE", "CANDIDATE", "SEMI")
                        )
                    ):
                        is_wrapped_inline = True
                    if not is_wrapped_inline:
                        info["is_code"] = True

            # 在相邻代码行之间传播（覆盖代码块中的纯括号行、行号+注释行、混合高亮行）
            for _ in range(2):
                for idx_ln, info in enumerate(line_infos):
                    if info["is_code"] or info["kind"] is not None or not info["non_space"]:
                        continue
                    if info["code_tag"] in ("SEMI", "PUNCT", "CANDIDATE") or re.match(
                        r"^\d+\s*(?://|/\*|#|\}|\{)", info["stripped"]
                    ):
                        prev_info = line_infos[idx_ln - 1] if idx_ln > 0 else None
                        next_info = (
                            line_infos[idx_ln + 1]
                            if idx_ln + 1 < len(line_infos)
                            else None
                        )
                        near_prev_code = (
                            prev_info is not None
                            and prev_info["is_code"]
                            and abs(prev_info["y0"] - info["y0"]) <= max(info["size"], prev_info["size"]) * 3.0
                        )
                        near_next_code = (
                            next_info is not None
                            and next_info["is_code"]
                            and abs(info["y0"] - next_info["y0"]) <= max(info["size"], next_info["size"]) * 3.0
                        )
                        if near_prev_code or near_next_code:
                            info["is_code"] = True

            # 5. 将预分析结果写入字符级映射表
            for info in line_infos:
                kind = info["kind"]
                if kind == "CONTINUATION":
                    syn_cls = _next_syn_cls()
                    for c in info["chars"]:
                        char_cls_override[id(c)] = syn_cls
                        char_force_text.add(id(c))
                elif kind in ("TOC_LEADER", "TOC_WIDE"):
                    title_chars = info["title_chars"]
                    dot_only = info["dot_only_chars"]
                    page_chars = info["page_chars"]
                    tail_chars = info["tail_chars"]

                    # 若章节号与标题之间存在较大制表符间距（如 "1    Introduction to CUDA"），锚定左侧章节号
                    t_ns = [c for c in title_chars if c.get_text().strip()]
                    split_pos = None
                    for i_c in range(len(title_chars) - 1):
                        c_cur = title_chars[i_c]
                        c_nxt = title_chars[i_c + 1]
                        if c_cur.get_text().strip() and c_nxt.get_text().strip():
                            if (c_nxt.x0 - c_cur.x1) > info["size"] * 1.35:
                                left_str = "".join(
                                    x.get_text() for x in title_chars[: i_c + 1]
                                ).strip()
                                if re.match(r"^\d+(?:\.\d+)*\.?$", left_str):
                                    split_pos = i_c + 1
                                    break
                    if split_pos is not None and t_ns:
                        sec_vg = _next_vgroup()
                        for c in title_chars[:split_pos]:
                            char_vgroup[id(c)] = sec_vg
                        title_chars = title_chars[split_pos:]
                        while title_chars and not title_chars[0].get_text().strip():
                            char_vgroup[id(title_chars[0])] = sec_vg
                            title_chars = title_chars[1:]

                    title_syn_cls = _next_syn_cls()
                    for c in title_chars:
                        char_cls_override[id(c)] = title_syn_cls
                    if page_chars:
                        cls_max_x1[title_syn_cls] = page_chars[0].x0 - info["size"] * 0.6
                    elif dot_only:
                        cls_max_x1[title_syn_cls] = dot_only[-1].x1
                    else:
                        cls_max_x1[title_syn_cls] = info["x1"]

                    dots_vg = _next_vgroup()
                    for c in tail_chars:
                        char_vgroup[id(c)] = dots_vg
                    toc_vgroup_meta[dots_vg] = {
                        "title_cls": title_syn_cls,
                        "dot_chars": dot_only,
                        "page_chars": page_chars,
                    }
                elif info["is_code"]:
                    code_vg = _next_vgroup()
                    for c in info["chars"]:
                        char_vgroup[id(c)] = code_vg
                elif is_toc_page:
                    syn_cls = _next_syn_cls()
                    for c in info["chars"]:
                        char_cls_override[id(c)] = syn_cls

        ############################################################
        # A. 原文档解析
        cur_vgroup: int = None
        for child in ltpage:
            if isinstance(child, LTChar):
                child_vg = char_vgroup.get(id(child))
                if child_vg is not None:
                    # 独立锚定的代码行或目录引导点/页码组：保持原坐标不变
                    if cur_vgroup != child_vg:
                        if vstk:
                            if sstk[-1] == "":
                                xt_cls = -1
                            sstk[-1] += f"{{v{len(var)}}}"
                            var.append(vstk)
                            varl.append(vlstk)
                            varf.append(vfix)
                            vstk = []
                            vlstk = []
                            vfix = 0
                        sstk.append("")
                        pstk.append(
                            Paragraph(
                                child.y0,
                                child.x0,
                                child.x0,
                                child.x1,
                                child.y0,
                                child.y1,
                                child.size,
                                False,
                            )
                        )
                        para_cls_list.append(-1)
                        if child_vg in toc_vgroup_meta:
                            toc_dots_para_map[len(sstk) - 1] = toc_vgroup_meta[child_vg]
                        cur_vgroup = child_vg
                    vstk.append(child)
                    pstk[-1].x0 = min(pstk[-1].x0, child.x0)
                    pstk[-1].x1 = max(pstk[-1].x1, child.x1)
                    pstk[-1].y0 = min(pstk[-1].y0, child.y0)
                    pstk[-1].y1 = max(pstk[-1].y1, child.y1)
                    xt = child
                    xt_cls = -1
                    continue
                elif cur_vgroup is not None:
                    if vstk:
                        sstk[-1] += f"{{v{len(var)}}}"
                        var.append(vstk)
                        varl.append(vlstk)
                        varf.append(vfix)
                        vstk = []
                        vlstk = []
                        vfix = 0
                    cur_vgroup = None
                    xt_cls = -1

                cur_v = False
                layout = self.layout[ltpage.pageid]
                # ltpage.height 可能是 fig 里面的高度，这里统一用 layout.shape
                h, w = layout.shape
                # 读取当前字符在 layout 中的类别
                cx, cy = np.clip(int(child.x0), 0, w - 1), np.clip(int(child.y0), 0, h - 1)
                cls = char_cls_override.get(id(child), layout[cy, cx])
                # 锚定文档中 bullet 的位置
                if child.get_text() == "•":
                    cls = 0
                # 同一 layout 框内换行后若字号发生显著变化（如标题与子条目在同一框内），强制开启新段落，防止误判为角标
                same_visual_line = (
                    xt is not None
                    and abs(child.y0 - xt.y0) < max(child.size, pstk[-1].size if pstk else child.size) * 0.85
                )
                if (
                    cls == xt_cls
                    and cls > 0
                    and pstk
                    and not same_visual_line
                    and child.get_text().strip()
                    and (
                        child.size < pstk[-1].size * 0.82
                        or child.size > pstk[-1].size * 1.22
                    )
                ):
                    xt_cls = -1
                # 判定当前字符是否属于公式
                if id(child) not in char_force_text and (                                                  # 判定当前字符是否属于公式
                    cls == 0                                                                                # 1. 类别为保留区域
                    or (
                        cls == xt_cls
                        and same_visual_line
                        and len(sstk[-1].strip()) > 1
                        and child.size < pstk[-1].size * 0.79
                    )                                                                                       # 2. 同行角标字体
                    or vflag(child.fontname, child.get_text())                                              # 3. 公式字体
                    or (child.matrix[0] == 0 and child.matrix[3] == 0)                                      # 4. 垂直字体
                ):
                    cur_v = True
                # 判定括号组是否属于公式
                if not cur_v and id(child) not in char_force_text:
                    if vstk and child.get_text() == "(":
                        cur_v = True
                        vbkt += 1
                    if vbkt and child.get_text() == ")":
                        cur_v = True
                        vbkt -= 1
                if (                                                        # 判定当前公式是否结束
                    not cur_v                                               # 1. 当前字符不属于公式
                    or cls != xt_cls                                        # 2. 当前字符与前一个字符不属于同一段落
                    # or (abs(child.x0 - xt.x0) > vmax and cls != 0)        # 3. 段落内换行，可能是一长串斜体的段落，也可能是段内分式换行，这里设个阈值进行区分
                    # 禁止纯公式（代码）段落换行，直到文字开始再重开文字段落，保证只存在两种情况
                    # A. 纯公式（代码）段落（锚定绝对位置）sstk[-1]=="" -> sstk[-1]=="{v*}"
                    # B. 文字开头段落（排版相对位置）sstk[-1]!=""
                    or (sstk[-1] != "" and abs(child.x0 - xt.x0) > vmax)    # 因为 cls==xt_cls==0 一定有 sstk[-1]==""，所以这里不需要再判定 cls!=0
                ):
                    if vstk:
                        if (                                                # 根据公式右侧的文字修正公式的纵向偏移
                            not cur_v                                       # 1. 当前字符不属于公式
                            and cls == xt_cls                               # 2. 当前字符与前一个字符属于同一段落
                            and child.x0 > max([vch.x0 for vch in vstk])    # 3. 当前字符在公式右侧
                        ):
                            vfix = vstk[0].y0 - child.y0
                        if sstk[-1] == "":
                            xt_cls = -1 # 禁止纯公式段落（sstk[-1]=="{v*}"）的后续连接，但是要考虑新字符和后续字符的连接，所以这里修改的是上个字符的类别
                        sstk[-1] += f"{{v{len(var)}}}"
                        var.append(vstk)
                        varl.append(vlstk)
                        varf.append(vfix)
                        vstk = []
                        vlstk = []
                        vfix = 0
                # 当前字符不属于公式或当前字符是公式的第一个字符
                if not vstk:
                    if cls == xt_cls:               # 当前字符与前一个字符属于同一段落
                        if child.x0 > xt.x1 + 1:    # 添加行内空格
                            sstk[-1] += " "
                        elif child.x1 < xt.x0:      # 添加换行空格并标记原文段落存在换行
                            sstk[-1] += " "
                            pstk[-1].brk = True
                    else:                           # 根据当前字符构建一个新的段落
                        sstk.append("")
                        init_x1 = cls_max_x1.get(cls, child.x0)
                        pstk.append(Paragraph(child.y0, child.x0, child.x0, init_x1, child.y0, child.y1, child.size, False))
                        para_cls_list.append(cls)
                        if cls in cls_max_x1:
                            toc_title_para_ids.add(len(sstk) - 1)
                if not cur_v:                                               # 文字入栈
                    if (                                                    # 根据当前字符修正段落属性
                        (
                            child.size > pstk[-1].size                      # 1. 当前字符比段落字体大
                            and (xt is None or same_visual_line)
                        )
                        or len(sstk[-1].strip()) == 1                       # 2. 当前字符为段落第二个文字（考虑首字母放大的情况）
                    ) and child.get_text() != " ":                          # 3. 当前字符不是空格
                        pstk[-1].y -= child.size - pstk[-1].size            # 修正段落初始纵坐标，假设两个不同大小字符的上边界对齐
                        pstk[-1].size = child.size
                    sstk[-1] += child.get_text()
                else:                                                       # 公式入栈
                    if (                                                    # 根据公式左侧的文字修正公式的纵向偏移
                        not vstk                                            # 1. 当前字符是公式的第一个字符
                        and cls == xt_cls                                   # 2. 当前字符与前一个字符属于同一段落
                        and child.x0 > xt.x0                                # 3. 前一个字符在公式左侧
                    ):
                        vfix = child.y0 - xt.y0
                    vstk.append(child)
                # 更新段落边界，因为段落内换行之后可能是公式开头，所以要在外边处理
                pstk[-1].x0 = min(pstk[-1].x0, child.x0)
                pstk[-1].x1 = max(pstk[-1].x1, child.x1)
                pstk[-1].y0 = min(pstk[-1].y0, child.y0)
                pstk[-1].y1 = max(pstk[-1].y1, child.y1)
                # 更新上一个字符
                xt = child
                xt_cls = cls
            elif isinstance(child, LTFigure):   # 图表
                pass
            elif isinstance(child, LTLine):     # 线条
                layout = self.layout[ltpage.pageid]
                # ltpage.height 可能是 fig 里面的高度，这里统一用 layout.shape
                h, w = layout.shape
                # 读取当前线条在 layout 中的类别
                cx, cy = np.clip(int(child.x0), 0, w - 1), np.clip(int(child.y0), 0, h - 1)
                cls = layout[cy, cx]
                if vstk and cls == xt_cls:      # 公式线条
                    vlstk.append(child)
                else:                           # 全局线条
                    lstk.append(child)
            else:
                pass
        # 处理结尾
        if vstk:    # 公式出栈
            sstk[-1] += f"{{v{len(var)}}}"
            var.append(vstk)
            varl.append(vlstk)
            varf.append(vfix)
        log.debug("\n==========[VSTACK]==========\n")
        for pid, v in enumerate(var):  # 计算公式宽度
            l = max([vch.x1 for vch in v]) - v[0].x0
            log.debug(f'< {l:.1f} {v[0].x0:.1f} {v[0].y0:.1f} {v[0].cid} {v[0].fontname} {len(varl[pid])} > v{pid} = {"".join([ch.get_text() for ch in v])}')
            vlen.append(l)

        ############################################################
        # B. 段落翻译
        log.debug("\n==========[SSTACK]==========\n")

        @retry(wait=wait_fixed(1))
        def worker(s: str):  # 多线程翻译
            if not s.strip() or re.match(r"^\{v\d+\}$", s):  # 空白和公式不翻译
                return s
            try:
                new = self.translator.translate(s)
                return new
            except BaseException as e:
                if log.isEnabledFor(logging.DEBUG):
                    log.exception(e)
                else:
                    log.exception(e, exc_info=False)
                raise e
        if self.perf:
            self.perf.add("paragraph_parse", perf_counter() - started)
            started = perf_counter()
        if self.translation_pool is not None:
            self.translation_futures.extend(self.translation_pool.submit(worker, s) for s in sstk)
            if self.perf:
                self.perf.add("translation_submit", perf_counter() - started)
            return ""  # Typeset after the whole document's requests have completed.
        if self.translation_futures is not None:
            news = [self.translation_futures.popleft().result() for _ in sstk]
        else:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=self.thread
            ) as executor:
                news = list(executor.map(worker, sstk))
        if self.perf:
            self.perf.add("translation", perf_counter() - started)
            started = perf_counter()

        ############################################################
        # C. 新文档排版
        def raw_string(fcur: str, cstk: str):  # 编码字符串
            if fcur == self.noto_name:
                return "".join(["%04x" % self.noto.has_glyph(ord(c)) for c in cstk])
            elif isinstance(self.fontmap[fcur], PDFCIDFont):  # 判断编码长度
                return "".join(["%04x" % ord(c) for c in cstk])
            else:
                return "".join(["%02x" % ord(c) for c in cstk])

        # 根据目标语言获取默认行距
        LANG_LINEHEIGHT_MAP = {
            "zh-cn": 1.4, "zh-tw": 1.4, "zh-hans": 1.4, "zh-hant": 1.4, "zh": 1.4,
            "ja": 1.1, "ko": 1.2, "en": 1.2, "ar": 1.0, "ru": 0.8, "uk": 0.8, "ta": 0.8
        }
        default_line_height = LANG_LINEHEIGHT_MAP.get(self.translator.lang_out.lower(), 1.1) # 小语种默认1.1
        _x, _y = 0, 0
        ops_list = []

        def gen_op_txt(font, size, x, y, rtxt):
            return f"/{font} {size:f} Tf 1 0 0 1 {x:f} {y:f} Tm [<{rtxt}>] TJ "

        def gen_op_line(x, y, xlen, ylen, linewidth):
            return f"ET q 1 0 0 1 {x:f} {y:f} cm [] 0 d 0 J {linewidth:f} w 0 0 m {xlen:f} {ylen:f} l S Q BT "

        def _char_adv(ch_str: str, sz: float) -> tuple[str, float]:
            f_ = None
            try:
                if f_ is None and self.fontmap["tiro"].to_unichr(ord(ch_str)) == ch_str:
                    f_ = "tiro"
            except Exception:
                pass
            if f_ is None:
                f_ = self.noto_name
            if f_ == self.noto_name:
                a_ = self.noto.char_lengths(ch_str, sz)[0]
            else:
                a_ = self.fontmap[f_].char_width(ord(ch_str)) * sz
            return f_, a_

        cls_end_x: dict[int, float] = {}
        # 确保目录标题段落在对应的引导点段落之前完成排版，以便准确获取标题结束横坐标
        order_ids = [i for i in range(len(news)) if i not in toc_dots_para_map] + [
            i for i in range(len(news)) if i in toc_dots_para_map
        ]
        para_ops_chunks: dict[int, list[str]] = {}

        for pid in order_ids:
            new = add_cjk_latin_spacing(news[pid])
            x: float = pstk[pid].x                      # 段落初始横坐标
            y: float = pstk[pid].y                      # 段落初始纵坐标
            x0: float = pstk[pid].x0                    # 段落左边界
            x1: float = pstk[pid].x1                    # 段落右边界
            height: float = pstk[pid].y1 - pstk[pid].y0 # 段落高度
            size: float = pstk[pid].size                # 段落字体大小
            brk: bool = pstk[pid].brk                   # 段落换行标记
            cstk: str = ""                              # 当前文字栈
            fcur: str = None                            # 当前字体 ID
            lidx = 0                                    # 记录换行次数
            tx = x
            fcur_ = fcur
            ptr = 0
            log.debug(f"< {y} {x} {x0} {x1} {size} {brk} > {sstk[pid]} | {new}")

            ops_vals: list[dict] = []

            if pid in toc_dots_para_map:
                meta = toc_dots_para_map[pid]
                title_end_x = cls_end_x.get(meta["title_cls"], 0.0)
                dot_chars: list[LTChar] = meta["dot_chars"]
                page_chars: list[LTChar] = meta["page_chars"]
                if dot_chars:
                    min_dot_x = (
                        title_end_x + size * 0.45
                        if title_end_x > 0
                        else dot_chars[0].x0
                    )
                    max_dot_x = (
                        page_chars[0].x0 - size * 0.35
                        if page_chars
                        else dot_chars[-1].x1
                    )
                    if title_end_x > 0 and len(dot_chars) >= 2 and min_dot_x < dot_chars[0].x0:
                        steps = [
                            dot_chars[i + 1].x0 - dot_chars[i].x0
                            for i in range(len(dot_chars) - 1)
                            if 1.5 <= (dot_chars[i + 1].x0 - dot_chars[i].x0) <= 30.0
                        ]
                        if steps:
                            step = float(np.median(steps))
                            tmpl = dot_chars[0]
                            tmpl_font = self.fontid[tmpl.font]
                            tmpl_rtxt = raw_string(tmpl_font, chr(tmpl.cid))
                            extra_xs: list[float] = []
                            cx_dot = dot_chars[0].x0 - step
                            while cx_dot >= min_dot_x:
                                extra_xs.append(cx_dot)
                                cx_dot -= step
                            for dx_pos in reversed(extra_xs):
                                ops_vals.append({
                                    "type": OpType.TEXT,
                                    "font": tmpl_font,
                                    "size": tmpl.size,
                                    "x": dx_pos,
                                    "dy": tmpl.y0 - y,
                                    "rtxt": tmpl_rtxt,
                                    "lidx": 0,
                                })
                    for vch in dot_chars:
                        if min_dot_x <= vch.x0 <= max_dot_x:
                            ops_vals.append({
                                "type": OpType.TEXT,
                                "font": self.fontid[vch.font],
                                "size": vch.size,
                                "x": vch.x0,
                                "dy": vch.y0 - y,
                                "rtxt": raw_string(self.fontid[vch.font], chr(vch.cid)),
                                "lidx": 0,
                            })
                for vch in page_chars:
                    ops_vals.append({
                        "type": OpType.TEXT,
                        "font": self.fontid[vch.font],
                        "size": vch.size,
                        "x": vch.x0,
                        "dy": vch.y0 - y,
                        "rtxt": raw_string(self.fontid[vch.font], chr(vch.cid)),
                        "lidx": 0,
                    })
                chunk_ops: list[str] = []
                for vals in ops_vals:
                    chunk_ops.append(
                        gen_op_txt(
                            vals["font"],
                            vals["size"],
                            vals["x"],
                            vals["dy"] + y,
                            vals["rtxt"],
                        )
                    )
                para_ops_chunks[pid] = chunk_ops
                continue

            # 若为目录标题行且翻译后宽度超出页码左侧边界，自适应微调字号避免撞上页码
            if pid in toc_title_para_ids and x1 > x + size:
                est_w = 0.0
                p_tmp = 0
                while p_tmp < len(new):
                    m_tmp = re.match(r"\{\s*v([\d\s]+)\}", new[p_tmp:], re.IGNORECASE)
                    if m_tmp:
                        p_tmp += len(m_tmp.group(0))
                        try:
                            vid_tmp = int(m_tmp.group(1).replace(" ", ""))
                            est_w += vlen[vid_tmp]
                        except Exception:
                            pass
                    else:
                        _, adv_tmp = _char_adv(new[p_tmp], size)
                        est_w += adv_tmp
                        p_tmp += 1
                avail_w = x1 - x
                if est_w > avail_w and est_w > 0:
                    size = max(size * 0.65, size * (avail_w / est_w) * 0.97)

            while ptr < len(new):
                vy_regex = re.match(
                    r"\{\s*v([\d\s]+)\}", new[ptr:], re.IGNORECASE
                )  # 匹配 {vn} 公式标记
                mod = 0  # 文字修饰符
                if vy_regex:  # 加载公式
                    ptr += len(vy_regex.group(0))
                    try:
                        vid = int(vy_regex.group(1).replace(" ", ""))
                        adv = vlen[vid]
                    except Exception:
                        continue  # 翻译器可能会自动补个越界的公式标记
                    if var[vid][-1].get_text() and unicodedata.category(var[vid][-1].get_text()[0]) in ["Lm", "Mn", "Sk"]:  # 文字修饰符
                        mod = var[vid][-1].width
                else:  # 加载文字
                    ch = new[ptr]
                    fcur_, adv = _char_adv(ch, size)
                    ptr += 1
                if (                                # 输出文字缓冲区
                    fcur_ != fcur                   # 1. 字体更新
                    or vy_regex                     # 2. 插入公式
                    or x + adv > x1 + 0.1 * size    # 3. 到达右边界（可能一整行都被符号化，这里需要考虑浮点误差）
                ):
                    if cstk:
                        ops_vals.append({
                            "type": OpType.TEXT,
                            "font": fcur,
                            "size": size,
                            "x": tx,
                            "dy": 0,
                            "rtxt": raw_string(fcur, cstk),
                            "lidx": lidx
                        })
                        cstk = ""
                if brk and x + adv > x1 + 0.1 * size:  # 到达右边界且原文段落存在换行
                    x = x0
                    lidx += 1
                if vy_regex:  # 插入公式
                    fix = 0
                    if fcur is not None:  # 段落内公式修正纵向偏移
                        fix = varf[vid]
                    for vch in var[vid]:  # 排版公式字符
                        vc = chr(vch.cid)
                        ops_vals.append({
                            "type": OpType.TEXT,
                            "font": self.fontid[vch.font],
                            "size": vch.size,
                            "x": x + vch.x0 - var[vid][0].x0,
                            "dy": fix + vch.y0 - var[vid][0].y0,
                            "rtxt": raw_string(self.fontid[vch.font], vc),
                            "lidx": lidx
                        })
                        if log.isEnabledFor(logging.DEBUG):
                            lstk.append(LTLine(0.1, (_x, _y), (x + vch.x0 - var[vid][0].x0, fix + y + vch.y0 - var[vid][0].y0)))
                            _x, _y = x + vch.x0 - var[vid][0].x0, fix + y + vch.y0 - var[vid][0].y0
                    for l in varl[vid]:  # 排版公式线条
                        if l.linewidth < 5:  # hack 有的文档会用粗线条当图片背景
                            ops_vals.append({
                                "type": OpType.LINE,
                                "x": l.pts[0][0] + x - var[vid][0].x0,
                                "dy": l.pts[0][1] + fix - var[vid][0].y0,
                                "linewidth": l.linewidth,
                                "xlen": l.pts[1][0] - l.pts[0][0],
                                "ylen": l.pts[1][1] - l.pts[0][1],
                                "lidx": lidx
                            })
                else:  # 插入文字缓冲区
                    if not cstk:  # 单行开头
                        tx = x
                        if x == x0 and ch == " ":  # 消除段落换行空格
                            adv = 0
                        else:
                            cstk += ch
                    else:
                        cstk += ch
                adv -= mod # 文字修饰符
                fcur = fcur_
                x += adv
                if log.isEnabledFor(logging.DEBUG):
                    lstk.append(LTLine(0.1, (_x, _y), (x, y)))
                    _x, _y = x, y
            # 处理结尾
            if cstk:
                ops_vals.append({
                    "type": OpType.TEXT,
                    "font": fcur,
                    "size": size,
                    "x": tx,
                    "dy": 0,
                    "rtxt": raw_string(fcur, cstk),
                    "lidx": lidx
                })

            if pid < len(para_cls_list) and para_cls_list[pid] > 0:
                cls_end_x[para_cls_list[pid]] = x

            line_height = default_line_height

            while (lidx + 1) * size * line_height > height and line_height >= 1:
                line_height -= 0.05

            chunk_ops = []
            for vals in ops_vals:
                if vals["type"] == OpType.TEXT:
                    chunk_ops.append(gen_op_txt(vals["font"], vals["size"], vals["x"], vals["dy"] + y - vals["lidx"] * size * line_height, vals["rtxt"]))
                elif vals["type"] == OpType.LINE:
                    chunk_ops.append(gen_op_line(vals["x"], vals["dy"] + y - vals["lidx"] * size * line_height, vals["xlen"], vals["ylen"], vals["linewidth"]))
            para_ops_chunks[pid] = chunk_ops

        for pid in range(len(news)):
            ops_list.extend(para_ops_chunks.get(pid, []))

        for l in lstk:  # 排版全局线条
            if l.linewidth < 5:  # hack 有的文档会用粗线条当图片背景
                ops_list.append(gen_op_line(l.pts[0][0], l.pts[0][1], l.pts[1][0] - l.pts[0][0], l.pts[1][1] - l.pts[0][1], l.linewidth))

        ops = f"BT {''.join(ops_list)}ET "
        if self.perf:
            self.perf.add("typesetting", perf_counter() - started)
        return ops


class OpType(Enum):
    TEXT = "text"
    LINE = "line"
