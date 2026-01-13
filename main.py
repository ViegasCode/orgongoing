from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sqlite3
import os
import shutil

app = FastAPI()

os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

DB_FILE = "database.db"

def get_db():
    return sqlite3.connect(DB_FILE)

# Criar tabela e popular dados
conn = get_db()
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS pessoas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    sobrenome TEXT,
    cargo TEXT NOT NULL,
    area TEXT NOT NULL,
    lider_id INTEGER,
    foto TEXT
)
""")
c.execute("SELECT COUNT(*) FROM pessoas")
if c.fetchone()[0] == 0:
    pessoas = [
        (1,"Fabio","Moreira","Coordenador","Diretoria",None,""),
        (2,"Douglas","","Líder","Ongoing Tech",1,""),
        (3,"Renan","","Dev","Ongoing Tech",2,""),
        (4,"Jose","","Dev","Ongoing Tech",2,""),
        (5,"Guilherme","","Líder","Observabilidade",1,""),
        (6,"Diego","Miranda","Analista de Incidentes","Observabilidade",5,""),
        (7,"Ronaldo","","Líder","Atendimento",1,""),
        (8,"Keny","","Analista","Atendimento",7,""),
        (9,"Diane","","Analista","Atendimento",7,""),
        (10,"Ana Paula","","Analista","Atendimento",7,""),
        (11,"Thiago","","Analista","Atendimento",7,""),
        (12,"Marcos Vinicius","","Analista","Atendimento",7,""),
        (13,"Matheus","Avila Paes","Líder","Office Suporte",1,""),
        (14,"Marcelo","Ferreira de Abreu","Funcionário","Office Suporte",13,""),
        (15,"Henrique","Ferreira Serafim","Funcionário","Office Suporte",13,""),
        (16,"Magno","Alexandre Silva de Jesus","Funcionário","Office Suporte",13,""),
        (17,"Adail","Pereira da Trindade","Funcionário","Office Suporte",13,""),
        (18,"Vagner","Bezerra Oliveira","Terceiro","Office Suporte",13,""),
        (19,"Flávio","Caetano","Terceiro","Office Suporte",13,"")
    ]
    c.executemany("INSERT INTO pessoas (id,nome,sobrenome,cargo,area,lider_id,foto) VALUES (?,?,?,?,?,?,?)", pessoas)
    conn.commit()
conn.close()

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/api/organograma")
def organograma():
    conn = get_db()
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
