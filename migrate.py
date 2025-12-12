import sqlite3

conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Adiciona as novas colunas se não existirem
try:
    cursor.execute('ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT "medium"')
    print("Coluna 'priority' adicionada")
except sqlite3.OperationalError:
    print("Coluna 'priority' já existe")

try:
    cursor.execute('ALTER TABLE tasks ADD COLUMN status TEXT DEFAULT "pending"')
    print("Coluna 'status' adicionada")
except sqlite3.OperationalError:
    print("Coluna 'status' já existe")

conn.commit()
conn.close()
print("Migração concluída!")
