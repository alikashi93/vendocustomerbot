"""نقطه ورود بات Vendo Customer Bot — اجرای long polling."""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import ADMIN_CHAT_ID, BOT_TOKEN
from bot.handlers import setup_routers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    # چاپ وضعیت تنظیمات — توکن ماسک می‌شود تا در لاگ لو نرود
    logger.info(
        "Config OK | ADMIN_CHAT_ID=%s | BOT_TOKEN=%s****%s",
        ADMIN_CHAT_ID,
        BOT_TOKEN[:8],
        BOT_TOKEN[-4:],
    )

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(setup_routers())

    attempt = 0
    try:
        while True:
            try:
                await bot.delete_webhook(drop_pending_updates=True)
                logger.info("Connected to Telegram! Bot is now polling... ✅")
                attempt = 0
                await dp.start_polling(bot)
            except asyncio.CancelledError:
                raise
            except Exception:
                attempt += 1
                wait = min(60, 5 * attempt)
                logger.exception(
                    "Bot error — retrying in %s seconds (attempt #%s)",
                    wait,
                    attempt,
                )
                await asyncio.sleep(wait)
    finally:
        await bot.session.close()
        logger.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
