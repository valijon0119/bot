# Replit uchun Telegram Bot Sozlashi

## 1. Replitda yangi loyiha yaratish
1. replit.com ga o'ting
2. "+ Create Repl" tugmasini bosing
3. "Python" tanlang
4. Loyiha nomini kiriting (masalan: telegram-file-bot)

## 2. Fayllarni yuklash
Quyidagi fayllarni Replitga yuklang:
- bot.py (asosiy kod)
- requirements.txt (kutubxonalar)
- .env (konfiguratsiya)

## 3. Replit maxsus sozlamalari

### Secrets qo'shish:
Replit da Secrets qo'shish uchun:
1. Chap tomondagi "Tools" tugmasini bosing
2. "Secrets" ni tanlang
3. Quyidagi secretlarni qo'shing:
   - Key: BOT_TOKEN
   - Value: 8271555595:AAFGclSWBtviAFXJyb6TYQzvQ-J9cxA4qpo
   - Key: ADMIN_GROUP_LINK
   - Value: https://t.me/studentstiia

### .env fayli o'rniga:
Replit da .env fayl o'rniga environment variables ishlatiladi:
```python
import os
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_GROUP_LINK = os.getenv('ADMIN_GROUP_LINK')
```

## 4. Kutubxonalarni o'rnatish
Replit da avtomatik o'rnatiladi, lekin kerak bo'lsa:
```bash
pip install python-telegram-bot==20.7 python-dotenv==1.0.0 httpx==0.24.1
```

## 5. Botni ishga tushirish
```bash
python bot.py
```

## 6. Web sozlash (ixtiyoriy)
Agar doimiy ishlash kerak bo'lsa:
1. "Keep Alive" qo'shing (uptime robot)
2. Yoki Replit ning avtomatik sleep funksiyasini o'chirish

## Replit afzalliklari:
✅ Avtomatik kutubxona o'rnatish
✅ 24/7 ishlash (bilan bepul versiyada)
✅ Online kod tahrirlash
✅ Tez deploy
✅ GitHub integratsiyasi
