from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QWidget, QGridLayout

from database import TodoDB
from todo_model import TodoModel

class MainWindow(QMainWindow):
    def __init__(self, title: str, window_size: tuple[int, int], db: TodoDB):
        super().__init__()
        db.init_table()

        self.setWindowTitle(title)
        self.setMinimumSize(*window_size)

        self.todo_widget = TodoWidget(db)
        self.setCentralWidget(self.todo_widget)

class TodoWidget(QWidget):
    def __init__(self, db: TodoDB):
        super().__init__()
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.todo_model = TodoModel(db, self)
        self.list_view = QListView()
        self.list_view.setModel(self.todo_model)
        self.grid_layout.addWidget(self.list_view)


if __name__ == "__main__":
    app = QApplication([])
    db = TodoDB()
    window = MainWindow("Todo App", (600, 400), db)
    window.show()
    print(f"Exited with status code {app.exec()}")
