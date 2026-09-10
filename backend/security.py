import hashlib, re

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, stored: str) -> bool:
    return hash_password(password) == stored

def strong_password(password: str) -> bool:
    return bool(len(password) >= 8 and re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'\d', password) and re.search(r'[^A-Za-z0-9]', password))
