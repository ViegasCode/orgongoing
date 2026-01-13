import sqlite3

# Conecta ao banco
conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

# Cria tabela caso não exista (compatível com seu organograma)
c.execute("""
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
conn.commit()

# Adiciona o líder da nova área
c.execute("""
INSERT INTO pessoas (nome, sobrenome, cargo, area, lider_id)
VALUES (?, ?, ?, ?, ?)
""", ("Pedro Hamilton Cardoso", "Dos Santos", "Líder", "Atendimento CD", 1))  # 1 = Fabio Moreira (Diretoria)

# Pega o ID do líder recém-criado
lider_id = c.lastrowid

# Lista de subordinados
subordinados = [
    ("Adriano", "Da Silva Souza", "Terceiro", "Atendimento CD", lider_id),
    ("Alessandro", "da Silva Garcia", "Funcionário", "Atendimento CD", lider_id),
    ("Guilherme", "De Freitas Alves", "Terceiro", "Atendimento CD", lider_id),
    ("Florisvaldo", "Sebastiao Querino", "Terceiro", "Atendimento CD", lider_id),
    ("Marcelo", "Machado Rogerio", "Terceiro", "Atendimento CD", lider_id),
    ("Helton", "Pereira do Nascimento", "Funcionário", "Atendimento CD", lider_id),
    ("Fabiano", "Jose Cardoso Gomes", "Terceiro", "Atendimento CD", lider_id),
    ("Sidy", "Moreira Da Silva", "Funcionário", "Atendimento CD", lider_id),
    ("Jose Filipe", "Ferreira Lopes", "Terceiro", "Atendimento CD", lider_id),
    ("Jose Henrique", "Medeiros Da Luz", "Funcionário", "Atendimento CD", lider_id),
    ("Samuel", "Carneiro", "Terceiro", "Atendimento CD", lider_id),
    ("Renan", "Cezar Da Silva Luz", "Terceiro", "Atendimento CD", lider_id),
    ("Erivelton", "Coutinho Dos Santos", "Terceiro", "Atendimento CD", lider_id),
    ("Matheus", "Varela De Chaves", "Terceiro", "Atendimento CD", lider_id),
    ("Marcelo Eduardo", "De Souza Soares", "Terceiro", "Atendimento CD", lider_id)
]

# Insere todos os subordinados
c.executemany("""
INSERT INTO pessoas (nome, sobrenome, cargo, area, lider_id)
VALUES (?,?,?,?,?)
""", subordinados)

# Salva alterações e fecha conexão
conn.commit()
conn.close()

print("✅ Área 'Atendimento CD' criada com Pedro como líder e todos os subordinados adicionados!")
