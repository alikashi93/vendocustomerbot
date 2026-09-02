"""ارسال خلاصه کامل درخواست به ادمین."""

import logging

from aiogram import Bot, html
from aiogram.types import User

from bot.config import ADMIN_CHAT_ID

logger = logging.getLogger(__name__)


def build_summary(user: User, data: dict) -> str:
    """ساخت متن خلاصه درخواست برای ادمین.

    ساختار data (در FSMContext):
        request_type: str            → نوع درخواست
        details: list[[label, value]] → جزئیات انتخاب‌شده در مسیر
        full_name / business_name / phone: str
        popup_photo_id: str | None   → file_id عکس پاپ‌آپ (در صورت وجود)
    """
    lines = [
        "📥 " + html.bold("درخواست جدید از بات Vendo"),
        "",
        f"🔖 نوع درخواست: {html.quote(data.get('request_type', '-'))}",
    ]

    details: list = data.get("details") or []
    if details:
        lines.append("")
        lines.append("📋 " + html.bold("جزئیات:"))
        for label, value in details:
            lines.append(f"• {html.quote(str(label))}: {html.quote(str(value))}")

    lines += [
        "",
        "👤 " + html.bold("اطلاعات تماس:"),
        f"• نام و نام‌خانوادگی: {html.quote(data.get('full_name', '-'))}",
        f"• نام مجموعه: {html.quote(data.get('business_name', '-'))}",
        f"• شماره موبایل: {html.quote(data.get('phone', '-'))}",
        "",
        f"🆔 کاربر تلگرام: {html.quote(user.full_name)}"
        + (f" (@{user.username})" if user.username else "")
        + f" — <code>{user.id}</code>",
    ]
    return "\n".join(lines)


async def notify_admin(bot: Bot, user: User, data: dict) -> None:
    """ارسال خلاصه درخواست (و عکس پاپ‌آپ در صورت وجود) به ADMIN_CHAT_ID."""
    text = build_summary(user, data)
    photo_id = data.get("popup_photo_id")
    try:
        if photo_id:
            # کپشن تلگرام حداکثر ۱۰۲۴ کاراکتر است؛ خلاصه‌های ما کوتاه‌تر از این حد هستند.
            await bot.send_photo(ADMIN_CHAT_ID, photo=photo_id, caption=text)
        else:
            await bot.send_message(ADMIN_CHAT_ID, text)
        logger.info("Admin notified for user %s", user.id)
    except Exception:  # noqa: BLE001
        logger.exception("Failed to notify admin for user %s", user.id)
