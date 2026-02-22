"""
CAPTCHA muncul setiap ~200 klik (Cloudflare Turnstile managed).
Selesaikan manual di browser lalu restart script.

Opsi otomatis: CapSolver API (ada free trial)
https://capsolver.com
"""

def solve_manual():
    print("\n" + "="*50)
    print("🔒 CAPTCHA DIPERLUKAN!")
    print("1. Buka browser")
    print("2. Selesaikan CAPTCHA di thenanobutton.com")
    print("3. Tekan ENTER untuk lanjut")
    print("="*50)
    input("✅ Tekan ENTER setelah selesai...")
    return True
