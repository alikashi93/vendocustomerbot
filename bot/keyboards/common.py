"""دکمه‌های تکرارشونده و مشترک."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

RESTART_BUTTON = InlineKeyboardButton(text="🔙 شروع مجدد", callback_data="restart")


def restart_keyboard() -> InlineKeyboardMarkup:
    """کیبورد فقط با دکمه شروع مجدد."""
    return InlineKeyboardMarkup(inline_keyboard=[[RESTART_BUTTON]])


def yes_no_keyboard(yes_cb: str, no_cb: str) -> InlineKeyboardMarkup:
    """کیبورد بله/خیر با callback دلخواه."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="بله", callback_data=yes_cb)],
            [InlineKeyboardButton(text="خیر", callback_data=no_cb)],
        ]
    )
