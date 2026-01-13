from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sqlite3
import os
import shutil

app = FastAPI()

os.makedirs("static/uploads", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    return sqlite3.connect("db.sqlite")

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/api/organograma")
def organograma():
    conn = get_db()
    conn = sqlite3.connect("database.db", check_same_thread=False)
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS pessoas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cargo TEXT NOT NULL,
        setor TEXT NOT NULL,
        lider TEXT NOT NULL
    )
    """)
    
    conn.commit()

    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM pessoas").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/upload/{pessoa_id}")
def upload(pessoa_id: int, file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1]
    filename = f"{pessoa_id}.{ext}"
    path = f"static/uploads/{filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    conn = get_db()
    conn.execute("UPDATE pessoas SET foto=? WHERE id=?", (filename, pessoa_id))
    conn.commit()
    conn.close()

    return {"status": "ok", "foto": filename}
