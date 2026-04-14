import pyotp
import os
from dotenv import load_dotenv
import time
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / '.env')

key = os.getenv("tuOTP")

def getOTP():
    if key is None:
        return "Fehler"
    totp = pyotp.TOTP(key)

    remaining = totp.interval - (time.time() % totp.interval)
    if remaining < 5:
        print(f"OTP fas abgelaufen {remaining:.1}s")
        time.sleep(remaining + 2)
        
    return totp.now()

print(getOTP())