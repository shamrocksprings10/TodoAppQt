from PySide6.QtCore import QSize, Slot
from PySide6.QtGui import QAction, QIcon, QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QWidget, QGridLayout, QLineEdit, QPushButton, QMenu, \
    QMessageBox

from database import TodoDB
from todo_model import TodoModel


class MainWindow(QMainWindow):
    def __init__(self, title: str, window_size: tuple[int, int], db: TodoDB):
        super().__init__()
        db.init_table()

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("icons/accessories-text-editor.png"))
        self.setFixedSize(QSize(*window_size))

        self.todo_widget = TodoWidget(db)
        self.setCentralWidget(self.todo_widget)

class TodoWidget(QWidget):
    def __init__(self, db: TodoDB):
        super().__init__()
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

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
        self.grid_layout.addWidget(search_widget)
        self.searchbar.returnPressed.connect(self.search_button.click)
        self.search_button.clicked.connect(self.search)

        self.todo_model = TodoModel(db, self)

        self.list_view = QListView()
        self.list_view.setModel(self.todo_model)
        self.list_view.setFont(font)
        self.grid_layout.addWidget(self.list_view)

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
            pass # TODO: issue warning

    def create_context_menu(self):
        context_menu = QMenu(self)
        font = QFont()
        font.setPointSize(12)
        context_menu.setFont(font)

        create_todo = QAction("New", self, icon=QIcon("icons/document-new.png"))
        create_todo.setShortcut("Ctrl+N")
        context_menu.addAction(create_todo)

        delete_todo = QAction("Delete", self, icon=QIcon("icons/edit-delete.png"))
        delete_todo.triggered.connect(self.delete_todo)
        delete_todo.setShortcut("Ctrl+D")
        context_menu.addAction(delete_todo)
        return context_menu

    def contextMenuEvent(self, event, /):
        if self.list_view.underMouse():
            context_menu = self.create_context_menu()
            context_menu.popup(self.mapToGlobal(event.pos()))

    def issue_warning(self, title: str, text: str):
        QMessageBox.warning(self, title, text)


if __name__ == "__main__":
    app = QApplication([])
    db = TodoDB()
    window = MainWindow("Todo App", (800, 600), db)
    window.show()
    print(f"Exited with status code {app.exec()}")
