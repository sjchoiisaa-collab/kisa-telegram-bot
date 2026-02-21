import os
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

message = "🔥 KISA 보안 공지 테스트 메시지"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

payload = {
    "chat_id": 8518888462,
    "text": message
}

requests.post(url, data=payload)
