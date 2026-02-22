from curl_cffi import requests as cf_requests
from config import BASE_URL, REF_CODE, API_URL

def get_session_token(wallet: str) -> str:
    """
    Ambil session token dari API.
    Token juga bisa diambil manual dari browser:
    localStorage.getItem('nanosessiontoken')
    """
    session = cf_requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
        "Referer": f"{BASE_URL}/{REF_CODE}",
        "Origin": BASE_URL,
    }

    session.get(
        f"{BASE_URL}/{REF_CODE}",
        impersonate="chrome120",
        headers=headers
    )

    r = session.get(
        f"{API_URL}/api/session",
        impersonate="chrome120",
        headers=headers,
        params={"wallet": wallet}
    )

    data = r.json()
    token = data.get("token", "")
    print(f"✅ Token didapat: {token[:20]}...")
    return token
