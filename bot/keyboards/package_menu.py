"""کیبورد چندانتخابی بسته‌ها برای فلوی خرید."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ترتیب و متن بسته‌ها — برای تغییر لیست بسته‌ها فقط همین دیکشنری را ویرایش کنید.
PACKAGES: dict[str, str] = {
    "base": "بسته پایه",
    "extra": "بسته تکمیلی",
    "brand": "بسته برندینگ",
    "branch": "بسته شعب",
    "topping": "بسته تاپینگ (شخصی‌سازی سفارش)",
    "smartx": "بسته باشگاه مشتریان اسمارت ایکس",
    "delivery": "بسته اتصال به سامانه‌های ارسال",
    "credit": "بسته اتصال به سامانه‌های پرداخت اعتباری",
}


def package_keyboard(selected: set[str] | list[str]) -> InlineKeyboardMarkup:
    """کیبورد toggle بسته‌ها؛ گزینه‌های انتخاب‌شده با ✅ نمایش داده می‌شوند."""
    selected = set(selected)
    rows = []
    for key, title in PACKAGES.items():
        prefix = "✅ " if key in selected else ""
        rows.append(
            [InlineKeyboardButton(text=f"{prefix}{title}", callback_data=f"pkg:{key}")]
        )
    rows.append(
        [InlineKeyboardButton(text="✅ ارسال درخواست", callback_data="pkg:submit")]
    )
    rows.append([InlineKeyboardButton(text="🔙 شروع مجدد", callback_data="restart")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
