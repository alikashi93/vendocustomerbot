"""فلوی «خرید بسته جدید» — انتخاب چندگانه بسته‌ها با دکمه‌های toggle."""

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.handlers.contact_info import start_contact_flow
from bot.keyboards.package_menu import PACKAGES, package_keyboard
from bot.states import PurchaseStates

logger = logging.getLogger(__name__)

router = Router(name="purchase_package")

PACKAGE_QUESTION = "قصد خرید کدام بسته را دارید؟ (امکان انتخاب چند بسته وجود دارد)"


@router.callback_query(F.data == "menu:purchase")
async def cb_purchase_menu(callback: CallbackQuery, state: FSMContext) -> None:
    """ورود به فلوی خرید بسته."""
    await state.set_state(PurchaseStates.selecting_packages)
    await state.update_data(selected_packages=[])
    await callback.message.edit_text(
        PACKAGE_QUESTION, reply_markup=package_keyboard(set())
    )
    await callback.answer()


@router.callback_query(
    PurchaseStates.selecting_packages, F.data.startswith("pkg:"), F.data != "pkg:submit"
)
async def cb_toggle_package(callback: CallbackQuery, state: FSMContext) -> None:
    """تیک زدن/برداشتن یک بسته — فقط کیبورد همان پیام ادیت می‌شود."""
    key = callback.data.split(":", 1)[1]
    if key not in PACKAGES:
        await callback.answer()
        return

    data = await state.get_data()
    selected: list[str] = data.get("selected_packages", [])
    if key in selected:
        selected.remove(key)
    else:
        selected.append(key)
    await state.update_data(selected_packages=selected)

    await callback.message.edit_reply_markup(reply_markup=package_keyboard(selected))
    await callback.answer()


@router.callback_query(PurchaseStates.selecting_packages, F.data == "pkg:submit")
async def cb_submit_packages(callback: CallbackQuery, state: FSMContext) -> None:
    """ارسال درخواست — فقط وقتی حداقل یک بسته انتخاب شده باشد."""
    data = await state.get_data()
    selected: list[str] = data.get("selected_packages", [])

    if not selected:
        await callback.answer(
            "⚠️ لطفاً ابتدا حداقل یک بسته را انتخاب کنید.", show_alert=True
        )
        return

    titles = [PACKAGES[k] for k in selected if k in PACKAGES]
    await state.update_data(
        request_type="خرید بسته جدید",
        details=[["بسته‌های انتخابی", "، ".join(titles)]],
    )
    await callback.message.edit_text(
        "بسته‌های انتخابی شما:\n" + "\n".join(f"• {t}" for t in titles)
    )
    await start_contact_flow(callback.message, state)
    await callback.answer()
