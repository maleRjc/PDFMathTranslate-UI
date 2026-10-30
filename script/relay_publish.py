#!/usr/bin/env python3
"""Publish signed Windows setup installer to GitHub Release v1.9.12 via high-speed relay server."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
import paramiko

HOST = "47.120.26.227"
USER = "root"
PASS = "Rjc_lihui0817"

VERSION = "1.9.12"
TAG_NAME = f"v{VERSION}"
REPO_OWNER = "maleRjc"
REPO_NAME = "PDFMathTranslate-UI"
RELEASE_ID = 427556949

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = PROJECT_ROOT / "dist" / "release"


def log(msg: str) -> None:
    print(f"[*] {msg}", flush=True)


def get_github_token() -> str:
    if token := os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"):
        return token
    try:
        p = subprocess.run(
            ["git", "credential", "fill"],
            input=b"protocol=https\nhost=github.com\n",
            capture_output=True,
            check=True,
        )
        lines = p.stdout.decode().splitlines()
        creds = dict(line.split("=", 1) for line in lines if "=" in line)
        if token := creds.get("password"):
            return token
    except Exception as e:
        log(f"Warning: could not get git credential: {e}")
    raise RuntimeError("GitHub access token not found in git credentials or environment")


def progress_callback(transferred: int, total: int) -> None:
    percent = (transferred / total) * 100
    mb_transferred = transferred / (1024 * 1024)
    mb_total = total / (1024 * 1024)
    sys.stdout.write(f"\r    Uploading: {mb_transferred:.2f}MB / {mb_total:.2f}MB ({percent:.1f}%)")
    sys.stdout.flush()


def main() -> None:
    token = get_github_token()

    setup_file = DIST_DIR / "PDFMathTranslate-v1.9.12-windows-x64-setup.exe"
    alias_file = DIST_DIR / "PDFMathTranslate_1.9.12_x64-setup.exe"

    if not setup_file.exists():
        sys.exit(f"Error: {setup_file} does not exist!")

    print("=" * 60)
    print("  PDFMathTranslate-UI: Windows Signed Setup Publishing")
    print("=" * 60)

    log(f"Connecting to relay server {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS, timeout=30)
    sftp = client.open_sftp()
    log("Connected to relay server.")

    remote_setup_path = "/tmp/PDFMathTranslate-v1.9.12-windows-x64-setup.exe"

    log(f"Uploading installer to relay server ({setup_file.stat().st_size / (1024*1024):.2f} MB)...")
    t0 = time.time()
    sftp.put(str(setup_file), remote_setup_path, callback=progress_callback)
    print()
    log(f"Relay upload completed in {time.time() - t0:.1f}s!")
    sftp.close()

    # Create remote hardlink for alias
    remote_alias_path = "/tmp/PDFMathTranslate_1.9.12_x64-setup.exe"
    client.exec_command(f"cp -l {remote_setup_path} {remote_alias_path}")

    remote_sha_path = "/tmp/SHA256SUMS.txt"
    sha_file = DIST_DIR / "SHA256SUMS.txt"
    sftp = client.open_sftp()
    sftp.put(str(sha_file), remote_sha_path)
    sftp.close()

    # Remote script to upload to GitHub Release via Linux curl
    remote_script = f"""\
import json
import subprocess
import urllib.parse
import sys
import time

TOKEN = "{token}"
RELEASE_ID = {RELEASE_ID}
REPO_OWNER = "{REPO_OWNER}"
REPO_NAME = "{REPO_NAME}"

# 1. Fetch release assets to delete any conflicting asset
cmd = [
    "curl", "-sL",
    "-H", f"Authorization: token {{TOKEN}}",
    "-H", "Accept: application/vnd.github.v3+json",
    f"https://api.github.com/repos/{{REPO_OWNER}}/{{REPO_NAME}}/releases/{{RELEASE_ID}}"
]
res = subprocess.run(cmd, capture_output=True, text=True, check=True)
rel_data = json.loads(res.stdout)
existing = {{a["name"]: a["id"] for a in rel_data.get("assets", [])}}

files = [
    ("{setup_file.name}", "{remote_setup_path}", "application/vnd.microsoft.portable-executable"),
    ("{alias_file.name}", "{remote_alias_path}", "application/vnd.microsoft.portable-executable"),
    ("SHA256SUMS.txt", "{remote_sha_path}", "text/plain"),
]

for name, path, ctype in files:
    if name in existing:
        aid = existing[name]
        print(f"Deleting older asset {{name}} (ID: {{aid}})...", flush=True)
        subprocess.run([
            "curl", "-sL", "-X", "DELETE",
            "-H", f"Authorization: token {{TOKEN}}",
            "-H", "Accept: application/vnd.github.v3+json",
            f"https://api.github.com/repos/{{REPO_OWNER}}/{{REPO_NAME}}/releases/assets/{{aid}}"
        ], check=True)

    endpoint = f"https://uploads.github.com/repos/{{REPO_OWNER}}/{{REPO_NAME}}/releases/{{RELEASE_ID}}/assets?name={{urllib.parse.quote(name)}}"
    print(f"Uploading {{name}} to GitHub Release via Linux server...", flush=True)
    t_start = time.time()
    up_cmd = [
        "curl", "-sL",
        "-X", "POST",
        "-H", f"Authorization: token {{TOKEN}}",
        "-H", f"Content-Type: {{ctype}}",
        "--data-binary", f"@{{path}}",
        endpoint
    ]
    up_res = subprocess.run(up_cmd, capture_output=True, text=True, check=True)
    elapsed = time.time() - t_start
    try:
        data = json.loads(up_res.stdout)
        print(f"Uploaded {{name}} in {{elapsed:.1f}}s! State: {{data.get('state')}}, URL: {{data.get('browser_download_url')}}", flush=True)
    except Exception:
        print(f"Uploaded {{name}} in {{elapsed:.1f}}s, response: {{up_res.stdout[:200]}}", flush=True)

print("All files uploaded successfully from server!", flush=True)
"""

    remote_py_path = "/tmp/do_github_upload.py"
    sftp = client.open_sftp()
    with sftp.file(remote_py_path, "w") as f:
        f.write(remote_script)
    sftp.close()

    log("Executing remote upload script on relay server...")
    stdin, stdout, stderr = client.exec_command(f"python3 -u {remote_py_path}")
    for line in iter(stdout.readline, ""):
        print(f"    [Remote] {line.strip()}", flush=True)

    err = stderr.read().decode()
    if err:
        log(f"Remote Stderr: {err}")

    # Cleanup remote temporary files
    log("Cleaning up temporary files on server...")
    client.exec_command(f"rm -f {remote_setup_path} {remote_alias_path} {remote_py_path}")
    client.close()

    # Update release body locally
    log("Updating GitHub Release notes (Body)...")
    updated_body = """\
> **📌 项目来源与开源致谢 (Upstream Attribution)**：本项目参考自开源项目 [PDFMathTranslate/PDFMathTranslate](https://github.com/PDFMathTranslate/PDFMathTranslate)，为学术与 PDF 文档排版还原原生桌面客户端（PySide6 UI），排版增强遵循 AGPL-3.0 开源协议。

## 🌟 主要改进 (Highlights)
1. **原生跨平台客户端 (PySide6 Desktop UI)**
   - 🌟 **集成 24 种 AI 翻译模型**：可视化配置 DeepSeek、OpenAI、Gemini、阿里 Qwen-MT、智谱 GLM、ModelScope、Ollama 本地模型、自定义 OpenAI 兼容接口等，支持一键设为默认。
   - 🌟 **双语/纯译文/原文一键 PDF 预览阅读器**：支持拖拽 PDF / Word 文档或文件列表，支持 arXiv 论文在线翻译与下载。
   - 🌟 **内置交互式使用说明与常见排错指南 (User Guide)**。
2. **10 种界面实时无缝切换 (Real-time 10-Language UI)**
   - 涵盖：**简体中文 (zh)**、**繁体中文 (zh-TW)**、**English (en)**、**日本語 (ja)**、**한국어 (ko)**、**Français (fr)**、**Deutsch (de)**、**Русский (ru)**、**Español (es)**、**Italiano (it)**。
3. **PDF 文档大纲 (TOC / 目录书签) 排版高保真还原**
   - **文档大纲自动翻译**：精准提取 PDF 原始书签/大纲（Outline / TOC），翻译并重写入纯译文 (Mono) 与双语 (Dual) PDF，保留完整层级与跳转坐标。
   - **页面目录排版修复**：自动识别点线（. . . . 42）目录行，针对性修复换行排版，动态修剪/展开引导点并右对齐页码，完美保持原坐标精度。
4. **跨页断行与页脚行号保护**
   - 自动检测并修复跨页提示（如 continued from previous page / continues on next page）以及行号混入，保护原文原位，彻底解决漏页断页痛点。
5. **支持自定义推广页与结尾页注入**
   - 生成的 PDF 末尾支持自定义自动添加推广页与超链接。

## 📦 发布包说明 (Release Assets)
- **PDFMathTranslate-v1.9.12-windows-x64-setup.exe** (推荐安装程序，兼容别名：`PDFMathTranslate_1.9.12_x64-setup.exe`)：
  - Windows 64位 原生桌面安装包（Setup Installer）。
  - **已使用权威数字证书签名（签名者：武汉矩阵力量科技有限公司 / Certum Code Signing CA，时间戳：Sectigo）**，完全杜绝 Windows 恶意软件拦截警报。
  - 自动创建桌面与开始菜单快捷方式，支持 Windows 控制面板/设置中心完整卸载。
- **PDFMathTranslate-v1.9.12-windows-x64.zip**：
  - Windows 64位 便携版（绿色免安装，解压即用），内置 Python 3.12 独立运行时，所有二进制程序均已完成数字签名。
- **PDFMathTranslate-v1.9.12-macOS-arm64.dmg**：
  - macOS (Apple Silicon) 安装包，已使用 **Apple Developer ID Application** 证书签名与公证。
- **PDFMathTranslate-v1.9.12-macOS-arm64.zip**：macOS 便携版 .app 压缩包。
- **pdf2zh-1.9.12-py3-none-any.whl / pdf2zh-1.9.12.tar.gz**：Python 安装包与源码包。

## 🔐 校验和 (SHA-256 Checksums)
完整文件 SHA-256 校验和见 `SHA256SUMS.txt` 与 `SHA256SUMS-python.txt`。
"""

    git_curl = r"C:\Program Files\Git\mingw64\bin\curl.exe"
    patch_payload = json.dumps({"body": updated_body})
    subprocess.run(
        [
            git_curl,
            "-x",
            "http://127.0.0.1:7890",
            "-sL",
            "-X",
            "PATCH",
            "-H",
            f"Authorization: token {token}",
            "-H",
            "Content-Type: application/json",
            "-d",
            patch_payload,
            f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/{RELEASE_ID}",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    log("Release body updated successfully!")

    print("=" * 60)
    print("SUCCESS: Windows Signed Setup Installer successfully published to GitHub Release!")
    print("=" * 60)


if __name__ == "__main__":
    main()
