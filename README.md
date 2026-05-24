# 🚛 Isuzu Zapchast Bot

Telegram bot orqali Isuzu yuk mashinalari ehtiyot qismlarini boshqarish tizimi.  
Zapchastlarni qo'shish, qidirish va narxlarini ko'rish — barchasi Telegram ichida.

---

## ✨ Imkoniyatlar

- 🔍 **Zapchast qidirish** — nom, kod yoki model bo'yicha
- ➕ **Zapchast qo'shish** — narx, kod, model, kategoriya, miqdor va tavsif bilan
- 📦 **Barcha Isuzu modellari** — NPR, NQR, NMR, FVR va boshqalar
- 💾 **SQLite ma'lumotlar bazasi** — tezkor va ishonchli saqlash
- ⚡ **Async arxitektura** — Aiogram 3.x + SQLAlchemy async

---

## 🗂️ Fayl tuzilmasi

```
isuzu_zapchast_bot/
│
├── bot.py                  # Ishga tushurish nuqtasi
├── config.py               # .env dan sozlamalar
├── requirements.txt        # Kutubxonalar
├── .env                    # BOT_TOKEN (gitga yuklanmaydi)
│
├── handlers/
│   ├── __init__.py         # Routerlarni export qiladi
│   ├── menu.py             # /start va asosiy menyu
│   └── parts.py            # Zapchast qo'shish va qidirish
│
└── database/
    ├── __init__.py
    ├── models.py           # SQLAlchemy modeli (Part jadvali)
    └── db.py               # DB ulanish va session
```

---

## 🏗️ Arxitektura

```
Telegram foydalanuvchi
        │
        ▼
Telegram Bot API
        │
        ▼
Aiogram 3.x Dispatcher
   (Router + FSM + Middleware)
        │
        ├──────────────────────┐
        ▼                      ▼
menu.py handler          parts.py handler
(/start, menyu)     (qidirish, qo'shish)
                               │
                               ▼
                      SQLAlchemy (async)
                               │
                               ▼
                        SQLite (zapchast.db)
                         [parts jadvali]
```

---

## 🗃️ Ma'lumotlar bazasi

**`parts` jadvali:**

| Ustun | Turi | Majburiy | Tavsif |
|-------|------|----------|--------|
| `id` | Integer | ✅ | Avtomatik ID |
| `nomi` | String | ✅ | Zapchast nomi |
| `narx` | Float | ✅ | Narx (so'mda) |
| `kodi` | String | ❌ | OEM yoki zapchast kodi |
| `model` | String | ❌ | Isuzu modeli (NPR, NQR...) |
| `kategoriya` | String | ❌ | Motor, tormoz, moy... |
| `dukonda_nechta` | Integer | ❌ | Mavjud miqdor |
| `tavsif` | String | ❌ | Qo'shimcha ma'lumot |
| `sana` | DateTime | ✅ | Avtomatik (default: now) |

---

## 🚀 O'rnatish va ishga tushirish

### 1. Repozitoriyani clone qiling

```bash
git clone https://github.com/username/isuzu_zapchast_bot.git
cd isuzu_zapchast_bot
```

### 2. Virtual muhit yarating

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Kutubxonalarni o'rnating

```bash
pip install -r requirements.txt
pip install greenlet
```

### 4. `.env` faylini sozlang

```bash
cp .env.example .env
```

`.env` faylini oching va tokeningizni yozing:

```
BOT_TOKEN=your_telegram_bot_token_here
```

> Token olish uchun Telegram'da [@BotFather](https://t.me/BotFather) ga `/newbot` yuboring.

### 5. Botni ishga tushiring

```bash
python bot.py
```

---

## 📦 Requirements

```
aiogram==3.7.0
sqlalchemy
aiosqlite
python-dotenv
greenlet
```

---

## 🤖 Bot ssenariysi

```
/start
  └── Asosiy menyu
        ├── 🔍 Zapchast qidirish
        │     └── Nom / kod / model yozing
        │           └── Natijalar ko'rsatiladi
        │
        └── ➕ Zapchast qo'shish
              ├── Nomi (majburiy)
              ├── Narxi (majburiy)
              ├── Kodi (ixtiyoriy, — bilan o'tkazish)
              ├── Modeli (ixtiyoriy)
              ├── Kategoriyasi (ixtiyoriy)
              ├── Dukonda nechta (ixtiyoriy)
              └── Tavsif (ixtiyoriy)
```

---

## 🛠️ Texnologiyalar

| Texnologiya | Versiya | Maqsad |
|-------------|---------|--------|
| Python | 3.11 | Asosiy til |
| Aiogram | 3.7.0 | Telegram Bot framework |
| SQLAlchemy | 2.x | ORM (async) |
| aiosqlite | latest | Async SQLite driver |
| python-dotenv | latest | Environment variables |

---

## 📋 Rejalar (Keyingi versiya)

- [ ] Admin panel — faqat adminlar zapchast qo'sha oladi
- [ ] Zapchastni tahrirlash va o'chirish
- [ ] Barcha zapchastlar ro'yxati (pagination bilan)
- [ ] Ustalar (master) moduli
- [ ] Webhook support (production uchun)
- [ ] Docker deploy

---

## 👤 Muallif

Loyiha [GitHub](https://github.com/username/isuzu_zapchast_bot) da ochiq manba sifatida joylashtirilgan.

---

> ⭐ Agar loyiha foydali bo'lsa, GitHub'da yulduzcha qo'yishni unutmang!
