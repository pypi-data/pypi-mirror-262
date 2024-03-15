from flask import Flask, render_template, request, jsonify
from .database import init_db, get_tasks, add_task, delete_task, mark_task_done

app = Flask(__name__)

@app.route('/')
def index():
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add():
    description = request.form['description']
    add_task(description)
    return jsonify({'message': 'Task added successfully'})

@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete(task_id):
    delete_task(task_id)
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/mark_task_done/<int:task_id>', methods=['PUT'])
def mark_done(task_id):
    mark_task_done(task_id)
    return jsonify({'message': 'Task marked as done'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
