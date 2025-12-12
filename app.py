from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import init_db, add_task, get_all_tasks, delete_task, toggle_task_status, get_stats

app = Flask(__name__)

init_db()

@app.route('/')
def index():
    tasks = get_all_tasks()
    stats = get_stats()
    return render_template('index.html', tasks=tasks, stats=stats)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form['description']
    due_date = request.form['due_date']
    priority = request.form['priority']
    add_task(title, description, due_date, priority)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    delete_task(task_id)
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    toggle_task_status(task_id)
    return redirect(url_for('index'))

@app.route('/stats')
def stats():
    return jsonify(get_stats())

if __name__ == '__main__':
    app.run(debug=True)
