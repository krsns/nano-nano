import threading
import websocket
from config import WS_URL, WALLET, WS_TOKEN
from utils.clicker import handle_message, click_loop

def on_open(ws):
    print("✅ WebSocket connected!")
    t = threading.Thread(target=click_loop, args=(ws,), daemon=True)
    t.start()

def on_error(ws, error):
    print(f"❌ WS Error: {error}")

def on_close(ws, code, reason):
    print(f"🔌 WS Closed: {code} - {reason}")

def main():
    print("=" * 50)
    print("  🖱️  NanoButton AutoClicker")
    print("=" * 50)

    if not WS_TOKEN:
        print("\n⚠️  WS_TOKEN belum diisi di .env!")
        print("Ambil dari browser:")
        print("  F12 → Console → localStorage.getItem('nanosessiontoken')")
        return

    if not WALLET:
        print("\n⚠️  NANO_WALLET belum diisi di .env!")
        return

    print(f"\n💳 Wallet: {WALLET[:20]}...")
    print(f"🔑 Token : {WS_TOKEN[:20]}...\n")

    while True:
        try:
            ws = websocket.WebSocketApp(
                WS_URL,
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
            import time
            time.sleep(5)

if __name__ == "__main__":
    main()
