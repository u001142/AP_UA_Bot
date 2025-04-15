# АвтоПомічникUA (@AP_UA_Bot)

Телеграм-бот-помічник з ремонту всіх марок авто, який працює на базі GPT через OpenRouter.

## Команди:
- `/start` — привітання
- `/setcar` — встановити авто, приклад: `/setcar Toyota Corolla 2008`
- `/ask` — поставити питання: `/ask Що робити якщо не заводиться?`

## Деплой на Render:
1. Створи Web Service на [render.com](https://render.com)
2. Завантаж .env (на базі .env.example)
3. Встанови Webhook URL: `https://your-app-name.onrender.com/<WEBHOOK_SECRET>`