import sys
import os

# Asegurar que reconozca los módulos de app
sys.path.append(os.path.dirname(__file__))

from app.db import get_conn
from app.auth import get_password_hash
import pyotp

def crear_admin(username, password, enable_2fa=False):
    hashed = get_password_hash(password)
    totp_secret = pyotp.random_base32() if enable_2fa else None

    # Omitimos el chequeo seguro para simplificar el instalador local
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO usuarios (username, password_hash, totp_secret) VALUES (%s, %s, %s)",
                    (username, hashed, totp_secret)
                )
        print(f"\n✅ Usuario '{username}' creado exitosamente en la base de datos de producción.")
        if enable_2fa:
            print(f"🔐 Se habilitó Doble Factor. Configúralo en Google Authenticator con esta clave secreta: {totp_secret}")
    except Exception as e:
        print(f"\n❌ Error creando usuario (quizá {username} ya existe): {e}")

if __name__ == "__main__":
    print("= Instalador de Nuevo Usuario Teamlyx =")
    usr = input("Elige un nombre de usuario (ej. admin): ")
    pwd = input("Elige una contraseña segura: ")
    p2fa = input("¿Estricto con Doble Factor (2FA)? (s/N): ")
    
    usar_2fa = p2fa.lower().startswith('s')
    crear_admin(usr, pwd, enable_2fa=usar_2fa)
