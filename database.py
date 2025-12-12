import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT NOT NULL,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_task(title, description, due_date, priority='medium'):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO tasks (title, description, due_date, priority, status, created_at)
        VALUES (?, ?, ?, ?, 'pending', ?)
    ''', (title, description, due_date, priority, created_at))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY priority DESC, due_date ASC')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def toggle_task_status(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM tasks WHERE id = ?', (task_id,))
    current_status = cursor.fetchone()[0]
    new_status = 'completed' if current_status == 'pending' else 'pending'
    cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM tasks')
    total = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "completed"')
    completed = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "pending"')
    pending = cursor.fetchone()[0]
    conn.close()
    return {'total': total, 'completed': completed, 'pending': pending}
