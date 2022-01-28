import bcrypt


def validate(password, hashed):
    password,hashed = bytes(password, 'utf-8'),bytes(hashed, 'utf-8')
    if bcrypt.checkpw(password, hashed):
        return True
    else:
        return False

def create(password):
    password = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    salt,hashed = salt.decode("utf-8"),hashed.decode("utf-8")
    return salt,hashed