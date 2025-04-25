from fastapi import FastAPI, Request
import requests
import os
import re

app = FastAPI()

user_api_keys = {}
user_models = {}
user_modes = {}  # حالت انتخابی کاربر

TOKEN = os.environ.get("TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"
GPT_URL = "https://api.openai.com/v1/chat/completions"

def make_analysis_prompt(text):
    return f"""
Analyze the following English text sentence by sentence. For each sentence, provide:
✅ Sentence number + sentence  
✅ Translation  
📌 Grammar notes  
📌 Collocations  
📌 Difficult words  
📌 Very similar collocations (bold only the blank words)

Text:
{text}
"""

def make_followup_prompt(question):
    return f"""
Answer the following grammar or analysis question in detail, clearly, and helpfully:
{question}
"""

def make_more_explanation_prompt(text):
    return f"""
Please provide an extended explanation, examples, and tips about this text:
{text}
"""

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{TELEGRAM_API}/sendMessage", json=payload)

def send_keyboard(chat_id):
    keyboard = {
        "keyboard": [
            [{"text": "📖 تحلیل ریدینگ"}, {"text": "📘 توضیح گرامر"}, {"text": "➕ توضیح بیشتر"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    send_message(chat_id, "لطفاً نوع تحلیل مورد نظر را انتخاب کنید:", reply_markup=keyboard)

def ask_gpt(user_key, prompt, preferred_model="gpt-4"):
    fallback_models = {
        "gpt-4": "gpt-3.5",
        "gpt-3.5": None
    }

    model = preferred_model
    while model:
        headers = {
            "Authorization": f"Bearer {user_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5
        }

        response = requests.post(GPT_URL, headers=headers, json=data)

        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            return content, model
        else:
            error_text = response.text
            if "model" in error_text.lower() and ("not available" in error_text.lower() or "access" in error_text.lower()):
                model = fallback_models.get(model)
            else:
                return f"❌ GPT error: {error_text}", None

    return "❌ None of the models are available for your key.", None

@app.post("/webhook/{token}")
async def telegram_webhook(token: str,req: Request):
    try:
        if token != TOKEN:
            return {"ok": False, "error": "Invalid token"}

        body = await req.json()
        message = body.get("message", {})
        text = message.get("text", "")
        chat_id = message.get("chat", {}).get("id")

        if not text:
            return {"ok": True}

        # تنظیم کلید
        if text.startswith("/setkey"):
            _, key = text.split(maxsplit=1)
            user_api_keys[chat_id] = key.strip()
            send_message(chat_id, "✅ Your OpenAI key has been saved.")
            return {"ok": True}

        # تنظیم مدل
        if text.startswith("/setmodel"):
            _, model = text.split(maxsplit=1)
            model = model.strip().lower()
            if model not in ["gpt-3.5", "gpt-4"]:
                send_message(chat_id, "❗ Invalid model. Please choose 'gpt-3.5' or 'gpt-4'.")
                return {"ok": True}
            user_models[chat_id] = model
            send_message(chat_id, f"✅ Your preferred model '{model}' has been set.")
            return {"ok": True}

        # بررسی انتخاب نوع تحلیل
        if text in ["📖 تحلیل ریدینگ", "📘 توضیح گرامر", "➕ توضیح بیشتر"]:
            user_modes[chat_id] = text
            send_message(chat_id, "لطفاً متن خود را ارسال کنید.")
            return {"ok": True}

        if chat_id not in user_api_keys:
            send_message(chat_id, "❗ Please set your OpenAI key first using /setkey YOUR_API_KEY")
            return {"ok": True}

        if chat_id not in user_modes:
            send_keyboard(chat_id)
            return {"ok": True}

        key = user_api_keys[chat_id]
        preferred_model = user_models.get(chat_id, "gpt-4")
        selected_mode = user_modes.get(chat_id)

        # ساخت پرامپت بر اساس انتخاب کاربر
        if selected_mode == "📖 تحلیل ریدینگ":
            prompt = make_analysis_prompt(text)
        elif selected_mode == "📘 توضیح گرامر":
            prompt = make_followup_prompt(text)
        else:  # ➕ توضیح بیشتر
            prompt = make_more_explanation_prompt(text)

        result, used_model = ask_gpt(key, prompt, preferred_model)

        if used_model:
            final_response = f"*پاسخ بر اساس ChatGPT-{used_model}*\n\n{result}"
        else:
            final_response = result

        send_message(chat_id, final_response[:4000])
        return {"ok": True}
    except Exception as e:
        print("❌ خطا:", e)
        return {"ok": False, "error": str(e)}