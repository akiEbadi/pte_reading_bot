ngrok http 8000
answer: https://e8d5-37-27-220-205.ngrok-free.app

curl -X POST "https://api.telegram.org/bot7909895077:AAEFh86hAHDsiYYNPPrOD2lvSKuK8gi1oTw/setWebhook" -d "url=https://e8d5-37-27-220-205.ngrok-free.app/webhook"


railway:
curl -F "url= ptereadingbot-production.up.railway.app/webhook/7909895077:AAHoISEIq60n2biRwOni5760vgrJvvDuYZc" https://api.telegram.org/bot7909895077:AAHoISEIq60n2biRwOni5760vgrJvvDuYZc/setWebhook

curl -X POST https://api.telegram.org/bot7909895077:AAHoISEIq60n2biRwOni5760vgrJvvDuYZc/setWebhook \
-d "url=ptereadingbot-production.up.railway.app/webhook"


curl https://api.telegram.org/bot7909895077:AAHoISEIq60n2biRwOni5760vgrJvvDuYZc/getWebhookInfo

uvicorn main:app --host 0.0.0.0 --port 8080 --reload