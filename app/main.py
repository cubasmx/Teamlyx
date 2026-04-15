from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.hik.client import request_get
from app.syncer import run_sync
from app.db import get_conn
from app.db_init import init_db  # mantén db_init.py si prefieres
from app.config import HIK_IP
from app.auth import LoginRequest, verify_password, verify_totp, create_access_token

app = FastAPI(title="RH Hikvision Middleware", version="0.1")

# Habilitar CORS para que el Frontend (Panel de Control) pueda enviar peticiones
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/login")
def login(req: LoginRequest):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, password_hash, totp_secret FROM usuarios WHERE username = %s", (req.username,))
            user = cur.fetchone()
            
    if not user:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
        
    usr_id, usr_name, passwd_hash, totp_sec = user
    
    if not verify_password(req.password, passwd_hash):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
        
    if totp_sec:
        if not req.totp_code or not verify_totp(totp_sec, req.totp_code):
            raise HTTPException(status_code=401, detail="Código 2FA incorrecto o faltante")
            
    token = create_access_token({"sub": usr_name})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/hikvision/isup")
async def hik_isup(request: Request):
    body = await request.body()
    print("Raw body:", body)
    return {"status": "ok"}

@app.on_event("startup")
def startup():
    init_db()
    
@app.get("/health")
def health():
    return {"ok": True}

@app.get("/hik/deviceinfo")
def deviceinfo():
    r = request_get(f"http://{HIK_IP}/ISAPI/System/deviceInfo")
    return {"status_code": r.status_code, "text": r.text}

@app.post("/sync/hikvision")
def sync_hikvision():
    return run_sync()

@app.get("/attendance")
def attendance(from_ts: str, to_ts: str, employee_no: str | None = None):
    # Esta vista devuelve RAW. Luego la normalizas a “entradas/salidas”.
    q = """
      SELECT event_ts, employee_no, event_type, payload
      FROM hik_events_raw
      WHERE event_ts BETWEEN %s AND %s
    """
    params = [from_ts, to_ts]
    if employee_no:
        q += " AND employee_no = %s"
        params.append(employee_no)
    q += " ORDER BY event_ts ASC LIMIT 5000"

    with get_conn() as c:
        with c.cursor() as cur:
            cur.execute(q, params)
            rows = cur.fetchall()
    return [{"event_ts": r[0], "employee_no": r[1], "event_type": r[2], "payload": r[3]} for r in rows]

@app.get("/empleados")
def listar_empleados():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM empleados")
            rows = cur.fetchall()
            return rows