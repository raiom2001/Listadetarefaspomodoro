import psycopg2
from psycopg2 import pool
from datetime import datetime
import os

# Connection pool para reutilizar conexões
connection_pool = None

def get_pool():
    global connection_pool
    if connection_pool is None:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 10,
            os.environ.get('POSTGRES_URL')
        )
    return connection_pool

def get_connection():
    pool = get_pool()
    return pool.getconn()

def release_connection(conn):
    pool = get_pool()
    pool.putconn(conn)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT NOT NULL,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    release_connection(conn)

def add_task(title, description, due_date, priority='medium'):
    conn = get_connection()
    cursor = conn.cursor()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO tasks (title, description, due_date, priority, status, created_at)
        VALUES (%s, %s, %s, %s, 'pending', %s)
    ''', (title, description, due_date, priority, created_at))
    conn.commit()
    cursor.close()
    release_connection(conn)

def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY priority DESC, due_date ASC')
    tasks = cursor.fetchall()
    cursor.close()
    release_connection(conn)
    return tasks

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    conn.commit()
    cursor.close()
    release_connection(conn)

def toggle_task_status(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM tasks WHERE id = %s', (task_id,))
    current_status = cursor.fetchone()[0]
    new_status = 'completed' if current_status == 'pending' else 'pending'
    cursor.execute('UPDATE tasks SET status = %s WHERE id = %s', (new_status, task_id))
    conn.commit()
    cursor.close()
    release_connection(conn)

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM tasks')
    total = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = %s', ('completed',))
    completed = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = %s', ('pending',))
    pending = cursor.fetchone()[0]
    cursor.close()
    release_connection(conn)
    return {'total': total, 'completed': completed, 'pending': pending}
