import os
from dotenv import load_dotenv

load_dotenv()

WALLET = os.getenv("NANO_WALLET", "")
WS_TOKEN = os.getenv("WS_TOKEN", "")
REF_CODE = os.getenv("REF_CODE", "z8AyrQ")
CLICK_INTERVAL_MIN = float(os.getenv("CLICK_INTERVAL_MIN", 1.5))
CLICK_INTERVAL_MAX = float(os.getenv("CLICK_INTERVAL_MAX", 3.0))

BASE_URL = "https://thenanobutton.com"
API_URL = "https://api.thenanobutton.com"
WS_URL = f"wss://api.thenanobutton.com/ws?token={WS_TOKEN}"
