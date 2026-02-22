import json
import time
import random
from config import CLICK_INTERVAL_MIN, CLICK_INTERVAL_MAX

click_count = 0
clicks_since_captcha = 0
total_earned = 0.0
captcha_required = False

def handle_message(ws, message: str):
    global click_count, clicks_since_captcha, total_earned, captcha_required

    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        return

    msg_type = data.get("type", "")

    if msg_type == "init":
        session = data.get("session", {})
        clicks_since_captcha = session.get("clicksSinceCaptcha", 0)
        captcha_required = session.get("captchaRequired", False)
        current_nano = session.get("currentNano", 0)
        print(f"📊 Session aktif")
        print(f"   💰 Balance: {current_nano} nano")
        print(f"   🖱️  Clicks since captcha: {clicks_since_captcha}/200")
        print(f"   🔒 CAPTCHA required: {captcha_required}")

    elif msg_type == "click":
        click_count += 1
        clicks_since_captcha = data.get("clicksSinceCaptcha", clicks_since_captcha + 1)
        amount = data.get("amount", 0)
        total_earned += amount
        remaining = 200 - clicks_since_captcha
        print(f"🖱️  Klik #{click_count} | +{amount} nano | CAPTCHA in: {remaining} klik")

    elif msg_type == "hourlylimit":
        print("⏳ Rate limit! Menunggu 10 detik...")
        time.sleep(10)

    elif msg_type == "captcharequired":
        captcha_required = True
        print("🔒 CAPTCHA diperlukan! Script dijeda...")

    elif msg_type == "error":
        print(f"❌ Server error: {data.get('message', 'Unknown')}")

    elif msg_type == "stats":
        online = data.get("onlineUsers", 0)
        print(f"👥 Online: {online}", end="\r")

def send_click(ws):
    ws.send(json.dumps({}))

def click_loop(ws):
    global captcha_required
    time.sleep(2)

    print(f"\n🚀 Auto clicker mulai!")
    print(f"   Interval: {CLICK_INTERVAL_MIN}-{CLICK_INTERVAL_MAX} detik\n")

    while True:
        if captcha_required:
            print("⏸️  Pause karena CAPTCHA...")
            time.sleep(30)
            continue
        try:
            send_click(ws)
            time.sleep(random.uniform(CLICK_INTERVAL_MIN, CLICK_INTERVAL_MAX))
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)
