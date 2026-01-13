from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sqlite3
import os

app = FastAPI()

# Pastas
os.makedirs("static/uploads", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    return sqlite3.connect("db.sqlite")

# Criar banco e popular
conn = get_db()
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS pessoas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    sobrenome TEXT,
    cargo TEXT,
    area TEXT,
    lider_id INTEGER,
    foto TEXT
)
""")

# Limpa e insere
c.execute("DELETE FROM pessoas")

pessoas = [
    ("Fabio","Moreira","Coordenador","Diretoria",None,""),
    ("Douglas","","Líder","Ongoing Tech",1,""),
    ("Renan","","Dev","Ongoing Tech",2,""),
    ("Jose","","Dev","Ongoing Tech",2,""),
    ("Guilherme","","Líder","Observabilidade",1,""),
    ("Diego","Miranda","Analista de Incidentes","Observabilidade",5,""),
    ("Ronaldo","","Líder","Atendimento",1,""),
    ("Keny","","Analista","Atendimento",7,""),
    ("Diane","","Analista","Atendimento",7,""),
    ("Ana Paula","","Analista","Atendimento",7,""),
    ("Thiago","","Analista","Atendimento",7,""),
    ("Marcos Vinicius","","Analista","Atendimento",7,""),
    ("Matheus","Avila Paes","Líder","Office Suporte",1,""),
    ("Marcelo","Ferreira de Abreu","Funcionário","Office Suporte",13,""),
    ("Henrique","Ferreira Serafim","Funcionário","Office Suporte",13,""),
    ("Magno","Alexandre Silva de Jesus","Funcionário","Office Suporte",13,""),
    ("Adail","Pereira da Trindade","Funcionário","Office Suporte",13,""),
    ("Vagner","Bezerra Oliveira","Terceiro","Office Suporte",13,""),
    ("Flávio","Caetano","Terceiro","Office Suporte",13,""),
]

c.executemany("INSERT INTO pessoas (nome,sobrenome,cargo,area,lider_id,foto) VALUES (?,?,?,?,?,?)", pessoas)
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
