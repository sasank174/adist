from itsdangerous import URLSafeTimedSerializer, SignatureExpired,BadTimeSignature
from dotenv import load_dotenv
load_dotenv()
import os

s = URLSafeTimedSerializer(os.getenv("SSECRET_KEY"))

def create(inp,salt):
    token = s.dumps(inp, salt=salt)
    return token


def check(inp,salt):
    try:
        value = s.loads(inp, salt=salt, max_age=900) # 900 seconds = 15 minutes
        value.append("valid")
    except SignatureExpired:
        value = s.loads(inp, salt=salt)
        value.append("expired")
        return value
    except BadTimeSignature:
        return "invalid"
    except Exception as e:
        return "invalid"
    return value

def get(inp,salt):
    try:
        value = s.loads(inp, salt=salt)
    except BadTimeSignature:
        return "invalid"
    return value

# ============================================================
def adcreate(inp):
    token = s.dumps(inp, salt="ad-unit")
    return token

def advalidate(inp):
    try:
        value = s.loads(inp, salt="ad-unit", max_age=120) # 120 seconds = 2 minutes
        return value
    except SignatureExpired:
        return "expired"
    except BadTimeSignature:
        return "invalid"