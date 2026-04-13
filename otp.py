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
    return totp.now()

print(getOTP())