"""کیبوردهای مربوط به فلوهای فعال‌سازی فیچر و آموزش."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# لیست فیچرها — برای افزودن/حذف فیچر فقط همین دیکشنری را ویرایش کنید.
FEATURES: dict[str, str] = {
    "coupon": "کوپن",
    "discount": "کد تخفیف",
    "popup": "پاپ‌آپ",
    "preorder": "پیش‌سفارش",
    "topping": "تاپینگ",
    "gateway": "درگاه پرداخت اعتباری",
    "fleet": "ناوگان پیک",
}


def feature_keyboard() -> InlineKeyboardMarkup:
    """انتخاب فیچر برای فعال‌سازی."""
    rows = [
        [InlineKeyboardButton(text=title, callback_data=f"feat:{key}")]
        for key, title in FEATURES.items()
    ]
    rows.append([InlineKeyboardButton(text="🔙 شروع مجدد", callback_data="restart")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def training_keyboard() -> InlineKeyboardMarkup:
    """انتخاب فیچر برای دریافت آموزش (با گزینه سایر)."""
    rows = [
        [InlineKeyboardButton(text=title, callback_data=f"train:{key}")]
        for key, title in FEATURES.items()
    ]
    rows.append(
        [InlineKeyboardButton(text="سایر (لطفاً وارد کنید)", callback_data="train:other")]
    )
    rows.append([InlineKeyboardButton(text="🔙 شروع مجدد", callback_data="restart")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ----- کوپن -----
COUPON_OPTIONS: dict[str, str] = {
    "first15": "۱۵٪ تخفیف سفارش اول",
    "all10": "۱۰٪ تخفیف برای کل کاربران",
    "freeship": "ارسال رایگان",
    "all": "همه موارد بالا",
}


def coupon_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=title, callback_data=f"coupon:{key}")]
        for key, title in COUPON_OPTIONS.items()
    ]
    rows.append(
        [
            InlineKeyboardButton(
                text="سایر (کوپن مدنظرتان را بنویسید)", callback_data="coupon:other"
            )
        ]
    )
    rows.append([InlineKeyboardButton(text="🔙 شروع مجدد", callback_data="restart")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ----- کد تخفیف: مرحله ۱ -----
DISCOUNT_OPTIONS: dict[str, str] = {
    "first20": "۲۰٪ تخفیف سفارش اول",
    "first15": "۱۵٪ تخفیف سفارش اول",
    "all15": "۱۵٪ تخفیف برای کل کاربران",
    "all10": "۱۰٪ تخفیف برای کل کاربران",
}


def discount_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=title, callback_data=f"disc:{key}")]
        for key, title in DISCOUNT_OPTIONS.items()
    ]
    rows.append(
        [
            InlineKeyboardButton(
                text="سایر (کد تخفیف مدنظرتان را بنویسید)", callback_data="disc:other"
            )
        ]
    )
    rows.append([InlineKeyboardButton(text="🔙 شروع مجدد", callback_data="restart")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ----- کد تخفیف: مرحله ۲ (کد خاص) -----
DISCOUNT_CODE_OPTIONS: dict[str, str] = {
    "site": "SITE",
    "off": "OFF",
}


def discount_code_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=title, callback_data=f"dcode:{key}")]
        for key, title in DISCOUNT_CODE_OPTIONS.items()
    ]
    rows.append(
        [
            InlineKeyboardButton(
                text="سایر (کد تخفیف مدنظرتان را بنویسید)", callback_data="dcode:other"
            )
        ]
    )
    rows.append([InlineKeyboardButton(text="🔙 شروع مجدد", callback_data="restart")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ----- تاپینگ -----
def topping_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="ثبت درخواست فعال‌سازی تاپینگ", callback_data="topping:submit"
                )
            ],
            [InlineKeyboardButton(text="🔙 شروع مجدد", callback_data="restart")],
        ]
    )


# ----- درگاه پرداخت اعتباری -----
GATEWAY_OPTIONS: dict[str, str] = {
    "digipay": "دیجی‌پی",
    "tara": "تارا",
    "azkivam": "ازکی‌وام",
    "digitara": "دیجی‌پی و تارا",
    "all": "همه موارد",
}


def gateway_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=title, callback_data=f"gw:{key}")]
        for key, title in GATEWAY_OPTIONS.items()
    ]
    rows.append([InlineKeyboardButton(text="🔙 شروع مجدد", callback_data="restart")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ----- ناوگان پیک -----
FLEET_OPTIONS: dict[str, str] = {
    "snappbox": "اسنپ باکس",
    "alopeyk": "الوپیک",
    "miare": "میاره",
    "all": "همه موارد بالا",
}


def fleet_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=title, callback_data=f"fleet:{key}")]
        for key, title in FLEET_OPTIONS.items()
    ]
    rows.append([InlineKeyboardButton(text="🔙 شروع مجدد", callback_data="restart")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
