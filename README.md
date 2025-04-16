
# АвтоПомічникUA (@AP_UA_Bot)

Телеграм-бот для допомоги з ремонтом авто будь-якої марки на базі ШІ (OpenRouter + FastAPI + Webhook)

## Команди:
- /start — запуск
- /choosecar — вибір авто по логотипу
- /ask — поставити запитання по авто

## Як розгорнути:
1. Створи `.env` на основі `.env.example`
2. Встанови залежності: `pip install -r requirements.txt`
3. Запусти локально або на Render:  
   `uvicorn main:app --host 0.0.0.0 --port 10000`
