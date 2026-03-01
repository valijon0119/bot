# Render.com ga deploy qilish

## 1. Render hisobi
- [render.com](https://render.com) ga kiring, GitHub bilan ulang.

## 2. Yangi Background Worker
- Dashboard → **New +** → **Background Worker**
- **Connect repository** — GitHub’dagi `Bot` reponi tanlang.
- **Branch:** `main`

## 3. Sozlash
| Maydon | Qiymat |
|--------|--------|
| **Name** | telegram-bot (yoki xohlagan nom) |
| **Region** | Frankfurt yoki yaqin |
| **Environment** | Docker |
| **Dockerfile Path** | `./Dockerfile` (default) |

## 4. Environment Variables
**Environment** bo‘limida qo‘shing:

| Key | Value |
|-----|--------|
| `BOT_TOKEN` | `8723577678:AAHYKj1k8b1qmzIa4Gawb7P1J1mhfCys8dQ` |
| `ADMIN_GROUP_LINK` | `https://t.me/studentstiia` |

## 5. Deploy
- **Create Background Worker** bosing.
- Build va start avtomatik boshlanadi. **Logs** da xatolik bo‘lmasa, bot ishlaydi.

## Tekshirish
- **Logs** — bot ishga tushganini va xatoliklarni ko‘ring.
- Telegram’da botga xabar yuborib tekshiring.
