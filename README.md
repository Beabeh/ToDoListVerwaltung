# Todo List Management API

## Description
This is a simple RESTful API for managing Todo lists and their entries using Flask. The API allows users to create, retrieve, update, and delete todo lists and their items.

## Features
- Create and manage multiple todo lists.
- Add, update, and delete entries in todo lists.
- Retrieve all todo lists or a specific one.
- Retrieve all entries from a specific list.

## Installation
### Prerequisites
- Python 3.7+
- Flask

### Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/todo-list-api.git
   cd todo-list-api
   ```
2. Install dependencies:
   ```sh
   pip install flask
   ```
3. Run the application:
   ```sh
   python flasktest.py
   ```
4. The API will be available at `http://127.0.0.1:5000/`

## API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/todo-lists` | Get all todo lists |
| POST | `/todo-list` | Create a new todo list |
| GET | `/todo-list/{list_id}` | Get a specific todo list by ID |
| DELETE | `/todo-list/{list_id}` | Delete a specific todo list with all its entries |
| GET | `/todo-list/{list_id}/entries` | Get all entries in a list |
| POST | `/todo-list/{list_id}/entry` | Add an entry to a list |
| PUT | `/todo-list/{list_id}/entry/{entry_id}` | Update an entry in a list |
| DELETE | `/todo-list/{list_id}/entry/{entry_id}` | Delete an entry from a list |

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

# MIT License

```
MIT License

Copyright (c) 2024 Bahareh Janott

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
