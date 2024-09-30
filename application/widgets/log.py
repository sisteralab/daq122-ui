from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy


class LogWidget(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Log")

        layout = QtWidgets.QHBoxLayout()
        self.content = QtWidgets.QLabel("--", self)
        self.content.setWordWrap(True)
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout.addWidget(self.content)
        self.setLayout(layout)

    def set_log(self, text: str):
        log = f"[{datetime.today().strftime('%H:%M:%S')}]{text}"
        self.content.setText(log)


class LogWriter:
    def __init__(self, log_widget):
        self.log_widget = log_widget

    def write(self, message):
        if message.strip():
            self.log_widget.set_log(message.strip())

    def flush(self):
        pass
