from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from database import TodoDB
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
    window = MainWindow("Todo App", (800, 600), db)
    window.show()
    print(f"Exited with status code {app.exec()}")
