"""ثبت روترها به‌ترتیب صحیح — روتر fallback باید همیشه آخر باشد."""

from aiogram import Router

from bot.handlers import (
    contact_info,
    feature_activation,
    purchase_package,
    start,
    training,
)


def setup_routers() -> Router:
    """ساخت روتر اصلی شامل همه روترهای بات."""
    root = Router(name="root")
    root.include_router(start.router)
    root.include_router(contact_info.router)
    root.include_router(purchase_package.router)
    root.include_router(feature_activation.router)
    root.include_router(training.router)
    # fallback حتماً باید آخر ثبت شود تا پیام‌های نامرتبط را بگیرد
    root.include_router(start.fallback_router)
    return root
