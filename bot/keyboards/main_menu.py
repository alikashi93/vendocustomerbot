"""کیبوردهای منوی اصلی و شروع."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def is_customer_keyboard() -> InlineKeyboardMarkup:
    """سوال اول: آیا مشتری وندو هستید؟"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ بله", callback_data="cust:yes")],
            [InlineKeyboardButton(text="❌ خیر", callback_data="cust:no")],
        ]
    )


def not_customer_keyboard() -> InlineKeyboardMarkup:
    """لینک به بات فروش برای غیرمشتریان."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🤖 بات درخواست طراحی سایت",
                    url="https://t.me/vendoonlineofficial_bot",
                )
            ],
            [InlineKeyboardButton(text="🔙 شروع مجدد", callback_data="restart")],
        ]
    )


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """منوی اصلی: سه درخواست ممکن."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 خرید بسته جدید", callback_data="menu:purchase")],
            [
                InlineKeyboardButton(
                    text="⚙️ فعال‌سازی فیچر روی سایت", callback_data="menu:feature"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📚 دریافت آموزش فعال‌سازی فیچرها", callback_data="menu:training"
                )
            ],
        ]
    )
