from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QWidget, QMessageBox

from config import Config

class InsertTodoDialog(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__()
        self.parent = parent
        self._content = None
        self.setWindowTitle(Config["dialog"]["insert_todo"]["tite"])
        self.setWindowIcon(QIcon("icons/accessories-text-editor.png"))

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.content_line_edit = QLineEdit(placeholderText=Config["dialog"]["insert_todo"]["placeholder"])
        self.content_line_edit.setFixedWidth(200)
        layout.addWidget(self.content_line_edit, alignment=Qt.AlignHCenter)
        self.dialog_button = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(self.dialog_button, alignment=Qt.AlignHCenter)

        self.dialog_button.accepted.connect(self.on_ok_button_clicked)
        self.dialog_button.rejected.connect(self.reject)

    def on_ok_button_clicked(self):
        self._content = self.content_line_edit.text()

        if len(self._content) >= 5:
            self.accept()
        else:
            self.reject()
            self.parent.issue_warning(
                Config["warning"]["content_too_short"]["title"],
                Config["warning"]["content_too_short"]["text"]
            )

    @property
    def content(self):
        return self._content
