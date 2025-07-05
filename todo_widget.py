from PySide6.QtCore import QSize, Slot
from PySide6.QtGui import QFont, QIcon, QAction, QCursor, QShortcut
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QListView, QMenu, QMessageBox

from config import Config
from database import TodoDB, TodoIn
from dialog import InsertTodoDialog
from todo_model import TodoModel


class TodoWidget(QWidget):
    def __init__(self, db: TodoDB):
        super().__init__()
        self.create_shortcuts()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        font = QFont()
        font.setPointSize(15)

        search_widget = QWidget()
        search_grid = QGridLayout()
        search_widget.setLayout(search_grid)
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search")
        self.searchbar.setFont(font)
        search_grid.addWidget(self.searchbar, 0, 0)
        self.search_button = QPushButton(icon=QIcon("icons/edit-find.png"))
        self.search_button.setIconSize(QSize(28, 28))
        search_grid.addWidget(self.search_button, 0, 1)
        self.layout.addWidget(search_widget)
        self.searchbar.returnPressed.connect(self.search_button.click)
        self.search_button.clicked.connect(self.search)

        self.todo_model = TodoModel(db, self)

        self.list_view = QListView()
        self.list_view.setModel(self.todo_model)
        self.list_view.setFont(font)
        self.layout.addWidget(self.list_view)

    @Slot()
    def search(self):
        # TODO: search functionality
        pass

    @Slot()
    def delete_todo(self):
        if self.list_view.selectionModel().hasSelection():
            index = self.list_view.selectionModel().currentIndex()
            self.todo_model.delete_todo(index)
        else:
            self.issue_warning(
                Config["warning"]["no_selection"]["title"], 
                Config["warning"]["no_selection"]["text"]
            )

    @Slot()
    def create_todo(self):
        pos = QCursor.pos()
        dialog = InsertTodoDialog(self)
        dialog.setGeometry(pos.x(), pos.y(), 200, 100)
        if dialog.exec():
            # Todo: Create todo
            self.todo_model.create_todo(TodoIn(content=dialog.content, completed=0))

    def create_shortcuts(self):
        delete_shortcut = QShortcut(Config["shortcuts"]["delete_todo"], self)
        delete_shortcut.activated.connect(self.delete_todo)

        create_shortcut = QShortcut(Config["shortcuts"]["new_todo"], self)
        create_shortcut.activated.connect(self.create_todo)


    def create_context_menu(self):
        context_menu = QMenu(self)
        font = QFont()
        font.setPointSize(12)
        context_menu.setFont(font)

        create_todo = QAction("New", self, icon=QIcon("icons/document-new.png"))
        create_todo.setShortcut(Config["shortcuts"]["new_todo"])
        create_todo.triggered.connect(self.create_todo)
        context_menu.addAction(create_todo)

        delete_todo = QAction("Delete", self, icon=QIcon("icons/edit-delete.png"))
        delete_todo.setShortcut(Config["shortcuts"]["delete_todo"])
        delete_todo.triggered.connect(self.delete_todo)
        context_menu.addAction(delete_todo)
        return context_menu

    def contextMenuEvent(self, event, /):
        if self.list_view.underMouse():
            context_menu = self.create_context_menu()
            context_menu.popup(self.mapToGlobal(event.pos()))

    def issue_warning(self, title: str, text: str):
        QMessageBox.warning(self.parent(), title, text)
