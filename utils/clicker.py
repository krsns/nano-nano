import json
import time
import requests

click_count = 0
clicks_since_captcha = 0
total_earned = 0.0
captcha_required = False

CLICK_INTERVAL = 0.3
AUTO_WD_EVERY = 100000  # withdraw tiap 100k klik

WALLET = ""  # diisi dari main.py
API_URL = "https://api.thenanobutton.com"
WS_TOKEN = ""  # diisi dari main.py

def set_config(wallet: str, token: str):
    global WALLET, WS_TOKEN
    WALLET = wallet
    WS_TOKEN = token

def do_withdraw():
    """Kirim request withdraw ke API"""
    try:
        r = requests.post(
            f"{API_URL}/api/withdraw",
            json={"wallet": WALLET},
            headers={
                "Content-Type": "application/json",
                "Origin": "https://thenanobutton.com",
                "Referer": "https://thenanobutton.com/",
                "Authorization": f"Bearer {WS_TOKEN}"
            },
            timeout=10
        )
        print(f"\n💸 WITHDRAW | Status: {r.status_code} | Response: {r.text[:100]}")
    except Exception as e:
        print(f"❌ Withdraw error: {e}")

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
        print(f"   💰 Balance       : {current_nano} nano")
        print(f"   🖱️  Since captcha : {clicks_since_captcha}/200")
        print(f"   🔒 CAPTCHA needed: {captcha_required}\n")

    elif msg_type == "click":
        click_count += 1
        clicks_since_captcha = data.get("clicksSinceCaptcha", clicks_since_captcha + 1)
        amount = data.get("amount", 0)
        total_earned += amount
        remaining = 200 - clicks_since_captcha
        print(f"🖱️  #{click_count:>6} | +{amount} nano | total: {total_earned:.4f} | captcha in: {remaining}")

        # Auto withdraw tiap 100k klik
        if click_count % AUTO_WD_EVERY == 0:
            print(f"\n🔔 {AUTO_WD_EVERY} klik tercapai! Memulai withdraw...")
            do_withdraw()

    elif msg_type == "hourlylimit":
        print("⏳ Rate limit! Tunggu 10 detik...")
        time.sleep(10)

    elif msg_type == "captcharequired":
        captcha_required = True
        print("\n🔒 CAPTCHA muncul! Script dijeda...")
        print("   Selesaikan di browser lalu tekan ENTER")
        input("✅ ENTER untuk lanjut... ")
        captcha_required = False

    elif msg_type == "error":
        print(f"❌ Error: {data.get('message', 'Unknown')}")

def send_click(ws):
    ws.send(json.dumps({}))

def click_loop(ws):
    global captcha_required
    time.sleep(1.5)

    print(f"🚀 Auto clicker mulai! (interval: {CLICK_INTERVAL}s)")
    print(f"💸 Auto withdraw setiap {AUTO_WD_EVERY:,} klik\n")

    while True:
        if captcha_required:
            time.sleep(1)
            continue
        try:
            send_click(ws)
            time.sleep(CLICK_INTERVAL)
        except Exception as e:
            print(f"❌ Klik error: {e}")
            time.sleep(3)
            break
