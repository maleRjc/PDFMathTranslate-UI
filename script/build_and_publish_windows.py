#!/usr/bin/env python3
"""Build, sign, package and publish Windows desktop release of PDFMathTranslate-UI.

References AiReadCode (G:/AiReadCode/AiReadCode) signing and release workflows.
"""

from __future__ import annotations

import glob
import hashlib
import json
import os
import shutil
import ssl
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

VERSION = "1.9.12"
TAG_NAME = f"v{VERSION}"
REPO_OWNER = "maleRjc"
REPO_NAME = "PDFMathTranslate-UI"
CERT_THUMBPRINT = "FEEFF01058543A90FD2119C07947368FD7A03494"
TIMESTAMP_URL = "http://timestamp.sectigo.com"
SIGNTOOL_PATH = r"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEP_BUILD_DIR = PROJECT_ROOT / "dep_build"
BUILD_DIR = PROJECT_ROOT / "build"
PACKAGE_NAME = f"PDFMathTranslate-{TAG_NAME}-windows-x64"
STAGE_DIR = BUILD_DIR / PACKAGE_NAME
DIST_DIR = PROJECT_ROOT / "dist" / "release"
ZIP_OUTPUT = DIST_DIR / f"{PACKAGE_NAME}.zip"


def log(msg: str) -> None:
    print(f"[*] {msg}", flush=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def get_github_token() -> str:
    """Retrieve GitHub token from git credentials or environment."""
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


def ensure_dependencies() -> None:
    """Ensure PyStand and Python embed zip are downloaded and extracted in dep_build."""
    DEP_BUILD_DIR.mkdir(parents=True, exist_ok=True)
    pystand_dir = DEP_BUILD_DIR / "PyStand"
    py_embed_dir = DEP_BUILD_DIR / "python_embed"

    proxy_args = ["-x", "http://127.0.0.1:7890"]

    if not (pystand_dir / "PyStand-x64-GUI" / "PyStand.exe").exists():
        log("Downloading PyStand release...")
        zip_path = DEP_BUILD_DIR / "PyStand.zip"
        subprocess.run(
            [
                "curl.exe",
                *proxy_args,
                "-sL",
                "https://github.com/skywind3000/PyStand/releases/download/1.1.4/PyStand-v1.1.4-exe.zip",
                "-o",
                str(zip_path),
            ],
            check=True,
        )
        shutil.unpack_archive(zip_path, pystand_dir)

    if not (py_embed_dir / "python312.dll").exists():
        log("Downloading Python 3.12 embed amd64...")
        zip_path = DEP_BUILD_DIR / "python.zip"
        subprocess.run(
            [
                "curl.exe",
                *proxy_args,
                "-sL",
                "https://www.python.org/ftp/python/3.12.9/python-3.12.9-embed-amd64.zip",
                "-o",
                str(zip_path),
            ],
            check=True,
        )
        shutil.unpack_archive(zip_path, py_embed_dir)


def prepare_stage_directory() -> None:
    """Assemble the complete standalone application directory."""
    log(f"Assembling package directory: {STAGE_DIR}")
    if STAGE_DIR.exists():
        shutil.rmtree(STAGE_DIR)
    STAGE_DIR.mkdir(parents=True)

    runtime_dir = STAGE_DIR / "runtime"
    runtime_dir.mkdir()
    py_embed_dir = DEP_BUILD_DIR / "python_embed"
    for item in py_embed_dir.iterdir():
        if item.is_file():
            shutil.copy2(item, runtime_dir / item.name)

    # Configure python312._pth to enable site-packages
    pth_file = runtime_dir / "python312._pth"
    pth_content = "python312.zip\n.\n..\n../site-packages\nimport site\n"
    pth_file.write_text(pth_content, encoding="utf-8")

    # Copy site-packages from local .venv
    venv_site = PROJECT_ROOT / ".venv" / "Lib" / "site-packages"
    dest_site = STAGE_DIR / "site-packages"
    log(f"Copying site-packages from {venv_site}...")
    shutil.copytree(
        venv_site,
        dest_site,
        ignore=shutil.ignore_patterns(
            "__pycache__",
            "*.pyc",
            "__editable___pdf2zh*",
            "_virtualenv*",
        ),
    )

    # Copy our current pdf2zh package directly into site-packages/pdf2zh
    pdf2zh_src = PROJECT_ROOT / "pdf2zh"
    dest_pdf2zh = dest_site / "pdf2zh"
    if dest_pdf2zh.exists():
        shutil.rmtree(dest_pdf2zh)
    log(f"Copying live pdf2zh package into {dest_pdf2zh}...")
    shutil.copytree(
        pdf2zh_src,
        dest_pdf2zh,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )

    # Copy app icon
    icon_src = PROJECT_ROOT / "assets" / "app_icon.ico"
    if icon_src.exists():
        shutil.copy2(icon_src, STAGE_DIR / "app_icon.ico")

    # Copy PyStand launchers
    pystand_dir = DEP_BUILD_DIR / "PyStand"
    gui_exe = pystand_dir / "PyStand-x64-GUI" / "PyStand.exe"
    cli_exe = pystand_dir / "PyStand-x64-CLI" / "PyStand.exe"

    shutil.copy2(gui_exe, STAGE_DIR / "PDFMathTranslate.exe")
    shutil.copy2(cli_exe, STAGE_DIR / "pdf2zh.exe")

    # PyStand initialization scripts with explicit sys.path setup and error handling
    int_prefix = (
        "import sys\n"
        "import os\n"
        "import multiprocessing\n"
        "base_dir = os.path.dirname(os.path.abspath(__file__))\n"
        "site_dir = os.path.join(base_dir, 'site-packages')\n"
        "if site_dir not in sys.path:\n"
        "    sys.path.insert(0, site_dir)\n"
        "if base_dir not in sys.path:\n"
        "    sys.path.insert(0, base_dir)\n"
    )

    gui_int = STAGE_DIR / "PDFMathTranslate.int"
    gui_int.write_text(
        int_prefix
        + "try:\n"
        + "    from pdf2zh import ensure_valid_std_streams\n"
        + "    ensure_valid_std_streams()\n"
        + "    from pdf2zh.desktop_ui import main\n"
        + "    if __name__ == '__main__':\n"
        + "        multiprocessing.freeze_support()\n"
        + "        sys.exit(main())\n"
        + "except Exception as e:\n"
        + "    import traceback, ctypes\n"
        + "    err_msg = traceback.format_exc()\n"
        + "    try:\n"
        + "        with open(os.path.join(base_dir, 'error.log'), 'w', encoding='utf-8') as f:\n"
        + "            f.write(err_msg)\n"
        + "    except Exception: pass\n"
        + "    ctypes.windll.user32.MessageBoxW(0, f'PDFMathTranslate 启动失败:\\n\\n{err_msg}', 'PDFMathTranslate 错误', 0x10)\n"
        + "    sys.exit(1)\n",
        encoding="utf-8",
    )

    cli_int = STAGE_DIR / "pdf2zh.int"
    cli_int.write_text(
        int_prefix
        + "from pdf2zh import ensure_valid_std_streams\n"
        + "from pdf2zh.pdf2zh import main\n\n"
        + "if __name__ == '__main__':\n"
        + "    multiprocessing.freeze_support()\n"
        + "    ensure_valid_std_streams()\n"
        + "    sys.exit(main())\n",
        encoding="utf-8",
    )

    fallback_int = STAGE_DIR / "_pystand_static.int"
    fallback_int.write_text(gui_int.read_text(encoding="utf-8"), encoding="utf-8")

    # Copy convenient batch launcher
    bat_src = PROJECT_ROOT / "启动PDF翻译桌面版.bat"
    if bat_src.exists():
        shutil.copy2(bat_src, STAGE_DIR / "启动PDF翻译桌面版.bat")

    log("Stage directory assembled successfully.")


def sign_executables() -> None:
    """Sign all executables and DLLs in the stage directory using signtool.exe."""
    if not os.path.exists(SIGNTOOL_PATH):
        raise FileNotFoundError(f"signtool.exe not found at {SIGNTOOL_PATH}")

    targets: list[Path] = [
        STAGE_DIR / "PDFMathTranslate.exe",
        STAGE_DIR / "pdf2zh.exe",
        STAGE_DIR / "runtime" / "python.exe",
        STAGE_DIR / "runtime" / "pythonw.exe",
    ]

    log(f"Signing {len(targets)} executable binaries with certificate {CERT_THUMBPRINT}...")
    for target in targets:
        if not target.exists():
            continue
        log(f"  Signing: {target.name}")
        cmd = [
            SIGNTOOL_PATH,
            "sign",
            "/sha1",
            CERT_THUMBPRINT,
            "/fd",
            "sha256",
            "/tr",
            TIMESTAMP_URL,
            "/td",
            "sha256",
            str(target),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            log(f"  Warning: signtool failed for {target.name}: {res.stderr or res.stdout}")
        else:
            log(f"  Signed successfully: {target.name}")

    # Verify signature
    check_ps = f"Get-AuthenticodeSignature '{STAGE_DIR / 'PDFMathTranslate.exe'}' | Select-Object Status, StatusMessage"
    res = subprocess.run(["powershell", "-Command", check_ps], capture_output=True, text=True)
    log(f"Authenticode Verification: {res.stdout.strip()}")


def create_zip_archive() -> Path:
    """Create ZIP archive of the staged directory."""
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    if ZIP_OUTPUT.exists():
        ZIP_OUTPUT.unlink()

    log(f"Creating release archive: {ZIP_OUTPUT}...")
    t0 = time.time()

    with zipfile.ZipFile(ZIP_OUTPUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for root, dirs, files in os.walk(STAGE_DIR):
            for file in files:
                p = Path(root) / file
                rel_p = p.relative_to(STAGE_DIR.parent)
                zf.write(p, arcname=str(rel_p))

    size_mb = ZIP_OUTPUT.stat().st_size / (1024 * 1024)
    log(f"Created {ZIP_OUTPUT.name} ({size_mb:.2f} MB) in {time.time() - t0:.1f}s")
    return ZIP_OUTPUT


def update_sha256sums() -> Path:
    """Calculate and write SHA256 checksums."""
    sha_file = DIST_DIR / "SHA256SUMS.txt"
    sums = {}
    if sha_file.exists():
        for line in sha_file.read_text(encoding="utf-8").splitlines():
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                sums[parts[1].strip()] = parts[0].strip()

    sums[ZIP_OUTPUT.name] = sha256_file(ZIP_OUTPUT)

    content = "\n".join(f"{sums[name]}  {name}" for name in sorted(sums)) + "\n"
    sha_file.write_text(content, encoding="utf-8")
    log(f"Updated {sha_file.name}:\n{content.strip()}")
    return sha_file


def upload_to_github_release(files_to_upload: list[Path]) -> None:
    """Upload built release assets to the GitHub Release via GitHub REST API."""
    token = get_github_token()
    ctx = ssl._create_unverified_context()

    # Install proxy handler for GitHub API and asset uploads
    proxy_handler = urllib.request.ProxyHandler(
        {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890",
        }
    )
    https_handler = urllib.request.HTTPSHandler(context=ctx)
    opener = urllib.request.build_opener(proxy_handler, https_handler)
    urllib.request.install_opener(opener)

    # 1. Get release info
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/tags/{TAG_NAME}"
    headers = {
        "User-Agent": "PDFMathTranslate-Packager",
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx) as resp:
        rel_data = json.loads(resp.read().decode())

    release_id = rel_data["id"]
    existing_assets = {a["name"]: a["id"] for a in rel_data.get("assets", [])}
    log(f"Found GitHub Release {TAG_NAME} (ID: {release_id}) with {len(existing_assets)} existing assets.")

    for file_path in files_to_upload:
        fname = file_path.name
        fsize = file_path.stat().st_size
        fsize_mb = fsize / (1024 * 1024)

        # Delete existing asset with same name if any
        if fname in existing_assets:
            aid = existing_assets[fname]
            log(f"Deleting older asset '{fname}' (ID: {aid})...")
            del_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/assets/{aid}"
            del_req = urllib.request.Request(del_url, headers=headers, method="DELETE")
            try:
                with urllib.request.urlopen(del_req, context=ctx):
                    pass
            except Exception as e:
                log(f"Warning: delete failed: {e}")

        # Upload asset
        upload_endpoint = f"https://uploads.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/{release_id}/assets?name={urllib.parse.quote(fname)}"
        log(f"Uploading {fname} ({fsize_mb:.2f} MB) to GitHub Release...")

        content_type = "application/zip" if fname.endswith(".zip") else "text/plain"
        upload_headers = {
            "User-Agent": "PDFMathTranslate-Packager",
            "Authorization": f"token {token}",
            "Content-Type": content_type,
            "Content-Length": str(fsize),
        }

        with open(file_path, "rb") as f:
            up_req = urllib.request.Request(
                upload_endpoint,
                data=f,
                headers=upload_headers,
                method="POST",
            )
            t_start = time.time()
            with urllib.request.urlopen(up_req, context=ctx) as up_resp:
                res_data = json.loads(up_resp.read().decode())
                elapsed = time.time() - t_start
                download_url = res_data.get("browser_download_url")
                log(f"Successfully uploaded {fname} in {elapsed:.1f}s!")
                log(f"  Download URL: {download_url}")


def main() -> None:
    print("=" * 60)
    print("  PDFMathTranslate-UI Windows Signed Release Builder")
    print("=" * 60)

    t0 = time.time()
    ensure_dependencies()
    prepare_stage_directory()
    sign_executables()
    zip_path = create_zip_archive()
    sha_path = update_sha256sums()
    upload_to_github_release([zip_path, sha_path])

    print("=" * 60)
    print(f"Windows release package built, signed, and published in {time.time() - t0:.1f}s!")
    print("=" * 60)


if __name__ == "__main__":
    main()
