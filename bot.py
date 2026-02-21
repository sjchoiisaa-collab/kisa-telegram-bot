import os
import requests
import xml.etree.ElementTree as ET
import json

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

RSS_URL = "https://www.kisa.or.kr/rss/notice_security.xml"
STATE_FILE = "last_id.txt"


def get_last_id():
    try:
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    except:
        return None


def save_last_id(last_id):
    with open(STATE_FILE, "w") as f:
        f.write(last_id)


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)


def check_notice():
    response = requests.get(RSS_URL)
    root = ET.fromstring(response.content)

    # 모든 item 중 첫 번째 가져오기
    latest = root.findall(".//item")[0]

    title = latest.find("title").text
    link = latest.find("link").text
    guid = latest.find("guid").text

    last_id = get_last_id()

    if guid != last_id:
        message = f"📢 KISA 보안공지\n\n{title}\n{link}"
        send_telegram(message)
        save_last_id(guid)

if __name__ == "__main__":
    check_notice()
