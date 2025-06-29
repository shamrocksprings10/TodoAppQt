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
# Update
UPDATE_TODO = "UPDATE todo SET content = :content, completed = :completed WHERE rowid = :rowid;"
# Delete
DELETE_ALL_TODOS = "DELETE FROM todo;"
DELETE_TODOS = "DELETE FROM todo WHERE content LIKE '%'|| ? ||'%';"
DROP_TABLE = "DROP TABLE todo;"

Todo = namedtuple("Todo", ("id", "content", "completed"))
TodoIn = namedtuple("TodoIn", ("content", "completed"))

class TodoDB:
    def __init__(self):
        Path("./todo.db").touch()
        self.connection = sqlite3.connect("./todo.db")

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute(CREATE_TABLE)
        self.connection.commit()

    def drop_table(self):
        cursor = self.connection.cursor()
        cursor.execute(DROP_TABLE)
        self.connection.commit()

    def insert_todo(self, todo: TodoIn):
        cursor = self.connection.cursor()
        cursor.execute(INSERT_TODO, todo._asdict())
        self.connection.commit()

    def insert_todos(self, todos: Iterable[TodoIn]):
        cursor = self.connection.cursor()
        cursor.executemany(INSERT_TODO, todos)
        self.connection.commit()

    def read_all_todos(self) -> list[Todo]:
        cursor = self.connection.cursor()
        result = cursor.execute(READ_ALL_TODOS)
        return [Todo(*row) for row in result]

    def search_todos(self, search: str) -> list[Todo]:
        cursor = self.connection.cursor()
        result = cursor.execute(SEARCH_TODOS, (search, ))
        return [Todo(*row) for row in result]

    def delete_todos(self, stem: str):
        cursor = self.connection.cursor()
        cursor.execute(DELETE_TODOS, (stem, ))
        self.connection.commit()

    def delete_all_todos(self):
        cursor = self.connection.cursor()
        cursor.execute(DELETE_ALL_TODOS)
        cursor.close()

    def __del__(self):
        self.connection.close()

if __name__ == "__main__":
    db = TodoDB()
    db.init_table()
