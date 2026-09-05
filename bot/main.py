"""نقطه ورود بات Vendo Customer Bot — اجرای long polling.

این فایل طوری نوشته شده که تحت هیچ شرایطی کرش نکند:
اگر تنظیمات اشتباه باشد یا اینترنت سرور به تلگرام نرسد،
بات زنده می‌ماند، دلیل دقیق را در لاگ می‌نویسد و دوباره تلاش می‌کند.
"""

import asyncio
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def _load_env():
    """خواندن و اعتبارسنجی متغیرهای محیطی. در صورت مشکل، None برمی‌گرداند."""
    token = os.getenv("BOT_TOKEN", "").strip()
    admin_raw = os.getenv("ADMIN_CHAT_ID", "").strip()

    problems = []
    if not token:
        problems.append("BOT_TOKEN khaali ast ya be container naresid-e")
    admin_id = 0
    if not admin_raw:
        problems.append("ADMIN_CHAT_ID khaali ast ya be container naresid-e")
    else:
        try:
            admin_id = int(admin_raw)
        except ValueError:
            problems.append(
                f"ADMIN_CHAT_ID bayad faqat ADAD baashad, ama in daryaft shod: {admin_raw!r}"
            )

    if problems:
        for p in problems:
            logger.error("CONFIG ERROR -> %s", p)
        logger.error(
            "Fix: dar Coolify bakhsh Environment Variables ra check konid "
            "(esm-e daghigh: BOT_TOKEN va ADMIN_CHAT_ID - bedoon quotation va fasele) "
            "va dobare Deploy bezanid."
        )
        return None

    logger.info(
        "Config OK | ADMIN_CHAT_ID=%s | BOT_TOKEN=%s****%s",
        admin_id,
        token[:8],
        token[-4:],
    )
    return token


async def _run_bot(token: str) -> None:
    from aiogram import Bot, Dispatcher
    from aiogram.client.default import DefaultBotProperties
    from aiogram.enums import ParseMode
    from aiogram.fsm.storage.memory import MemoryStorage

    from bot.handlers import setup_routers

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(setup_routers())
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Connected to Telegram! Bot is now polling... OK")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def main() -> None:
    logger.info("=== Vendo Customer Bot starting ===")
    attempt = 0
    while True:
        token = _load_env()
        if token is None:
            # تنظیمات مشکل دارد — زنده می‌مانیم و هر ۳۰ ثانیه یادآوری می‌کنیم
            await asyncio.sleep(30)
            continue
        try:
            await _run_bot(token)
        except asyncio.CancelledError:
            raise
        except Exception:
            attempt += 1
            wait = min(60, 5 * attempt)
            logger.exception(
                "Bot error - retrying in %s seconds (attempt #%s)", wait, attempt
            )
            await asyncio.sleep(wait)


if __name__ == "__main__":
    asyncio.run(main())
