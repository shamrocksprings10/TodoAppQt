from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon, QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QWidget, QGridLayout, QToolBar, QLineEdit, QLabel, \
    QHBoxLayout, QSizePolicy, QPushButton, QMenu

from database import TodoDB
from todo_model import TodoModel

class MainWindow(QMainWindow):
    def __init__(self, title: str, window_size: tuple[int, int], db: TodoDB):
        super().__init__()
        db.init_table()

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("accessories-text-editor.png"))
        self.setFixedSize(QSize(*window_size))

        self.todo_widget = TodoWidget(db)
        self.setCentralWidget(self.todo_widget)

class TodoWidget(QWidget):
    def __init__(self, db: TodoDB):
        super().__init__()
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        font = QFont()
        font.setPointSize(18)

        search_widget = QWidget()
        hbox = QHBoxLayout()
        search_widget.setLayout(hbox)
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search")
        self.searchbar.setFont(font)
        hbox.addWidget(self.searchbar)
        self.search_button = QPushButton(icon=QIcon("edit-find.png"))
        self.search_button.setIconSize(QSize(32, 32))
        hbox.addWidget(self.search_button)
        self.grid_layout.addWidget(search_widget)

        self.todo_model = TodoModel(db, self)

        self.list_view = QListView()
        self.list_view.setModel(self.todo_model)
        self.list_view.setFont(font)
        self.grid_layout.addWidget(self.list_view)

    def create_actions(self, menu: QMenu):
        create_todo = QAction("New", self, icon=QIcon("document-new.png"))
        create_todo.setShortcut("Ctrl+N")
        menu.addAction(create_todo)

        delete_todo = QAction("Delete", self, icon=QIcon("edit-delete.png"))
        delete_todo.setShortcut("Ctrl+D")
        menu.addAction(delete_todo)

    def contextMenuEvent(self, event, /):
        if self.list_view.underMouse():
            context_menu = QMenu(self)
            self.create_actions(context_menu)
            context_menu.popup(self.mapToGlobal(event.pos()))


if __name__ == "__main__":
    app = QApplication([])
    db = TodoDB()
    window = MainWindow("Todo App", (800, 600), db)
    window.show()
    print(f"Exited with status code {app.exec()}")
