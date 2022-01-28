from itsdangerous import URLSafeTimedSerializer, SignatureExpired,BadTimeSignature

s = URLSafeTimedSerializer('Thisisasecret!')


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