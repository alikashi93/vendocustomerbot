"""هندلر /start، سوال «مشتری وندو هستید؟» و منوی اصلی + هندلر fallback."""

import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.common import restart_keyboard
from bot.keyboards.main_menu import (
    is_customer_keyboard,
    main_menu_keyboard,
    not_customer_keyboard,
)

logger = logging.getLogger(__name__)

router = Router(name="start")

WELCOME_TEXT = (
    "سلام! به بات پشتیبانی مشتریان وندو خوش اومدید 👋\n"
    "آیا شما جزو مشتریان فعلی وندو هستید؟"
)

NOT_CUSTOMER_TEXT = (
    "برای درخواست طراحی سایت لطفاً به بات زیر مراجعه کنید:\n"
    "@vendoonlineofficial_bot"
)

MAIN_MENU_TEXT = "چه درخواستی دارید؟"


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    """/start — همیشه فلو را از اول شروع می‌کند."""
    await state.clear()
    await message.answer(WELCOME_TEXT, reply_markup=is_customer_keyboard())
    logger.info("User %s started the bot", message.from_user.id)


@router.callback_query(F.data == "restart")
async def cb_restart(callback: CallbackQuery, state: FSMContext) -> None:
    """دکمه «🔙 شروع مجدد» — بازگشت به ابتدای فلو از هر جای بات."""
    await state.clear()
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=is_customer_keyboard())
    await callback.answer()


@router.callback_query(F.data == "cust:no")
async def cb_not_customer(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(
        NOT_CUSTOMER_TEXT, reply_markup=not_customer_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "cust:yes")
async def cb_is_customer(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(MAIN_MENU_TEXT, reply_markup=main_menu_keyboard())
    await callback.answer()


# ---------------------------------------------------------------------------
# Fallback — این روتر باید آخر از همه در Dispatcher ثبت شود (bot/handlers/__init__.py)
# ---------------------------------------------------------------------------
fallback_router = Router(name="fallback")


@fallback_router.message()
async def fallback_message(message: Message) -> None:
    """پیام‌های نامرتبط (خارج از فلو یا با نوع اشتباه) — بدون کرش هندل می‌شوند."""
    await message.answer(
        "متوجه پیام شما نشدم. 🙏\n"
        "لطفاً از دکمه‌های بات استفاده کنید یا برای شروع دوباره /start را بزنید.",
        reply_markup=restart_keyboard(),
    )


@fallback_router.callback_query()
async def fallback_callback(callback: CallbackQuery) -> None:
    """کلیک روی دکمه‌های قدیمی/منقضی‌شده."""
    await callback.answer(
        "این دکمه دیگر فعال نیست. لطفاً با /start از ابتدا شروع کنید.",
        show_alert=True,
    )
