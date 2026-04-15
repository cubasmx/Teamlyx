import psycopg2
from psycopg2.pool import SimpleConnectionPool
import contextlib
from app.config import DB_DSN

# Inicializar un pool simple para no saturar la BD
pool = None
try:
    pool = SimpleConnectionPool(1, 20, DB_DSN)
except Exception as e:
    print("Error conectando a la base de datos:", e)

@contextlib.contextmanager
def get_conn():
    if not pool:
        raise Exception("Database pool not initialized")
    conn = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        pool.putconn(conn)
