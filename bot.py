import time
import requests

# حتماً توکن خود را در این متغیر قرار دهید
BOT_TOKEN = "CCJEHH0IACPWCTRHDDIBKJLUSPEWIIKRUPLHREXNGVHVMRVWDSGUJVKYQHEMPDCJ"
BASE_URL = f"https://botapi.rubika.ir/v3/{BOT_TOKEN}"

def run_bot():
    print("ربات در حال اجراست...")
    
    # تست اتصال اولیه
    me_res = requests.post(f"{BASE_URL}/getMe")
    print("وضعیت توکن:", me_res.json())

    next_offset = None

    while True:
        payload = {"limit": 50}
        if next_offset:
            payload["offset_id"] = next_offset

        try:
            req = requests.post(f"{BASE_URL}/getUpdates", json=payload, timeout=10)
            data = req.json()

            if "updates" in data and data["updates"]:
                for update in data["updates"]:
                    update_type = update.get("type")
                    chat_id = update.get("chat_id")
                    
                    sender_id = None
                    
                    # استخراج شناسه کاربری بر اساس نوع رویداد
                    if update_type == "StartedBot":
                        sender_id = chat_id
                    elif update_type == "NewMessage":
                        sender_id = update.get("new_message", {}).get("sender_id")

                    if sender_id:
                        msg = f"سلام! شناسه کاربری شما:\n`{sender_id}`"
                        
                        # ارسال پیام
                        requests.post(
                            f"{BASE_URL}/sendMessage", 
                            json={"chat_id": chat_id, "text": msg}
                        )
                        print(f"پاسخ به {sender_id} ارسال شد.")

                # آپدیت کردن افست برای دریافت پیام‌های بعدی
                next_offset = data.get("next_offset_id")

        except Exception as e:
            print("خطا:", e)

        time.sleep(3) # وقفه 3 ثانیه ای برای جلوگیری از بلاک شدن

if __name__ == "__main__":
    run_bot()
