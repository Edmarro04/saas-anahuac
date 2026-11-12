from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Se conecta a la base de datos de Supabase usando la variable de entorno
DB_URL = os.getenv("DATABASE_URL")

@app.get("/api/tareas")
def obtener_tareas():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, titulo FROM tareas;")
        tareas = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": t[0], "titulo": t[1]} for t in tareas]
    except Exception as e:
        return {"error": str(e)}

# Sirve la interfaz gráfica
app.mount("/", StaticFiles(directory="public", html=True), name="public")