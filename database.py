import sqlite3
from collections import namedtuple
from typing import Iterable
from pathlib import Path

# Create
CREATE_TABLE = "CREATE TABLE IF NOT EXISTS todo (content TEXT CHECK( LENGTH(content) >= 5 ), completed INTEGER CHECK( completed IN (0,1) ));"
INSERT_TODO = "INSERT INTO todo VALUES (:content, :completed);"
# Read
READ_ALL_TODOS = "SELECT rowid, * FROM todo ORDER BY rowid;"
SEARCH_TODOS = "SELECT rowid, * FROM todo WHERE content LIKE '%'|| ? ||'%' ORDER BY rowid;"
GET_TODO = "SELECT rowid, * FROM todo WHERE rowid = :id"
# Update
UPDATE_TODO_BY_CONTENT = "UPDATE todo SET content = :content WHERE rowid = :id;"
UPDATE_TODO_BY_COMPLETED = "UPDATE todo SET completed = :completed WHERE rowid = :id;"
# Delete
DELETE_ALL_TODOS = "DELETE FROM todo;"
DELETE_TODO = "DELETE FROM todo WHERE rowid = :id"
DROP_TABLE = "DROP TABLE todo;"

Todo = namedtuple("Todo", ("id", "content", "completed"))
TodoIn = namedtuple("TodoIn", ("content", "completed"))
TodoUpdate = namedtuple("TodoUpdate", ("content", "completed"), defaults=(None, None))

def execute(connection: sqlite3.Connection, query: str, args=None, *, commit=False):
    cursor = connection.cursor()
    if args:
        result = cursor.execute(query, args)
    else:
        result = cursor.execute(query)
    if commit:
        connection.commit()
    return result


class TodoDB:
    def __init__(self):
        Path("./todo.db").touch()
        self.connection = sqlite3.connect("./todo.db")

    def init_table(self): execute(self.connection, CREATE_TABLE, commit=True)
    def drop_table(self): execute(self.connection, DROP_TABLE, commit=True)

    # Create
    def insert_todo(self, todo: TodoIn): execute(self.connection, INSERT_TODO, todo._asdict(), commit=True)
    def insert_todos(self, todos: Iterable[TodoIn]): execute(self.connection, INSERT_TODO, todos, commit=True)

    # Read
    def get_todo(self, id_: int) -> Todo: return Todo(*execute(self.connection, GET_TODO, id_).fetchone())
    def get_all_todos(self) -> list[Todo]:
        result = execute(self.connection, READ_ALL_TODOS)
        return [Todo(*row) for row in result]
    def search_todos(self, search: str) -> list[Todo]:
        result = execute(self.connection, SEARCH_TODOS, (search, ))
        return [Todo(*row) for row in result]

    # Update
    def update_todo(self, id_: int, update: TodoUpdate):
        if update.completed is not None:
            execute(self.connection, UPDATE_TODO_BY_COMPLETED, {"id": id_, "completed": update.completed}, commit=True)
        if update.content is not None:
            execute(self.connection, UPDATE_TODO_BY_CONTENT, {"id": id_, "content": update.content}, commit=True)

    # Delete
    def delete_todo(self, id_: int): execute(self.connection, DELETE_TODO, id_, commit=True)
    def delete_all_todos(self): execute(self.connection, DELETE_ALL_TODOS, commit=True)

    def __del__(self):
        self.connection.close()
