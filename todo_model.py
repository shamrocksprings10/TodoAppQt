from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt

import re, string
from textwrap import shorten as truncate

from config import Config
from database import TodoDB, TodoUpdate, TodoIn
from dialog import CanIssueWarning

TODO_CHAR_WIDTH = 60

class TodoModel(QAbstractListModel):
    def __init__(self, db: TodoDB, parent: CanIssueWarning):
        super().__init__()
        self.search_string = ""
        self.db = db
        self.refresh_list()
        self._parent = parent

    def refresh_list(self):
        self.todos = self.db.search_todos(search=self.search_string)
        self.dataChanged.emit(QModelIndex(), QModelIndex(), self.todos)

    def rowCount(self, parent=None):
        return len(self.todos)

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            content = self.todos[index.row()].content
            content = re.sub(f"[{string.whitespace}]]", " ", content)
            return truncate(content, TODO_CHAR_WIDTH, placeholder="...")
        elif role == Qt.ItemDataRole.CheckStateRole:
            return int(self.todos[index.row()].completed) * 2
        return None

    def setData(self, index: QModelIndex, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole:
            id_ = self.todos[index.row()].id
            if len(value) >= 5:
                self.db.update_todo(id_, TodoUpdate(content=value))
            else:
                self._parent.issue_warning(
                    Config["warning"]["content_too_short"]["title"],
                    Config["warning"]["content_too_short"]["text"]
                )
            self.refresh_list()
            self.dataChanged.emit(index, index)
            return True
        elif role == Qt.ItemDataRole.CheckStateRole:
            checked = int(value == 2)
            id_ = self.todos[index.row()].id
            self.db.update_todo(id_, TodoUpdate(completed=checked))
            self.refresh_list()
            self.dataChanged.emit(index, index)
            return True

    def delete_todo(self, index: QModelIndex):
        id_ = self.todos[index.row()].id
        self.db.delete_todo(id_)
        self.refresh_list()
        self.removeRow(index.row())
        self.dataChanged.emit(index, index)

    def create_todo(self, todo: TodoIn):
        self.db.insert_todo(todo)
        self.refresh_list()
        index = self.index(len(self.todos) - 1, 0)
        self.dataChanged.emit(index, index)

    def flags(self, index: QModelIndex):
        return Qt.ItemIsEditable | Qt.ItemIsUserCheckable | super().flags(index)