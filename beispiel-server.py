from flask import Flask, jsonify, request, render_template
import uuid

app = Flask(__name__)

todo_lists = {}
@app.route('/')
def index():
# gebe Antwort an aufrufenden Client zurück
    return render_template('index.html')

# Get all todo lists
@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(list(todo_lists.values())), 200

# Add new todo list
@app.route('/todo-list', methods=['POST'])
def add_todo_list():
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    list_id = str(uuid.uuid4())
    todo_lists[list_id] = {'id': list_id, 'name': data['name'], 'entries': []}
    return jsonify(todo_lists[list_id]), 200

# Get a todo list by ID
@app.route('/todo-list/<string:list_id>', methods=['GET'])
def get_todo_list(list_id):
    if list_id in todo_lists:
        return jsonify(todo_lists[list_id]), 200
    return jsonify({'error': 'List not found'}), 404

# Delete a todo list
@app.route('/todo-list/<string:list_id>', methods=['DELETE'])
def delete_todo_list(list_id):
    if list_id in todo_lists:
        del todo_lists[list_id]
        return jsonify({'message': 'List deleted'}), 200
    return jsonify({'error': 'List not found'}), 404

# Get all entries from a todo list
@app.route('/todo-list/<string:list_id>/entries', methods=['GET'])
def get_list_entries(list_id):
    if list_id in todo_lists:
        return jsonify(todo_lists[list_id]['entries']), 200
    return jsonify({'error': 'List not found'}), 404

# Add an entry to a todo list
@app.route('/todo-list/<string:list_id>/entry', methods=['POST'])
def add_entry_to_list(list_id):
    if list_id not in todo_lists:
        return jsonify({'error': 'List not found'}), 404
    data = request.get_json()
    if 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    entry_id = str(uuid.uuid4())
    entry = {'id': entry_id, 'name': data['name'], 'description': data['description'], 'list_id': list_id}
    todo_lists[list_id]['entries'].append(entry)
    return jsonify(entry), 200

# Update a todo list entry
@app.route('/todo-list/<string:list_id>/entry/<string:entry_id>', methods=['PUT'])
def update_entry(list_id, entry_id):
    data = request.get_json()
    if list_id not in todo_lists:
        return jsonify({'error': 'List not found'}), 404
    if 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    for entry in todo_lists[list_id]['entries']:
        if entry['id'] == entry_id:
            entry['name'] = data.get('name', entry['name'])
            entry['description'] = data.get('description', entry['description'])
            return jsonify(entry), 200
    return jsonify({'error': 'Entry not found'}), 404

# Delete a todo list entry
@app.route('/todo-list/<string:list_id>/entry/<string:entry_id>', methods=['DELETE'])
def delete_entry(list_id, entry_id):
    if list_id not in todo_lists:
        return jsonify({'error': 'List not found'}), 404
    for entry in todo_lists[list_id]['entries']:
        if entry['id'] == entry_id:
            todo_lists[list_id]['entries'].remove(entry)
            return jsonify({'message': 'Entry deleted'}), 200
    return jsonify({'error': 'Entry not found'}), 404

if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
