from passlib.hash import pbkdf2_sha256

def hash_password(password):
    hashed = pbkdf2_sha256.hash(password)
    return hashed

def check_password(password, hashed):
    return pbkdf2_sha256.verify(password, hashed)