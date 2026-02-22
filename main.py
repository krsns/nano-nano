import threading
import websocket
import time
import json
from utils.clicker import handle_message, click_loop

def on_open(ws):
    print("✅ WebSocket connected!")
    t = threading.Thread(target=click_loop, args=(ws,), daemon=True)
    t.start()

def on_error(ws, error):
    print(f"❌ WS Error: {error}")

def on_close(ws, code, reason):
    print(f"🔌 WS Closed: {code} - {reason}")
    print("🔄 Reconnecting dalam 3 detik...")
    time.sleep(3)

def main():
    print("=" * 50)
    print("  🖱️  NanoButton AutoClicker")
    print("=" * 50)

    # Input token saat start
    print("\n📋 Cara dapat token:")
    print("   Buka thenanobutton.com → F12 → Console")
    print("   localStorage.getItem('nanosessiontoken')\n")

    wallet = input("💳 Masukkan Nano Wallet Address: ").strip()
    token = input("🔑 Masukkan WS Token: ").strip()

    if not wallet or not token:
        print("❌ Wallet dan token tidak boleh kosong!")
        return

    ws_url = f"wss://api.thenanobutton.com/ws?token={token}"

    print(f"\n💳 Wallet : {wallet[:20]}...")
    print(f"🔑 Token  : {token[:20]}...")
    print(f"⚡ Interval: 0.3 detik/klik")
    print(f"🌐 Connecting...\n")

    while True:
        try:
            ws = websocket.WebSocketApp(
                ws_url,
                on_open=on_open,
                on_message=handle_message,
                on_error=on_error,
                on_close=on_close
            )
            ws.run_forever(ping_interval=30, ping_timeout=10)
        except KeyboardInterrupt:
            print("\n👋 Script dihentikan.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()
