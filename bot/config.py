"""خواندن تنظیمات از متغیرهای محیطی."""

import os


class ConfigError(Exception):
    """خطای مربوط به تنظیمات ناقص."""


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ConfigError(
            f"متغیر محیطی {name} تنظیم نشده است. "
            f"لطفاً آن را در فایل .env یا تنظیمات محیط قرار دهید."
        )
    return value


BOT_TOKEN: str = _require_env("BOT_TOKEN")
ADMIN_CHAT_ID: int = int(_require_env("ADMIN_CHAT_ID"))
