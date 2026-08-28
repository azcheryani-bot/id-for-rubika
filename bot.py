import os
import time
import requests

# خواندن توکن از متغیرهای محیطی یا مقدار مستقیم
BOT_TOKEN = os.getenv(
    "RUBIKA_BOT_TOKEN",
    "CCJEHH0IACPWCTRHDDIBKJLUSPEWIIKRUPLHREXNGVHVMRVWDSGUJVKYQHEMPDCJ",
)
BASE_URL = f"https://botapi.rubika.ir/v3/{BOT_TOKEN}"


def send_message(chat_id: str, text: str, reply_to_message_id: str = None):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id

    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None


def get_updates(offset_id: str = None, limit: int = 50):
    url = f"{BASE_URL}/getUpdates"
    payload = {"limit": limit}
    if offset_id:
        payload["offset_id"] = offset_id

    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error getting updates: {e}")
    return None


def run_bot():
    print("Rubika bot is running...")
    next_offset = None

    while True:
        data = get_updates(offset_id=next_offset)

        if data:
            updates = data.get("updates", [])
            next_offset = data.get("next_offset_id", next_offset)

            for update in updates:
                update_type = update.get("type")
                chat_id = update.get("chat_id")

                # بررسی استارت ربات یا پیام جدید
                if update_type == "StartedBot":
                    # در رویداد شروع بات
                    sender_id = chat_id
                    msg = (
                        f"سلام! خوش آمدید.\n\n"
                        f"شناسه کاربری (User ID) شما: `{sender_id}`"
                    )
                    send_message(chat_id, msg)

                elif update_type == "NewMessage":
                    message = update.get("new_message", {})
                    sender_id = message.get("sender_id")
                    message_id = message.get("message_id")
                    text = message.get("text", "").strip()

                    # پاسخ به دستور start یا هر پیام متنی دریافتی
                    if text == "/start" or text == "start":
                        response_text = (
                            f"شناسه کاربری (User ID) شما:\n`{sender_id}`"
                        )
                        send_message(
                            chat_id, response_text, reply_to_message_id=message_id
                        )

        time.sleep(2)


if __name__ == "__main__":
    run_bot()