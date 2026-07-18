# Telegram Monitoring Bot

Qoraqalpog'iston tumanlari kanallarida ma'lumot qidirish uchun Telegram bot.

## 🚀 O'rnatish

1. **Kutubxonalarni o'rnatish:**
```bash
pip install -r requirements.txt
```

2. **`.env` faylini yaratish:**
```bash
cp .env.example .env
```

3. **`.env` faylini to'ldirish:**
- `TOKEN` - BotFather'dan olingan bot tokeni
- `API_ID` - https://my.telegram.org saytidan olingan API ID
- `API_HASH` - https://my.telegram.org saytidan olingan API Hash

## 📚 API Credentials olish

1. **Bot Token:**
   - Telegram'da @BotFather botini toping
   - `/newbot` buyrug'ini yuboring
   - Bot nomi va username kiriting
   - Tokenni nusxalab `.env` fayliga joylang

2. **API ID va Hash:**
   - https://my.telegram.org saytiga kiring
   - Login qiling
   - "API development tools" bo'limiga o'ting
   - Yangi application yarating
   - API ID va API Hashni oling va `.env` fayliga joylang

## ▶️ Botni ishga tushirish

```bash
python bot.py
```

## 🎯 Funksiyalar

- **📍 Tumanlar bo'yicha qidiruv** - Qoraqalpog'iston tumanlari kanallarida qidirish
- **➕ Yangi kanal qo'shish** - Yangi kanallarni bazaga qo'shish
- **⏳ Vaqt bo'yicha filtrlash** - 24 soat yoki 7 kun ichidagi xabarlar

## 📋 Qo'llab-quvvatlanadigan tumanlar

- Нөкис қаласы
- Амударья районы
- Беруний районы
- Бозатаў районы
- Кегейли районы
- Қараөзек районы
- Қанликөл районы
- Қоңырат районы
- Мойнақ районы
- Нөкис районы
- Тахтакөпир районы
- Тақыятас районы
- Тўрткўл районы
- Хожели районы
- Шымбай районы
- Шоманай районы
- Елликқала районы

Har bir tumanda ikkita kanal turi mavjud:
- 🏢 Kotibiyat
- 🏛 Hokimlik

## ⚠️ Eslatmalar

- Bot birinchi marta ishga tushganda telefon raqami orqali Telegram hisobingizga kirish so'raladi
- Sessiya fayli avtomatik yaratiladi va keyingi ishga tushirishlarda avtomatik ishlatiladi
- Kanallardan qidirish uchun bot ushbu kanallarga a'zo bo'lishi shart
