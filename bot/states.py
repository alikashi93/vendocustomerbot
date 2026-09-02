"""تعریف تمام Stateهای FSM بات.

هر فلو StatesGroup مخصوص خودش را دارد تا ویرایش هر بخش مستقل باشد.
"""

from aiogram.fsm.state import State, StatesGroup


class PurchaseStates(StatesGroup):
    """فلوی خرید بسته جدید (چندانتخابی)."""

    selecting_packages = State()


class CouponStates(StatesGroup):
    """فلوی فعال‌سازی کوپن."""

    choosing = State()
    custom_text = State()  # حالت «سایر» — دریافت متن آزاد


class DiscountStates(StatesGroup):
    """فلوی فعال‌سازی کد تخفیف (۴ مرحله)."""

    choosing_discount = State()
    custom_discount = State()      # «سایر» در مرحله ۱
    choosing_code = State()
    custom_code = State()          # «سایر» در مرحله ۲
    start_date = State()           # مرحله ۳ — متن آزاد
    end_date = State()             # مرحله ۴ — متن آزاد


class PopupStates(StatesGroup):
    """فلوی فعال‌سازی پاپ‌آپ."""

    discount_text = State()        # مرحله ۱ — متن آزاد
    has_image = State()            # مرحله ۲ — بله/خیر
    waiting_image = State()        # دریافت عکس
    use_template = State()         # سوال تمپلیت


class PreorderStates(StatesGroup):
    """فلوی فعال‌سازی پیش‌سفارش (۳ مرحله متنی)."""

    days_before = State()
    minutes_to_kitchen = State()
    minutes_before_slot = State()


class TrainingStates(StatesGroup):
    """فلوی دریافت آموزش."""

    choosing = State()
    custom_text = State()  # «سایر» — متن آزاد


class ContactStates(StatesGroup):
    """فلوی مشترک دریافت اطلاعات تماس (۳ مرحله)."""

    full_name = State()
    business_name = State()
    phone = State()
