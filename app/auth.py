import bcrypt
import pyjwt as jwt # Se usará PyJWT o python-jose dependiendo de la versión
import pyotp
import datetime
import os
from fastapi import HTTPException
from pydantic import BaseModel

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-teamlyx-2025")
ALGORITHM = "HS256"

class LoginRequest(BaseModel):
    username: str
    password: str
    totp_code: str = None  # opcional si no tiene 2FA

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=12) # Sesiones largas
    to_encode.update({"exp": expire})
    
    # Intenta usar PyJWT o Jwt normal
    import jwt as pyjwt
    encoded_jwt = pyjwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_totp(secret: str, code: str) -> bool:
    if not secret:
        return True
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
