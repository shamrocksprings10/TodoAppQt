from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QWidget, QMessageBox


class InsertTodoDialog(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__()
        self.parent = parent
        self._content = None

        self.setWindowTitle("Create New Todo")
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.content_line_edit = QLineEdit(placeholderText="Content")
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
            self.parent.issue_warning("Content is too short", "Your content must be at least 5 characters long.")

    @property
    def content(self):
        return self._content
