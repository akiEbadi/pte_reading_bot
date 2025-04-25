ngrok http 8000
answer: https://e8d5-37-27-220-205.ngrok-free.app

curl -X POST "https://api.telegram.org/bot7909895077:AAFIpzGDcJFBVaEDFFLjGiOEDq_VsZNg9HI/setWebhook" -d "url=https://e8d5-37-27-220-205.ngrok-free.app/webhook"


railway:
curl -F "url=https://ptereadingbot-production.up.railway.app/webhook/7909895077:AAFIpzGDcJFBVaEDFFLjGiOEDq_VsZNg9HI" https://api.telegram.org/bot7909895077:AAFIpzGDcJFBVaEDFFLjGiOEDq_VsZNg9HI/setWebhook

curl -X POST https://api.telegram.org/bot7909895077:AAFIpzGDcJFBVaEDFFLjGiOEDq_VsZNg9HI/setWebhook \
-d "url=https://ptereadingbot-production.up.railway.app/webhook"


curl https://api.telegram.org/bot7909895077:AAFIpzGDcJFBVaEDFFLjGiOEDq_VsZNg9HI/getWebhookInfo

uvicorn main:app --host 0.0.0.0 --port 8080 --reload