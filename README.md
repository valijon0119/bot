# Telegram Fayl Yuborish Boti (Admin Boshqaruvi bilan)

Bu Telegram boti barcha foydalanuvchilar tomonidan yuborilgan fayllarni (PDF, Word, rasmlar) admin guruhiga avtomatik ravishda yuboradi. Guruhni admin o'zi biriktiradi va ovozli xabarlar bilan stikerlar bloklangan.

## O'rnatish

1. Python 3.7+ o'rnatilganligini tekshiring
2. Kerakli kutubxonalarni o'rnatish:
```bash
pip install -r requirements.txt
```

## Sozlash

1. `.env` faylini oching
2. `BOT_TOKEN` ni kiriting (already configured)

Guruh linkini bot ishga tushirilgandan so'ng admin orqali o'rnatiladi:
- `/login` - Admin tizimiga kirish
- `/setgroup` - Guruh linkini o'rnatish

### Guruh link formatlari:

1. **Ochiq guruh uchun**: `https://t.me/guruh_nomi`
2. **Shaxsiy guruh uchun**: `https://t.me/joinchat/ABC123DEF456`
3. **To'g'ridan-to'g'ri ID uchun**: `-1001234567890`

## Ishga tushirish

```bash
python bot.py
```

## Funksiyalar

- ✅ **Barcha foydalanuvchilar uchun** - Fayl yuborishga ruxsat berilgan
- ✅ **Admin boshqaruvi** - Guruhni admin o'zi biriktiradi
- ✅ **Taqiqlangan kontent** - Ovozli xabarlar va stikerlar bloklangan
- ✅ **PDF fayllarini qabul qilish** va yuborish
- ✅ **Word hujjatlarini** (.doc, .docx) qabul qilish va yuborish
- ✅ **Rasmlarni** (JPG, PNG, GIF, WebP) qabul qilish va yuborish
- ✅ **Foydalanuvchi uchun qulay interfeys** (o'zbek tilida)
- ✅ **Xatoliklarni boshqarish**
- ✅ **Loglarni saqlash**

## Admin Autentifikatsiyasi

### Admin Ro'yxatdan O'tish
- `/register` buyrug'i orqali yangi admin yaratish
- Foydalanuvchi nomi va parolni kiritish talab qilinadi
- Parol ikki marta kiritiladi (tasdiqlash uchun)
- Ma'lumotlar `admin_data.json` fayliga saqlanadi

### Tizimga Kirish
- `/login` buyrug'i bilan tizimga kirish
- Foydalanuvchi nomi va parolni kiritish
- Muvaffaqiyatli kirishdan so'ng 24 soat davomida sessiya faol bo'ladi

### Admin Buyruqlari
- `/setgroup` - Guruh linkini o'rnatish
- `/logout` - Tizimdan chiqish
- `/status` - Admin holatini ko'rish
- `/cancel` - Jarayonni bekor qilish (login/registratsiyada)

## Qo'llab-quvvatlanadigan fayl turlari

- PDF fayllar (.pdf)
- Microsoft Word hujjatlari (.doc, .docx)
- Rasmlar (.jpg, .png, .gif, .webp)

## ❌ Qo'llab-quvvatlanmaydigan kontent

- Ovozli xabarlar
- Stikerlar
- Video xabarlar
- Audio xabarlar
- Oddiy text xabarlar (faqat buyruqlar qabul qilinadi)

## Bot Token

Bot token: `.env` faylida yoki `fly secrets` da `BOT_TOKEN` o'rnatiladi.

## Xavfsizlik

- Barcha parollar SHA-256 bilan hashlangan holda saqlanadi
- Faqat adminlar guruh linkini o'zgartira oladi
- Sessiyalar 24 soatdan keyin avtomatik ravishda tugaydi
- Admin ma'lumotlari `admin_data.json` faylda saqlanadi
- Guruh konfiguratsiyasi `group_config.json` faylda saqlanadi

## Fayllar Tuzilishi

```
Bot/
├── bot.py              # Asosiy bot kodi
├── requirements.txt     # Kerakli kutubxonalar
├── .env               # Konfiguratsiya fayli (BOT_TOKEN)
├── admin_data.json    # Admin ma'lumotlari (avtomatik yaratiladi)
├── group_config.json  # Guruh konfiguratsiyasi (avtomatik yaratiladi)
└── README.md          # Qo'llanma
```

## Muhit O'zgaruvchilari

`.env` faylida quyidagi o'zgaruvchilar mavjud:

```env
BOT_TOKEN=your_bot_token_from_@BotFather
ADMIN_GROUP_LINK=  # ixtiyoriy, asosiy konfiguratsiya bot orqali amalga oshiriladi
```

## Buyruqlar

### Umumiy buyruqlar (barcha foydalanuvchilar uchun)
- `/start` - Botni ishga tushirish
- `/help` - Yordam ma'lumotlari

### Admin buyruqlari
- `/register` - Ro'yxatdan o'tish
- `/login` - Tizimga kirish
- `/setgroup` - Guruh linkini o'rnatish
- `/logout` - Tizimdan chiqish
- `/status` - Admin holatini ko'rish
- `/cancel` - Jarayonni bekor qilish

## Foydalanish

1. **Botni ishga tushiring**: `python bot.py`
2. **Admin sifatida ro'yxatdan o'ting**: `/register`
3. **Tizimga kiring**: `/login`
4. **Guruh linkini o'rnating**: `/setgroup`
5. **Barcha foydalanuvchilar endi fayl yuborishi mumkin!**
