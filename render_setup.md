# Render uchun Telegram Bot Sozlashi

## 1. Render.com ga o'ting
1. render.com saytiga o'ting
2. Hisobingizga kiring yoki ro'yxatdan o'ting

## 2. Yangi Web Service yarating
1. Dashboardda "New +" tugmasini bosing
2. "Web Service" tanlang
3. GitHub repository ni ulang yoki "Build and deploy from a Git repository" tanlang

## 3. Repository sozlamalari

### Agar GitHub ishlatsangiz:
1. Kodlarni GitHub ga yuklang
2. Render da repository ni tanlang

### Agar GitHub ishlatmasangiz:
1. "Create a new repository" tanlang
2. Fayllarni yuklang:
   - bot.py
   - requirements.txt
   - Dockerfile
   - .env (yoki environment variables)

## 4. Environment Variables
Render da quyidagi environment variables qo'shing:

**Environment** → **Environment Variables** → **Add**:
- Name: `BOT_TOKEN`
- Value: `8271555595:AAFGclSWBtviAFXJyb6TYQzvQ-J9cxA4qpo`
- Name: `ADMIN_GROUP_LINK`
- Value: `https://t.me/studentstiia`

## 5. Build va Deploy sozlamalari

### Build Command:
```
pip install -r requirements.txt
```

### Start Command:
```
python bot.py
```

### Runtime:
- Python 3.11
- Region: eng yaqin region (masalan: Oregon)
- Instance Type: Free

## 6. Health Check (ixtiyoriy)
Health Check Path: `/` (yoki health check endpoint qo'shing)

## 7. Deploy
"Create Web Service" tugmasini bosing va deploy kuting.

## Render afzalliklari:
✅ Bepul plan (750 soat/oy)
✅ Avtomatik deploy
✅ SSL sertifikati
✅ Monitoring
✅ Loglar
✅ Custom domain (pro plan)

## Ishga tushirishdan oldin tekshirish:
1. Bot token to'g'ri ekanligini tekshiring
2. Kanal linki to'g'ri ekanligini tekshiring
3. Fayllar to'g'ri yuklanganligini tekshiring

## Agar xatolik bo'lsa:
1. Render loglarini tekshiring
2. Environment variables to'g'ri ekanligini tekshiring
3. Python versiyasi mos kelishini tekshiring
