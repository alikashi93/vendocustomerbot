"""فلوی «فعال‌سازی فیچر روی سایت».

هر فیچر یک سکشن کاملاً مستقل با هندلرهای خودش دارد:
    - کوپن                → سکشن COUPON
    - کد تخفیف            → سکشن DISCOUNT
    - پاپ‌آپ               → سکشن POPUP
    - پیش‌سفارش            → سکشن PREORDER
    - تاپینگ              → سکشن TOPPING
    - درگاه پرداخت اعتباری → سکشن GATEWAY
    - ناوگان پیک           → سکشن FLEET

برای تغییر رفتار هر فیچر فقط سکشن مربوط به همان فیچر را ویرایش کنید.
"""

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.handlers.contact_info import start_contact_flow
from bot.keyboards.common import yes_no_keyboard
from bot.keyboards.feature_menu import (
    COUPON_OPTIONS,
    DISCOUNT_CODE_OPTIONS,
    DISCOUNT_OPTIONS,
    FEATURES,
    FLEET_OPTIONS,
    GATEWAY_OPTIONS,
    coupon_keyboard,
    discount_code_keyboard,
    discount_keyboard,
    feature_keyboard,
    fleet_keyboard,
    gateway_keyboard,
    topping_keyboard,
)
from bot.states import (
    CouponStates,
    DiscountStates,
    PopupStates,
    PreorderStates,
)

logger = logging.getLogger(__name__)

router = Router(name="feature_activation")

FEATURE_QUESTION = "قصد فعال‌سازی کدام فیچر زیر را در سایتتان دارید؟"


def _request_type(feature_key: str) -> str:
    return f"فعال‌سازی فیچر: {FEATURES[feature_key]}"


# ===========================================================================
# منوی انتخاب فیچر
# ===========================================================================
@router.callback_query(F.data == "menu:feature")
async def cb_feature_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(FEATURE_QUESTION, reply_markup=feature_keyboard())
    await callback.answer()


# ===========================================================================
# سکشن COUPON — فیچر «کوپن»
# ===========================================================================
@router.callback_query(F.data == "feat:coupon")
async def coupon_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(CouponStates.choosing)
    await state.update_data(request_type=_request_type("coupon"), details=[])
    await callback.message.edit_text(
        "کدام کد تخفیف برای شما فعال شود؟", reply_markup=coupon_keyboard()
    )
    await callback.answer()


@router.callback_query(CouponStates.choosing, F.data.startswith("coupon:"))
async def coupon_choose(callback: CallbackQuery, state: FSMContext) -> None:
    key = callback.data.split(":", 1)[1]

    if key == "other":
        await state.set_state(CouponStates.custom_text)
        await callback.message.edit_text("لطفاً کوپن مدنظرتان را تایپ و ارسال کنید:")
        await callback.answer()
        return

    if key not in COUPON_OPTIONS:
        await callback.answer()
        return

    await state.update_data(details=[["کوپن انتخابی", COUPON_OPTIONS[key]]])
    await callback.message.edit_text(f"کوپن انتخابی: {COUPON_OPTIONS[key]}")
    await start_contact_flow(callback.message, state)
    await callback.answer()


@router.message(CouponStates.custom_text, F.text)
async def coupon_custom(message: Message, state: FSMContext) -> None:
    await state.update_data(details=[["کوپن انتخابی (سایر)", message.text.strip()]])
    await start_contact_flow(message, state)


# ===========================================================================
# سکشن DISCOUNT — فیچر «کد تخفیف» (۴ مرحله)
# ===========================================================================
@router.callback_query(F.data == "feat:discount")
async def discount_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(DiscountStates.choosing_discount)
    await state.update_data(request_type=_request_type("discount"), details=[])
    await callback.message.edit_text(
        "کدام کد تخفیف برای شما فعال شود؟", reply_markup=discount_keyboard()
    )
    await callback.answer()


@router.callback_query(DiscountStates.choosing_discount, F.data.startswith("disc:"))
async def discount_choose(callback: CallbackQuery, state: FSMContext) -> None:
    """مرحله ۱: انتخاب نوع تخفیف."""
    key = callback.data.split(":", 1)[1]

    if key == "other":
        await state.set_state(DiscountStates.custom_discount)
        await callback.message.edit_text("لطفاً کد تخفیف مدنظرتان را تایپ و ارسال کنید:")
        await callback.answer()
        return

    if key not in DISCOUNT_OPTIONS:
        await callback.answer()
        return

    data = await state.get_data()
    details = data.get("details", [])
    details.append(["نوع تخفیف", DISCOUNT_OPTIONS[key]])
    await state.update_data(details=details)
    await _discount_ask_code(callback.message, state)
    await callback.answer()


@router.message(DiscountStates.custom_discount, F.text)
async def discount_custom(message: Message, state: FSMContext) -> None:
    """مرحله ۱ («سایر»): دریافت متن آزاد نوع تخفیف."""
    data = await state.get_data()
    details = data.get("details", [])
    details.append(["نوع تخفیف (سایر)", message.text.strip()])
    await state.update_data(details=details)
    await _discount_ask_code(message, state)


async def _discount_ask_code(message: Message, state: FSMContext) -> None:
    """مرحله ۲: سوال کد تخفیف خاص."""
    await state.set_state(DiscountStates.choosing_code)
    await message.answer(
        "کد تخفیف خاصی مدنظرتان هست؟", reply_markup=discount_code_keyboard()
    )


@router.callback_query(DiscountStates.choosing_code, F.data.startswith("dcode:"))
async def discount_code_choose(callback: CallbackQuery, state: FSMContext) -> None:
    key = callback.data.split(":", 1)[1]

    if key == "other":
        await state.set_state(DiscountStates.custom_code)
        await callback.message.edit_text("لطفاً کد تخفیف مدنظرتان را تایپ و ارسال کنید:")
        await callback.answer()
        return

    if key not in DISCOUNT_CODE_OPTIONS:
        await callback.answer()
        return

    data = await state.get_data()
    details = data.get("details", [])
    details.append(["کد تخفیف", DISCOUNT_CODE_OPTIONS[key]])
    await state.update_data(details=details)
    await _discount_ask_start_date(callback.message, state)
    await callback.answer()


@router.message(DiscountStates.custom_code, F.text)
async def discount_code_custom(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    details = data.get("details", [])
    details.append(["کد تخفیف (سایر)", message.text.strip()])
    await state.update_data(details=details)
    await _discount_ask_start_date(message, state)


async def _discount_ask_start_date(message: Message, state: FSMContext) -> None:
    """مرحله ۳: تاریخ شروع."""
    await state.set_state(DiscountStates.start_date)
    await message.answer("این کد تخفیف از کی شروع شود؟ (وارد کنید)")


@router.message(DiscountStates.start_date, F.text)
async def discount_start_date(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    details = data.get("details", [])
    details.append(["تاریخ شروع", message.text.strip()])
    await state.update_data(details=details)
    # مرحله ۴: تاریخ پایان
    await state.set_state(DiscountStates.end_date)
    await message.answer("تا چه تاریخی ادامه داشته باشد؟ (وارد کنید)")


@router.message(DiscountStates.end_date, F.text)
async def discount_end_date(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    details = data.get("details", [])
    details.append(["تاریخ پایان", message.text.strip()])
    await state.update_data(details=details)
    await start_contact_flow(message, state)


# ===========================================================================
# سکشن POPUP — فیچر «پاپ‌آپ»
# ===========================================================================
@router.callback_query(F.data == "feat:popup")
async def popup_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(PopupStates.discount_text)
    await state.update_data(request_type=_request_type("popup"), details=[])
    await callback.message.edit_text("چه تخفیفی برای پاپ‌آپ در نظر گرفته‌اید؟")
    await callback.answer()


@router.message(PopupStates.discount_text, F.text)
async def popup_discount(message: Message, state: FSMContext) -> None:
    """مرحله ۱: تخفیف پاپ‌آپ (متن آزاد)."""
    data = await state.get_data()
    details = data.get("details", [])
    details.append(["تخفیف پاپ‌آپ", message.text.strip()])
    await state.update_data(details=details)

    await state.set_state(PopupStates.has_image)
    await message.answer(
        "عکسی برای پاپ‌آپ دارید؟",
        reply_markup=yes_no_keyboard("popup_img:yes", "popup_img:no"),
    )


@router.callback_query(PopupStates.has_image, F.data == "popup_img:yes")
async def popup_has_image(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(PopupStates.waiting_image)
    await callback.message.edit_text("لطفاً عکس پاپ‌آپ را ارسال کنید:")
    await callback.answer()


@router.message(PopupStates.waiting_image, F.photo | F.document)
async def popup_receive_image(message: Message, state: FSMContext) -> None:
    """دریافت عکس پاپ‌آپ (به‌صورت عکس یا فایل)."""
    data = await state.get_data()
    details = data.get("details", [])

    if message.photo:
        # بزرگ‌ترین سایز عکس را نگه می‌داریم
        await state.update_data(popup_photo_id=message.photo[-1].file_id)
        details.append(["عکس پاپ‌آپ", "توسط کاربر ارسال شد (پیوست همین پیام)"])
    else:
        # فایل (document) — file_id فایل برای ادمین در متن ذکر می‌شود
        details.append(
            ["عکس پاپ‌آپ", f"به‌صورت فایل ارسال شد ({message.document.file_name or 'file'})"]
        )
        await state.update_data(popup_document_id=message.document.file_id)

    await state.update_data(details=details)
    await start_contact_flow(message, state)


@router.message(PopupStates.waiting_image)
async def popup_image_wrong_type(message: Message) -> None:
    """اگر به‌جای عکس چیز دیگری فرستاد."""
    await message.answer("لطفاً عکس پاپ‌آپ را به‌صورت عکس یا فایل ارسال کنید. 🙏")


@router.callback_query(PopupStates.has_image, F.data == "popup_img:no")
async def popup_no_image(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(PopupStates.use_template)
    await callback.message.edit_text(
        "می‌خواهید از پاپ‌آپ‌های تمپلیت برای شما استفاده شود؟",
        reply_markup=yes_no_keyboard("popup_tpl:yes", "popup_tpl:no"),
    )
    await callback.answer()


@router.callback_query(PopupStates.use_template, F.data.startswith("popup_tpl:"))
async def popup_template_choice(callback: CallbackQuery, state: FSMContext) -> None:
    answer = "بله" if callback.data.endswith("yes") else "خیر"
    data = await state.get_data()
    details = data.get("details", [])
    details.append(["عکس پاپ‌آپ", "ندارد"])
    details.append(["استفاده از تمپلیت", answer])
    await state.update_data(details=details)
    await callback.message.edit_text(f"استفاده از پاپ‌آپ تمپلیت: {answer}")
    await start_contact_flow(callback.message, state)
    await callback.answer()


# ===========================================================================
# سکشن PREORDER — فیچر «پیش‌سفارش» (۳ مرحله متنی)
# ===========================================================================
@router.callback_query(F.data == "feat:preorder")
async def preorder_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(PreorderStates.days_before)
    await state.update_data(request_type=_request_type("preorder"), details=[])
    await callback.message.edit_text(
        "از چند روز زودتر امکان ثبت پیش‌سفارش وجود داشته باشد؟ (وارد کنید)"
    )
    await callback.answer()


@router.message(PreorderStates.days_before, F.text)
async def preorder_days(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    details = data.get("details", [])
    details.append(["تعداد روز زودتر برای ثبت پیش‌سفارش", message.text.strip()])
    await state.update_data(details=details)

    await state.set_state(PreorderStates.minutes_to_kitchen)
    await message.answer(
        "چند دقیقه قبل از زمان انتخابی توسط مشتری، سفارش به آشپزخانه ارسال شود؟\n"
        "(مثال: اگر مشتری برای ساعت ۱۸ پیش‌سفارش ثبت کرده باشد و شما عدد زیر را "
        "۳۰ وارد کنید، ساعت ۱۷:۳۰ این سفارش به‌عنوان سفارش جدید در آشپزخانه "
        "پرینت می‌شود)"
    )


@router.message(PreorderStates.minutes_to_kitchen, F.text)
async def preorder_kitchen(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    details = data.get("details", [])
    details.append(["دقیقه قبل از زمان مشتری برای ارسال به آشپزخانه", message.text.strip()])
    await state.update_data(details=details)

    await state.set_state(PreorderStates.minutes_before_slot)
    await message.answer(
        "ثبت پیش‌سفارش تا چند دقیقه قبل از بازه فعال باشد؟ "
        "(مثلاً تا چند دقیقه قبل از ساعت ۱۹ امکان ثبت پیش‌سفارش برای این ساعت "
        "وجود داشته باشد؟)"
    )


@router.message(PreorderStates.minutes_before_slot, F.text)
async def preorder_slot(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    details = data.get("details", [])
    details.append(["مهلت ثبت پیش‌سفارش (دقیقه قبل از بازه)", message.text.strip()])
    await state.update_data(details=details)
    await start_contact_flow(message, state)


# ===========================================================================
# سکشن TOPPING — فیچر «تاپینگ»
# ===========================================================================
@router.callback_query(F.data == "feat:topping")
async def topping_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(
        "با توجه به پیچیدگی‌های فنی این فیچر با شما تماس می‌گیریم.",
        reply_markup=topping_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "topping:submit")
async def topping_submit(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(
        request_type=_request_type("topping"),
        details=[["توضیح", "درخواست فعال‌سازی تاپینگ ثبت شد"]],
    )
    await callback.message.edit_text("درخواست فعال‌سازی تاپینگ ثبت شد. ✅")
    await start_contact_flow(callback.message, state)
    await callback.answer()


# ===========================================================================
# سکشن GATEWAY — فیچر «درگاه پرداخت اعتباری»
# ===========================================================================
@router.callback_query(F.data == "feat:gateway")
async def gateway_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(
        "می‌خواهید کدام درگاه در سایت شما فعال شود؟", reply_markup=gateway_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("gw:"))
async def gateway_choose(callback: CallbackQuery, state: FSMContext) -> None:
    key = callback.data.split(":", 1)[1]
    if key not in GATEWAY_OPTIONS:
        await callback.answer()
        return

    await state.update_data(
        request_type=_request_type("gateway"),
        details=[["درگاه انتخابی", GATEWAY_OPTIONS[key]]],
    )
    await callback.message.edit_text(f"درگاه انتخابی: {GATEWAY_OPTIONS[key]}")
    await start_contact_flow(callback.message, state)
    await callback.answer()


# ===========================================================================
# سکشن FLEET — فیچر «ناوگان پیک»
# ===========================================================================
@router.callback_query(F.data == "feat:fleet")
async def fleet_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(
        "کدام ناوگان پیک را می‌خواهید؟", reply_markup=fleet_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("fleet:"))
async def fleet_choose(callback: CallbackQuery, state: FSMContext) -> None:
    key = callback.data.split(":", 1)[1]
    if key not in FLEET_OPTIONS:
        await callback.answer()
        return

    await state.update_data(
        request_type=_request_type("fleet"),
        details=[["ناوگان انتخابی", FLEET_OPTIONS[key]]],
    )
    await callback.message.edit_text(f"ناوگان انتخابی: {FLEET_OPTIONS[key]}")
    await start_contact_flow(callback.message, state)
    await callback.answer()
