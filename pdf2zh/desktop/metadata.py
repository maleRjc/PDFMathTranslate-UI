"""Metadata, provider definitions, and settings helpers for PDFMathTranslate Desktop UI."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from pdf2zh.config import ConfigManager
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
    X302AITranslator,
    XinferenceTranslator,
    ZhipuTranslator,
)

# Ordered mapping of display name -> Translator class
SERVICE_MAP: dict[str, type[BaseTranslator]] = {
    "OpenAI": OpenAITranslator,
    "DeepSeek": DeepseekTranslator,
    "Gemini": GeminiTranslator,
    "Ali Qwen-Translation": QwenMtTranslator,
    "Silicon (硅基流动)": SiliconTranslator,
    "Zhipu (智谱 GLM)": ZhipuTranslator,
    "ModelScope (魔搭)": ModelScopeTranslator,
    "OpenAI-liked (自定义兼容接口)": OpenAIlikedTranslator,
    "Ollama (本地模型)": OllamaTranslator,
    "AzureOpenAI": AzureOpenAITranslator,
    "Grok (xAI)": GrokTranslator,
    "Groq": GroqTranslator,
    "MiniMax": MiniMaxTranslator,
    "302.AI": X302AITranslator,
    "Xinference": XinferenceTranslator,
    "Dify": DifyTranslator,
    "AnythingLLM": AnythingLLMTranslator,
    "Google": GoogleTranslator,
    "Bing": BingTranslator,
    "DeepL": DeepLTranslator,
    "DeepLX": DeepLXTranslator,
    "Azure Translator": AzureTranslator,
    "Tencent (腾讯云翻译)": TencentTranslator,
    "Argos Translate": ArgosTranslator,
}

# Reverse lookup from translator.name (e.g. "openai") to UI key
TRANSLATOR_NAME_TO_KEY: dict[str, str] = {
    cls.name: key for key, cls in SERVICE_MAP.items()
}

# Provider metadata for richer UI display (category, description, doc url, model suggestions)
PROVIDER_METADATA: dict[str, dict[str, Any]] = {
    "OpenAI": {
        "category": "AI 大模型",
        "desc": "OpenAI 官方接口或兼容代理，支持 GPT-4o / GPT-4.1 系列模型。",
        "url": "https://platform.openai.com/api-keys",
        "models": ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "gpt-4.1", "o3-mini"],
    },
    "DeepSeek": {
        "category": "AI 大模型",
        "desc": "DeepSeek 官方 API，性价比极高，非常适合学术论文中英互译。",
        "url": "https://platform.deepseek.com/api_keys",
        "models": ["deepseek-chat", "deepseek-reasoner"],
    },
    "Gemini": {
        "category": "AI 大模型",
        "desc": "Google Gemini OpenAI 兼容接口，上下文大、速度快。",
        "url": "https://aistudio.google.com/app/apikey",
        "models": [
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-2.5-flash-preview-04-17",
        ],
    },
    "Ali Qwen-Translation": {
        "category": "AI 大模型",
        "desc": "阿里云百炼 Qwen-MT 专业翻译大模型，针对科技文献专门优化。",
        "url": "https://bailian.console.aliyun.com/",
        "models": ["qwen-mt-turbo", "qwen-mt-plus"],
    },
    "Silicon (硅基流动)": {
        "category": "AI 大模型",
        "desc": "SiliconFlow 云端推理平台，提供 Qwen2.5、DeepSeek-V3 等多种模型。",
        "url": "https://cloud.siliconflow.cn/account/ak",
        "models": [
            "Qwen/Qwen2.5-7B-Instruct",
            "Qwen/Qwen2.5-32B-Instruct",
            "Qwen/Qwen2.5-72B-Instruct",
            "deepseek-ai/DeepSeek-V3",
        ],
    },
    "Zhipu (智谱 GLM)": {
        "category": "AI 大模型",
        "desc": "智谱清言开放平台，glm-4-flash 免费且速度快。",
        "url": "https://open.bigmodel.cn/usercenter/apikeys",
        "models": ["glm-4-flash", "glm-4-air", "glm-4-plus"],
    },
    "ModelScope (魔搭)": {
        "category": "AI 大模型",
        "desc": "魔搭社区 API-Inference 免费推理接口。",
        "url": "https://modelscope.cn/my/myaccesstoken",
        "models": [
            "Qwen/Qwen2.5-32B-Instruct",
            "Qwen/Qwen2.5-72B-Instruct",
            "deepseek-ai/DeepSeek-V3",
        ],
    },
    "OpenAI-liked (自定义兼容接口)": {
        "category": "AI 大模型",
        "desc": "支持所有兼容 OpenAI Chat Completions 协议的第三方中转、OneAPI、vLLM、LM Studio 等。",
        "url": "",
        "models": ["gpt-4o-mini", "deepseek-chat", "qwen-plus", "claude-3-5-sonnet"],
    },
    "Ollama (本地模型)": {
        "category": "本地部署",
        "desc": "使用本地运行的 Ollama 服务，无需 API Key，保护数据隐私。",
        "url": "https://ollama.com/",
        "models": ["gemma2", "qwen2.5:7b", "qwen2.5:14b", "llama3.1:8b"],
    },
    "AzureOpenAI": {
        "category": "AI 大模型",
        "desc": "微软 Azure OpenAI 企业级服务。",
        "url": "https://portal.azure.com/",
        "models": ["gpt-4o-mini", "gpt-4o"],
    },
    "Grok (xAI)": {
        "category": "AI 大模型",
        "desc": "xAI Grok 大模型接口。",
        "url": "https://console.x.ai/",
        "models": ["grok-2-1212", "grok-3-mini-beta", "grok-3-beta"],
    },
    "Groq": {
        "category": "AI 大模型",
        "desc": "Groq LPU 极速推理平台。",
        "url": "https://console.groq.com/keys",
        "models": ["llama-3-3-70b-versatile", "gemma2-9b-it"],
    },
    "MiniMax": {
        "category": "AI 大模型",
        "desc": "MiniMax 开放平台大模型。",
        "url": "https://platform.minimaxi.com/",
        "models": ["MiniMax-M2.7", "abab6.5s-chat"],
    },
    "302.AI": {
        "category": "AI 大模型",
        "desc": "302.AI 聚合 AI 平台。",
        "url": "https://302.ai/",
        "models": ["Gemma-7B", "gpt-4o-mini", "deepseek-chat"],
    },
    "Xinference": {
        "category": "本地部署",
        "desc": "Xorbits Inference 本地/私有化模型推理服务。",
        "url": "https://inference.readthedocs.io/",
        "models": ["gemma-2-it", "qwen2.5-instruct"],
    },
    "Dify": {
        "category": "AI 应用编排",
        "desc": "连接自建或云端 Dify 工作流/应用 API。",
        "url": "https://dify.ai/",
        "models": [],
    },
    "AnythingLLM": {
        "category": "AI 应用编排",
        "desc": "连接 AnythingLLM 本地或私有知识库工作区 API。",
        "url": "https://anythingllm.com/",
        "models": [],
    },
    "Google": {
        "category": "传统机器翻译",
        "desc": "Google 网页免费翻译接口（需要网络能访问 Google）。",
        "url": "",
        "models": [],
    },
    "Bing": {
        "category": "传统机器翻译",
        "desc": "微软必应免费翻译接口，国内可直接访问，无需配置密钥。",
        "url": "",
        "models": [],
    },
    "DeepL": {
        "category": "传统机器翻译",
        "desc": "DeepL 官方 API，需填写 DeepL Auth Key。",
        "url": "https://www.deepl.com/pro-api",
        "models": [],
    },
    "DeepLX": {
        "category": "传统机器翻译",
        "desc": "DeepLX 自建或第三方免 Key 服务端接口。",
        "url": "",
        "models": [],
    },
    "Azure Translator": {
        "category": "传统机器翻译",
        "desc": "微软 Azure 认知服务文本翻译接口。",
        "url": "https://portal.azure.com/",
        "models": [],
    },
    "Tencent (腾讯云翻译)": {
        "category": "传统机器翻译",
        "desc": "腾讯云机器翻译 TMT，需要 SecretId 和 SecretKey。",
        "url": "https://console.cloud.tencent.com/cam/capi",
        "models": [],
    },
    "Argos Translate": {
        "category": "本地部署",
        "desc": "Argos 离线开源神经网络翻译（需安装 argostranslate 扩展）。",
        "url": "",
        "models": [],
    },
}

# Friendly labels and placeholders for environment variable fields
ENV_FIELD_INFO: dict[str, dict[str, str]] = {
    "OPENAI_BASE_URL": {
        "label": "API 接口地址 (Base URL)",
        "placeholder": "https://api.openai.com/v1",
    },
    "OPENAI_API_KEY": {
        "label": "API 密钥 (API Key)",
        "placeholder": "sk-...",
        "secret": "true",
    },
    "OPENAI_MODEL": {
        "label": "模型名称 (Model)",
        "placeholder": "gpt-4o-mini",
        "is_model": "true",
    },
    "OPENAI_STREAM": {
        "label": "流式输出 (Stream)",
        "placeholder": "true 或 false",
    },
    "OPENAI_STOP_TOKENS": {
        "label": "停止词 (Stop Tokens)",
        "placeholder": "选填，多个以空格分隔",
    },
    "OPENAI_MAX_TOKENS": {
        "label": "最大生成 Token 数 (Max Tokens)",
        "placeholder": "-1 表示默认不限制",
    },
    "DEEPSEEK_API_KEY": {
        "label": "DeepSeek API Key",
        "placeholder": "sk-...",
        "secret": "true",
    },
    "DEEPSEEK_MODEL": {
        "label": "模型名称 (Model)",
        "placeholder": "deepseek-chat",
        "is_model": "true",
    },
    "GEMINI_API_KEY": {
        "label": "Gemini API Key",
        "placeholder": "AIzaSy...",
        "secret": "true",
    },
    "GEMINI_MODEL": {
        "label": "模型名称 (Model)",
        "placeholder": "gemini-1.5-flash",
        "is_model": "true",
    },
    "ALI_API_KEY": {
        "label": "阿里云百炼 API Key",
        "placeholder": "sk-...",
        "secret": "true",
    },
    "ALI_MODEL": {
        "label": "模型名称 (Model)",
        "placeholder": "qwen-mt-turbo",
        "is_model": "true",
    },
    "ALI_DOMAINS": {
        "label": "领域提示描述 (Domains)",
        "placeholder": "Scientific paper translation...",
    },
    "SILICON_API_KEY": {
        "label": "硅基流动 API Key",
        "placeholder": "sk-...",
        "secret": "true",
    },
    "SILICON_MODEL": {
        "label": "模型名称 (Model)",
        "placeholder": "Qwen/Qwen2.5-7B-Instruct",
        "is_model": "true",
    },
    "ZHIPU_API_KEY": {
        "label": "智谱 API Key",
        "placeholder": "填写智谱开放平台 API Key",
        "secret": "true",
    },
    "ZHIPU_MODEL": {
        "label": "模型名称 (Model)",
        "placeholder": "glm-4-flash",
        "is_model": "true",
    },
    "MODELSCOPE_BASE_URL": {
        "label": "魔搭 Base URL",
        "placeholder": "https://api-inference.modelscope.cn/v1",
    },
    "MODELSCOPE_API_KEY": {
        "label": "魔搭 Access Token / API Key",
        "placeholder": "填写魔搭 SDK Token",
        "secret": "true",
    },
    "MODELSCOPE_MODEL": {
        "label": "模型名称 (Model)",
        "placeholder": "Qwen/Qwen2.5-32B-Instruct",
        "is_model": "true",
    },
    "OPENAILIKED_BASE_URL": {
        "label": "自定义接口地址 (Base URL)",
        "placeholder": "例如 https://api.xxx.com/v1",
    },
    "OPENAILIKED_API_KEY": {
        "label": "API 密钥 (API Key)",
        "placeholder": "sk-...",
        "secret": "true",
    },
    "OPENAILIKED_MODEL": {
        "label": "模型名称 (Model)",
        "placeholder": "例如 gpt-4o-mini / claude-3-5-sonnet",
        "is_model": "true",
    },
    "OPENAILIKED_STREAM": {
        "label": "流式输出 (Stream)",
        "placeholder": "false 或 true",
    },
    "OPENAILIKED_STOP_TOKENS": {
        "label": "停止词 (Stop Tokens)",
        "placeholder": "选填，多个以空格分隔",
    },
    "OPENAILIKED_MAX_TOKENS": {
        "label": "最大 Token 数 (Max Tokens)",
        "placeholder": "-1 表示默认",
    },
    "OLLAMA_HOST": {
        "label": "Ollama 服务地址",
        "placeholder": "http://127.0.0.1:11434",
    },
    "OLLAMA_MODEL": {
        "label": "本地模型名称 (Model)",
        "placeholder": "gemma2 / qwen2.5:7b",
        "is_model": "true",
    },
    "AZURE_OPENAI_BASE_URL": {
        "label": "Azure 终结点 (Endpoint)",
        "placeholder": "https://xxx.openai.azure.com",
    },
    "AZURE_OPENAI_API_KEY": {
        "label": "Azure OpenAI Key",
        "placeholder": "填写密钥",
        "secret": "true",
    },
    "AZURE_OPENAI_MODEL": {
        "label": "部署/模型名称 (Deployment)",
        "placeholder": "gpt-4o-mini",
        "is_model": "true",
    },
    "AZURE_OPENAI_API_VERSION": {
        "label": "API 版本 (Version)",
        "placeholder": "2024-06-01",
    },
    "GROK_BASE_URL": {
        "label": "Grok Base URL",
        "placeholder": "https://api.x.ai/v1",
    },
    "GROK_API_KEY": {
        "label": "Grok API Key",
        "placeholder": "xai-...",
        "secret": "true",
    },
    "GROK_MODEL": {
        "label": "模型名称 (Model)",
        "placeholder": "grok-2-1212",
        "is_model": "true",
    },
    "GROK_STREAM": {
        "label": "流式输出 (Stream)",
        "placeholder": "true 或 false",
    },
    "GROQ_API_KEY": {
        "label": "Groq API Key",
        "placeholder": "gsk_...",
        "secret": "true",
    },
    "GROQ_MODEL": {
        "label": "模型名称 (Model)",
        "placeholder": "llama-3-3-70b-versatile",
        "is_model": "true",
    },
    "MINIMAX_API_KEY": {
        "label": "MiniMax API Key",
        "placeholder": "填写密钥",
        "secret": "true",
    },
    "MINIMAX_MODEL": {
        "label": "模型名称 (Model)",
        "placeholder": "MiniMax-M2.7",
        "is_model": "true",
    },
    "X302AI_API_KEY": {
        "label": "302.AI API Key",
        "placeholder": "sk-...",
        "secret": "true",
    },
    "X302AI_MODEL": {
        "label": "模型名称 (Model)",
        "placeholder": "Gemma-7B",
        "is_model": "true",
    },
    "XINFERENCE_HOST": {
        "label": "Xinference 服务地址",
        "placeholder": "http://127.0.0.1:9997",
    },
    "XINFERENCE_MODEL": {
        "label": "模型名称 (Model)",
        "placeholder": "gemma-2-it",
        "is_model": "true",
    },
    "DIFY_API_URL": {
        "label": "Dify API 地址",
        "placeholder": "https://api.dify.ai/v1/chat-messages",
    },
    "DIFY_API_KEY": {
        "label": "Dify API Key",
        "placeholder": "app-...",
        "secret": "true",
    },
    "AnythingLLM_URL": {
        "label": "AnythingLLM 接口地址",
        "placeholder": "http://localhost:3001/api/v1/workspace/xxx/chat",
    },
    "AnythingLLM_APIKEY": {
        "label": "AnythingLLM API Key",
        "placeholder": "填写密钥",
        "secret": "true",
    },
    "DEEPL_AUTH_KEY": {
        "label": "DeepL Auth Key",
        "placeholder": "填写 DeepL 认证密钥",
        "secret": "true",
    },
    "DEEPLX_ENDPOINT": {
        "label": "DeepLX 接口地址",
        "placeholder": "https://api.deepl.com/translate",
    },
    "DEEPLX_ACCESS_TOKEN": {
        "label": "DeepLX Access Token (选填)",
        "placeholder": "选填访问令牌",
        "secret": "true",
    },
    "AZURE_ENDPOINT": {
        "label": "Azure 翻译终结点",
        "placeholder": "https://api.translator.azure.cn",
    },
    "AZURE_API_KEY": {
        "label": "Azure 翻译订阅密钥",
        "placeholder": "填写密钥",
        "secret": "true",
    },
    "TENCENTCLOUD_SECRET_ID": {
        "label": "腾讯云 SecretId",
        "placeholder": "AKID...",
    },
    "TENCENTCLOUD_SECRET_KEY": {
        "label": "腾讯云 SecretKey",
        "placeholder": "填写 SecretKey",
        "secret": "true",
    },
}

LANG_MAP: dict[str, str] = {
    "简体中文 (Simplified Chinese)": "zh",
    "繁体中文 (Traditional Chinese)": "zh-TW",
    "英语 (English)": "en",
    "日语 (Japanese)": "ja",
    "韩语 (Korean)": "ko",
    "法语 (French)": "fr",
    "德语 (German)": "de",
    "俄语 (Russian)": "ru",
    "西班牙语 (Spanish)": "es",
    "意大利语 (Italian)": "it",
}

CODE_TO_LANG_LABEL: dict[str, str] = {v: k for k, v in LANG_MAP.items()}
# Also map legacy GUI language names
LEGACY_LANG_TO_CODE: dict[str, str] = {
    "Simplified Chinese": "zh",
    "Traditional Chinese": "zh-TW",
    "English": "en",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Spanish": "es",
    "Italian": "it",
}

DEFAULT_PROMPT_TEMPLATE = (
    "You are a professional, authentic machine translation engine. "
    "Only Output the translated text, do not include any other text.\n\n"
    "Translate the following markdown source text to ${lang_out}. "
    "Keep the formula notation {v*} unchanged. "
    "Output translation directly without any additional text.\n\n"
    "Source Text: ${text}\n\n"
    "Translated Text:"
)


def is_secret_field(env_key: str) -> bool:
    info = ENV_FIELD_INFO.get(env_key, {})
    if info.get("secret") == "true":
        return True
    upper = env_key.upper()
    return any(tok in upper for tok in ("KEY", "TOKEN", "SECRET", "PASSWORD"))


def get_provider_envs(service_key: str) -> dict[str, str]:
    """Load current saved/default env dict for a given service key."""
    translator_cls = SERVICE_MAP[service_key]
    saved = ConfigManager.get_translator_by_name(translator_cls.name) or {}
    result: dict[str, str] = {}
    for k, default_val in translator_cls.envs.items():
        val = saved.get(k)
        if val is None or val == "":
            val = os.environ.get(k, default_val)
        result[k] = "" if val is None else str(val)
    return result


def save_provider_envs(service_key: str, envs: dict[str, str]) -> None:
    """Save env dict for a given service key into ConfigManager and os.environ."""
    translator_cls = SERVICE_MAP[service_key]
    clean_envs: dict[str, Any] = {}
    for k in translator_cls.envs:
        val = envs.get(k, "").strip()
        clean_envs[k] = val if val != "" else None
        if val:
            os.environ[k] = val
    ConfigManager.set_translator_by_name(translator_cls.name, clean_envs)


def is_provider_configured(service_key: str) -> tuple[bool, str]:
    """Return (is_ready, status_label) for a provider."""
    from pdf2zh.desktop.i18n import tr

    translator_cls = SERVICE_MAP[service_key]
    if not translator_cls.envs:
        return True, tr("status_free")
    envs = get_provider_envs(service_key)
    # Check if any required secret/key or URL is missing
    required_keys = [
        k
        for k, default_v in translator_cls.envs.items()
        if default_v is None and "STOP_TOKENS" not in k and "ACCESS_TOKEN" not in k
    ]
    if not required_keys:
        return True, tr("status_ready")
    for rk in required_keys:
        if not envs.get(rk, "").strip():
            return False, tr("status_need_key")
    return True, tr("status_configured")


class AppSettings:
    """Centralized helper for reading and writing application-level settings via ConfigManager."""

    DEFAULTS: dict[str, Any] = {
        "PDF2ZH_UI_LANG": "zh",
        "PDF2ZH_DEFAULT_SERVICE": "Bing",
        "PDF2ZH_LANG_FROM_CODE": "en",
        "PDF2ZH_LANG_TO_CODE": "zh",
        "PDF2ZH_DEFAULT_MODE": "fast",  # fast, ultrafast, precise, babeldoc
        "PDF2ZH_VFONT": "",
        "PDF2ZH_VCHAR": "",
        "PDF2ZH_CUSTOM_PROMPT": "",
        "PDF2ZH_USE_CUSTOM_PROMPT": False,
        "PDF2ZH_SKIP_SUBSET_FONTS": False,
        "PDF2ZH_COMPATIBLE_PDFA": False,
        "PDF2ZH_OCR_LANGUAGE": "",
        "PDF2ZH_TESSDATA_PREFIX": "",
        "PDF2ZH_OUTPUT_DIR": "",
        "PDF2ZH_SAVE_NEXT_TO_SOURCE": True,
        "PDF2ZH_GEN_MONO": True,
        "PDF2ZH_GEN_DUAL": True,
        "PDF2ZH_THREADS": 4,
        "PDF2ZH_AUTO_PREVIEW": True,
        "PDF2ZH_AUTO_OPEN_DIR": False,
        "PDF2ZH_IGNORE_CACHE": False,
        "PDF2ZH_PROXY_ENABLED": False,
        "PDF2ZH_HTTP_PROXY": "http://127.0.0.1:7890",
        "PDF2ZH_ONNX_BACKEND": "auto",
        "PDF2ZH_ONNX_MODEL_PATH": "",
    }

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        fallback = cls.DEFAULTS.get(key) if default is None else default
        val = ConfigManager.get(key, None)
        if val is None:
            return fallback
        if isinstance(fallback, bool) and not isinstance(val, bool):
            return str(val).lower() in ("true", "1", "yes")
        if isinstance(fallback, int) and not isinstance(val, int):
            try:
                return int(val)
            except (ValueError, TypeError):
                return fallback
        return val

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        ConfigManager.set(key, value)

    @classmethod
    def apply_runtime_settings(cls) -> None:
        """Apply proxy, OCR, and ONNX runtime settings to the current process."""
        if cls.get("PDF2ZH_PROXY_ENABLED"):
            proxy = str(cls.get("PDF2ZH_HTTP_PROXY") or "").strip()
            if proxy:
                os.environ["HTTP_PROXY"] = proxy
                os.environ["HTTPS_PROXY"] = proxy
                os.environ["http_proxy"] = proxy
                os.environ["https_proxy"] = proxy
        else:
            for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
                os.environ.pop(k, None)

        ocr_lang = str(cls.get("PDF2ZH_OCR_LANGUAGE") or "").strip()
        if ocr_lang:
            os.environ["PDF2ZH_OCR_LANGUAGE"] = ocr_lang
        else:
            os.environ.pop("PDF2ZH_OCR_LANGUAGE", None)

        tess_prefix = str(cls.get("PDF2ZH_TESSDATA_PREFIX") or "").strip()
        if tess_prefix:
            os.environ["TESSDATA_PREFIX"] = tess_prefix

        backend = str(cls.get("PDF2ZH_ONNX_BACKEND") or "auto")
        try:
            from pdf2zh.doclayout import set_backend

            set_backend(backend)
        except Exception:
            pass

    @classmethod
    def config_file_path(cls) -> Path:
        return ConfigManager.get_instance()._config_path

    @classmethod
    def cache_db_path(cls) -> Path:
        return Path.home() / ".cache" / "pdf2zh" / "cache.v1.db"

