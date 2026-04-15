from app.db import get_conn

def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            # Creamos la tabla de usuarios solo si no existe en la BD PostgreSQL actual
            cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                totp_secret VARCHAR(50)
            )
            """)
            
            # Nota: Asumimos que 'hik_events_raw' y 'empleados' ya existen y fueron creados por otro sistema
            # si necesitas que los creemos por si acaso, dímelo.
