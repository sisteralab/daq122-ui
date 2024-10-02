from typing import List, Dict

from PyQt5 import QtWidgets, QtCore


class MonitorGroup(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Monitor")

        vlayout = QtWidgets.QVBoxLayout()
        glayout = QtWidgets.QGridLayout()
        hlayout = QtWidgets.QHBoxLayout()

        for i in range(8):
            glayout.addWidget(QtWidgets.QLabel(f"AI{i+1}", self), 0, i)
            ai = QtWidgets.QLabel("", self)
            setattr(self, f"ai{i+1}", ai)
            glayout.addWidget(ai, 1, i)

        self.timer = QtWidgets.QLabel("", self)
        hlayout.addWidget(QtWidgets.QLabel("Timer:"), alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        hlayout.addWidget(self.timer, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        vlayout.addLayout(glayout)
        vlayout.addLayout(hlayout)

        self.setLayout(vlayout)

    def add_data(self, data: List[Dict]):
        for dat in data:
            ai = getattr(self, f"ai{dat['channel']}")
            ai.setText(f"{dat['voltage']:.4f}")

        self.timer.setText(f"{data[0]['time']}")
