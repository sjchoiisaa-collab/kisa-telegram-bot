import os
import requests
import xml.etree.ElementTree as ET

# ===== 환경변수 =====
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# ===== KISA RSS 주소 =====
RSS_URL = "https://knvd.krcert.or.kr/rss/securityNotice.do"

# ===== 텔레그램 전송 =====
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    print("Telegram response:", response.text)


# ===== 마지막 공지 저장 =====
def get_last_id():
    if not os.path.exists("last_id.txt"):
        return None
    with open("last_id.txt", "r") as f:
        return f.read().strip()


def save_last_id(guid):
    with open("last_id.txt", "w") as f:
        f.write(guid)


# ===== 공지 체크 =====
def check_notice():
    print("Checking KISA RSS...")

    response = requests.get(RSS_URL)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    # 네임스페이스 제거 처리
    for elem in root.iter():
        if "}" in elem.tag:
            elem.tag = elem.tag.split("}", 1)[1]

    items = root.findall(".//item")

    if not items:
        print("No items found in RSS.")
        return

    latest = items[0]

    title_elem = latest.find("title")
    link_elem = latest.find("link")
    guid_elem = latest.find("guid")

    if title_elem is None or link_elem is None or guid_elem is None:
        print("RSS structure unexpected.")
        return

    title = title_elem.text
    link = link_elem.text
    guid = guid_elem.text

    last_id = get_last_id()

    if guid != last_id:
        message = f"📢 KISA 보안공지\n\n{title}\n{link}"
        send_telegram(message)
        save_last_id(guid)
        print("New notice sent!")
    else:
        print("No new notice.")


if __name__ == "__main__":
    check_notice()
