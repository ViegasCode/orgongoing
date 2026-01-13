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
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Criação da tabela e dados iniciais
def init_db():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS pessoas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        sobrenome TEXT NOT NULL,
        cargo TEXT NOT NULL,
        area TEXT NOT NULL,
        lider_id INTEGER,
        foto TEXT
    )
    """)
    # Inserir dados apenas se tabela estiver vazia
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM pessoas")
    if c.fetchone()[0] == 0:
        pessoas = [
            (1,"Fabio","Moreira","Coordenador","Diretoria",None,None),
            (2,"Douglas","","Líder","Ongoing Tech",1,None),
            (3,"Renan","","Dev","Ongoing Tech",2,None),
            (4,"Jose","","Dev","Ongoing Tech",2,None),
            (5,"Guilherme","","Líder","Observabilidade/Gestão de Incidentes",1,None),
            (6,"Diego","Miranda","Analista de Incidentes","Observabilidade/Gestão de Incidentes",5,None),
            (7,"Ronaldo","","Líder","Ongoing/Cao - Atendimento",1,None),
            (8,"Keny","","Analista","Ongoing/Cao - Atendimento",7,None),
            (9,"Diane","","Analista","Ongoing/Cao - Atendimento",7,None),
            (10,"Ana Paula","","Analista","Ongoing/Cao - Atendimento",7,None),
            (11,"Thiago","","Analista","Ongoing/Cao - Atendimento",7,None),
            (12,"Marcos Vinicius","","Analista","Ongoing/Cao - Atendimento",7,None),
            (13,"Matheus","Avila Paes","Líder","Atendimento Office Suporte",1,None),
            (14,"Marcelo","Ferreira de Abreu","Funcionário","Atendimento Office Suporte",13,None),
            (15,"Henrique","Ferreira Serafim","Funcionário","Atendimento Office Suporte",13,None),
            (16,"Magno","Alexandre Silva de Jesus","Funcionário","Atendimento Office Suporte",13,None),
            (17,"Adail","Pereira da Trindade","Funcionário","Atendimento Office Suporte",13,None),
            (18,"Vagner","Bezerra Oliveira","Terceiro","Atendimento Office Suporte",13,None),
            (19,"Flávio","Caetano","Terceiro","Atendimento Office Suporte",13,None)
        ]
        c.executemany("INSERT INTO pessoas (id,nome,sobrenome,cargo,area,lider_id,foto) VALUES (?,?,?,?,?,?,?)", pessoas)
        conn.commit()
    conn.close()

init_db()

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/api/organograma")
def organograma():
    conn = get_db()
    rows = conn.execute("SELECT * FROM pessoas").fetchall()
    conn.close()
    # converter Row para dict
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
