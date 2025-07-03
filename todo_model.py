from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide6.QtWidgets import QMessageBox, QWidget

from database import TodoDB, TodoUpdate

import re, string
from textwrap import shorten as truncate

TODO_CHAR_WIDTH = 60

class TodoModel(QAbstractListModel):
    def __init__(self, db: TodoDB, parent: QWidget):
        super().__init__()
        self.db = db
        self.todos = self.refresh_list()
        self._parent = parent

    def refresh_list(self):
        return self.db.get_all_todos()

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
                QMessageBox.warning(self._parent, "Content too short", "Your input was too short.")
            self.todos = self.refresh_list()
            return True
        elif role == Qt.ItemDataRole.CheckStateRole:
            checked = int(value == 2)
            id_ = self.todos[index.row()].id
            self.db.update_todo(id_, TodoUpdate(completed=checked))
            self.todos = self.refresh_list()
            return True

    def delete_todo(self, index: QModelIndex):
        self.beginRemoveRows(index, index.row(), index.row())
        id_ = self.todos[index.row()].id
        self.db.delete_todo(id_)
        self.todos = self.refresh_list()
        self.endRemoveRows()

    def flags(self, index: QModelIndex):
        return Qt.ItemIsEditable | Qt.ItemIsUserCheckable | super().flags(index)