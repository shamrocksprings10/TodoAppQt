from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from config import Config
from database import TodoDB, TodoIn
from todo_widget import TodoWidget


class MainWindow(QMainWindow):
    def __init__(self, title: str, window_size: tuple[int, int], db: TodoDB):
        super().__init__()
        db.init_table()

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("icons/accessories-text-editor.png"))
        self.setFixedSize(QSize(*window_size))

        self.todo_widget = TodoWidget(db)
        self.setCentralWidget(self.todo_widget)


if __name__ == "__main__":
    app = QApplication([])
    db = TodoDB()
    db.init_table()

    if len(db.get_all_todos()) == 0:
        db.insert_todo(TodoIn(content="Create Some Todos!", completed=0))

    window = MainWindow(Config["gui"]["window_title"], (800, 600), db)
    window.show()
    print(f"Exited with status code {app.exec()}")
