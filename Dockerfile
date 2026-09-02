# syntax=docker/dockerfile:1

# ---------------------------------------------------------------------------
# Stage 1: Builder — نصب وابستگی‌ها در یک virtualenv مجزا
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------------------------------------------------------
# Stage 2: Runtime — ایمیج نهایی سبک با کاربر non-root
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# procps برای دستور pgrep در HEALTHCHECK لازم است (در ایمیج slim وجود ندارد)
RUN apt-get update \
    && apt-get install -y --no-install-recommends procps \
    && rm -rf /var/lib/apt/lists/*

# ساخت کاربر غیر root برای امنیت بیشتر
RUN groupadd --system app && useradd --system --gid app --home-dir /app app

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY bot/ ./bot/

USER app

# نکته: این بات از Long Polling استفاده می‌کند و خودش به سرور تلگرام وصل می‌شود؛
# هیچ سرور HTTP یا endpointای داخل کانتینر اجرا نمی‌شود.
# بنابراین به‌صورت عمدی هیچ پورتی EXPOSE نشده است — نیازی به پورت نیست.
# healthcheck نیز بر پایه زنده بودن پروسه پایتون است، نه پورت.

HEALTHCHECK --interval=60s --timeout=10s --start-period=15s --retries=3 \
    CMD pgrep -f "bot.main" > /dev/null || exit 1

CMD ["python", "-m", "bot.main"]
