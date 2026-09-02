"""فلوی «دریافت آموزش فعال‌سازی فیچرها»."""

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.handlers.contact_info import start_contact_flow
from bot.keyboards.feature_menu import FEATURES, training_keyboard
from bot.states import TrainingStates

logger = logging.getLogger(__name__)

router = Router(name="training")

TRAINING_QUESTION = "برای کدام فیچر نیاز به آموزش دارید؟"


@router.callback_query(F.data == "menu:training")
async def cb_training_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(TrainingStates.choosing)
    await callback.message.edit_text(TRAINING_QUESTION, reply_markup=training_keyboard())
    await callback.answer()


@router.callback_query(TrainingStates.choosing, F.data.startswith("train:"))
async def cb_training_choose(callback: CallbackQuery, state: FSMContext) -> None:
    key = callback.data.split(":", 1)[1]

    if key == "other":
        await state.set_state(TrainingStates.custom_text)
        await callback.message.edit_text(
            "لطفاً فیچر مدنظرتان برای آموزش را تایپ و ارسال کنید:"
        )
        await callback.answer()
        return

    if key not in FEATURES:
        await callback.answer()
        return

    await state.update_data(
        request_type="دریافت آموزش فعال‌سازی فیچر",
        details=[["فیچر موردنظر برای آموزش", FEATURES[key]]],
        is_training=True,
    )
    await callback.message.edit_text(f"فیچر انتخابی برای آموزش: {FEATURES[key]}")
    await start_contact_flow(callback.message, state)
    await callback.answer()


@router.message(TrainingStates.custom_text, F.text)
async def training_custom(message: Message, state: FSMContext) -> None:
    await state.update_data(
        request_type="دریافت آموزش فعال‌سازی فیچر",
        details=[["فیچر موردنظر برای آموزش (سایر)", message.text.strip()]],
        is_training=True,
    )
    await start_contact_flow(message, state)
