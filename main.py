from PySide6.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self, title: str, window_size: tuple[int, int]):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(*window_size)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow("Todo App", (600, 400))
    window.show()
    print(f"Exited with status code {app.exec()}")
