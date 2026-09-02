# Vendo Customer Bot 🤖

بات تلگرام پشتیبانی مشتریان **وندو** (`@VendoCustomerbot`) — نوشته‌شده با Python و [aiogram 3.x](https://docs.aiogram.dev) به‌صورت کاملاً async و بر پایه **Long Polling**.

## امکانات

- ✅ تشخیص مشتری فعلی وندو (و هدایت غیرمشتریان به `@vendoonlineofficial_bot`)
- 🛒 **خرید بسته جدید** — انتخاب چندگانه (toggle) از بین ۸ بسته
- ⚙️ **فعال‌سازی فیچر روی سایت** — فلوی مستقل برای هر فیچر:
  کوپن، کد تخفیف (۴ مرحله)، پاپ‌آپ (با دریافت عکس)، پیش‌سفارش (۳ مرحله)، تاپینگ، درگاه پرداخت اعتباری، ناوگان پیک
- 📚 **دریافت آموزش فعال‌سازی فیچرها**
- 📇 دریافت اطلاعات تماس (نام، مجموعه، موبایل با اعتبارسنجی ساده) در پایان هر فلو
- 📥 ارسال خلاصه کامل و مرتب هر درخواست (به‌همراه عکس پاپ‌آپ در صورت وجود) به چت ادمین
- 🔙 دکمه «شروع مجدد» و دستور `/start` در هر لحظه، fallback برای پیام‌های نامرتبط، لاگ‌گیری استاندارد

## متغیرهای محیطی

| متغیر | توضیح |
|---|---|
| `BOT_TOKEN` | توکن بات از [@BotFather](https://t.me/BotFather) |
| `ADMIN_CHAT_ID` | شناسه عددی چت ادمین که خلاصه درخواست‌ها به آن ارسال می‌شود (chat id عددی، مثلاً `123456789` یا برای گروه `-100xxxxxxxxxx`) |

نمونه در [`.env.example`](.env.example) موجود است:

```bash
cp .env.example .env
# سپس مقادیر واقعی را در .env قرار دهید
```

## اجرای لوکال (با venv)

```bash
python3.12 -m venv .venv
source .venv/bin/activate        # ویندوز: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # و مقادیر را پر کنید
export $(grep -v '^#' .env | xargs)   # لینوکس/مک — یا متغیرها را دستی set کنید

python -m bot.main
```

## اجرا با Docker / docker-compose

```bash
cp .env.example .env             # و مقادیر را پر کنید
docker compose up -d --build
docker compose logs -f           # مشاهده لاگ‌ها
```

### چرا هیچ پورتی expose نشده؟

این بات از **Long Polling** استفاده می‌کند؛ یعنی خودِ بات به‌صورت خروجی (outbound) به سرورهای تلگرام وصل می‌شود و آپدیت‌ها را می‌گیرد. **هیچ سرور HTTP یا endpointای داخل کانتینر اجرا نمی‌شود**، بنابراین:

- در `Dockerfile` هیچ `EXPOSE`ای وجود ندارد (پورتی برای گوش‌دادن نیست).
- در `docker-compose.yml` هیچ `ports:`ای تعریف نشده است.
- healthcheck کانتینر بر اساس **زنده بودن پروسه پایتون** (`pgrep`) کار می‌کند، نه پورت.

### دیپلوی روی Coolify

1. ریپازیتوری را به GitHub پوش کنید.
2. در Coolify یک ریسورس جدید از نوع **Docker Compose** (یا Dockerfile) به همین ریپو وصل کنید.
3. در بخش Environment Variables مقادیر `BOT_TOKEN` و `ADMIN_CHAT_ID` را به‌صورت secret ست کنید.
4. چون بات polling است، **نیازی به دامنه، پورت یا تنظیمات پراکسی نیست** — Health Check مبتنی بر HTTP را در Coolify غیرفعال بگذارید (healthcheck داخلی Docker خودش وضعیت را گزارش می‌دهد).
5. Deploy بزنید. ✅

## ساختار پروژه (برای توسعه آینده)

```
vendo-customer-bot/
├── bot/
│   ├── main.py                  # entrypoint — ساخت Bot/Dispatcher و اجرای polling
│   ├── config.py                # خواندن BOT_TOKEN و ADMIN_CHAT_ID از env
│   ├── states.py                # همه FSM Stateها (هر فلو یک StatesGroup مجزا)
│   ├── keyboards/
│   │   ├── main_menu.py         # کیبورد شروع و منوی اصلی
│   │   ├── package_menu.py      # لیست بسته‌ها (PACKAGES) و کیبورد toggle
│   │   ├── feature_menu.py      # لیست فیچرها و همه گزینه‌های زیرفلوها
│   │   └── common.py            # دکمه‌های تکرارشونده (بله/خیر، شروع مجدد)
│   ├── handlers/
│   │   ├── __init__.py          # ثبت روترها (fallback همیشه آخر)
│   │   ├── start.py             # /start، سوال مشتری بودن، منوی اصلی، fallback
│   │   ├── purchase_package.py  # فلوی خرید بسته (چندانتخابی)
│   │   ├── feature_activation.py# هر فیچر یک «سکشن» مستقل با هندلرهای خودش
│   │   ├── training.py          # فلوی دریافت آموزش
│   │   └── contact_info.py      # فلوی مشترک ۳مرحله‌ای اطلاعات تماس + پیام پایانی
│   └── utils/
│       └── notify_admin.py      # ساخت و ارسال خلاصه درخواست به ادمین
├── requirements.txt
├── Dockerfile                   # multi-stage، non-root، بدون EXPOSE (polling)
├── docker-compose.yml           # بدون port mapping، restart: unless-stopped
├── .env.example
└── README.md
```

### راهنمای تغییرات رایج

| می‌خواهید... | فقط این فایل را ویرایش کنید |
|---|---|
| بسته‌ای اضافه/حذف کنید | دیکشنری `PACKAGES` در `bot/keyboards/package_menu.py` |
| گزینه‌های کوپن/تخفیف/درگاه/پیک را تغییر دهید | دیکشنری‌های `bot/keyboards/feature_menu.py` |
| رفتار یک فیچر خاص را عوض کنید | سکشن همان فیچر در `bot/handlers/feature_activation.py` |
| متن سوالات اطلاعات تماس یا پیام پایانی | `bot/handlers/contact_info.py` |
| فرمت پیام خلاصه ادمین | `bot/utils/notify_admin.py` |

> **نکته:** وضعیت کاربران در `MemoryStorage` نگهداری می‌شود؛ با ری‌استارت کانتینر، فلوهای نیمه‌کاره ریست می‌شوند (کاربر کافی است `/start` بزند). در صورت نیاز به ماندگاری، می‌توانید در `bot/main.py` به `RedisStorage` سوئیچ کنید.
