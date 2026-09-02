"""فلوی مشترک دریافت اطلاعات تماس (۳ مرحله) — از همه مسیرها صدا زده می‌شود.

نحوه استفاده از سایر هندلرها:
    await start_contact_flow(message, state)
پیش‌نیاز: قبل از فراخوانی، این کلیدها در FSMContext ست شده باشند:
    request_type: str
    details: list[[label, value]]
    is_training: bool (اختیاری — برای پیام پایانی خاص مسیر آموزش)
    popup_photo_id: str (اختیاری)
"""

import logging
import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.common import restart_keyboard
from bot.states import ContactStates
from bot.utils.notify_admin import notify_admin

logger = logging.getLogger(__name__)

router = Router(name="contact_info")

# پیام‌های پایانی
FINAL_MESSAGE_TRAINING = "درخواست شما ثبت شد، به‌زودی با شما تماس می‌گیریم."
FINAL_MESSAGE_DEFAULT = (
    "درخواست شما با موفقیت ثبت شد، همکاران ما به‌زودی با شما تماس خواهند گرفت. ✅"
)

# جدول تبدیل ارقام فارسی/عربی به انگلیسی
_DIGIT_MAP = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")

_PHONE_RE = re.compile(r"^09\d{9}$")


def _normalize_phone(text: str) -> str:
    """حذف فاصله/خط تیره و تبدیل ارقام فارسی به انگلیسی."""
    return re.sub(r"[\s\-]+", "", text.translate(_DIGIT_MAP))


async def start_contact_flow(message: Message, state: FSMContext) -> None:
    """شروع فلوی ۳ مرحله‌ای دریافت اطلاعات تماس."""
    await state.set_state(ContactStates.full_name)
    await message.answer("لطفاً نام و نام‌خانوادگی خود را وارد کنید:")


@router.message(ContactStates.full_name, F.text)
async def process_full_name(message: Message, state: FSMContext) -> None:
    await state.update_data(full_name=message.text.strip())
    await state.set_state(ContactStates.business_name)
    await message.answer("لطفاً نام مجموعه/کسب‌وکار خود را وارد کنید:")


@router.message(ContactStates.business_name, F.text)
async def process_business_name(message: Message, state: FSMContext) -> None:
    await state.update_data(business_name=message.text.strip())
    await state.set_state(ContactStates.phone)
    await message.answer("لطفاً شماره موبایل خود را وارد کنید:")


@router.message(ContactStates.phone, F.text)
async def process_phone(message: Message, state: FSMContext) -> None:
    phone = _normalize_phone(message.text)
    data = await state.get_data()

    # اعتبارسنجی ساده شماره ایرانی؛ فقط یک بار تذکر می‌دهیم و بلاک نمی‌کنیم.
    if not _PHONE_RE.match(phone) and not data.get("phone_warned"):
        await state.update_data(phone_warned=True)
        await message.answer(
            "⚠️ فرمت شماره موبایل صحیح به نظر نمی‌رسد "
            "(نمونه صحیح: 09123456789).\n"
            "لطفاً شماره را دوباره وارد کنید:"
        )
        return

    await state.update_data(phone=phone)
    data = await state.get_data()

    # ۱) پیام تأییدیه پایانی به کاربر
    final_text = FINAL_MESSAGE_TRAINING if data.get("is_training") else FINAL_MESSAGE_DEFAULT
    await message.answer(final_text, reply_markup=restart_keyboard())

    # ۲) ارسال خلاصه کامل به ادمین
    await notify_admin(message.bot, message.from_user, data)

    await state.clear()
    logger.info(
        "Flow completed for user %s (request: %s)",
        message.from_user.id,
        data.get("request_type"),
    )
