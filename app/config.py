# Centraliza carga de .env / variables de entorno
from dotenv import load_dotenv
import os
from pathlib import Path

root = Path(__file__).resolve().parents[1]
env_path = root / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()  # fallback al entorno ya cargado

HIK_IP = os.getenv("HIK_IP")
HIK_USER = os.getenv("HIK_USER")
HIK_PAS = os.getenv("HIK_PAS")
HIK_VERIFY = os.getenv("HIK_VERIFY", "false").lower() in ("1", "true", "yes")
DB_DSN = os.getenv("DB_DSN") or (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST','rh-hik-db')}:5432/{os.getenv('POSTGRES_DB')}"
)
BASE_URL = os.getenv("HIK_BASE_URL") or f"http://{HIK_IP}/ISAPI"
