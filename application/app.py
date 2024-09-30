from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from application.widgets import PlotWidget
from application.widgets.data_table import DataTable
from application.widgets.config_group import ConfigGroup
from application.widgets.initialize_group import InitializeGroup
from application.widgets.measure_group import MeasureGroup


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        hlayout = QtWidgets.QHBoxLayout()
        left_vlayout = QtWidgets.QVBoxLayout()
        right_vlayout = QtWidgets.QVBoxLayout()

        self.plot_widget = PlotWidget(self)
        left_vlayout.addWidget(self.plot_widget)

        self.initialize_group = InitializeGroup(self)
        right_vlayout.addWidget(self.initialize_group)

        self.config_group = ConfigGroup(self)
        right_vlayout.addWidget(self.config_group)

        self.measure_group = MeasureGroup(self)
        right_vlayout.addWidget(self.measure_group)

        self.data_table = DataTable(self)
        right_vlayout.addWidget(self.data_table)

        hlayout.addLayout(left_vlayout)
        hlayout.addLayout(right_vlayout)

        self.setLayout(hlayout)


class App(QMainWindow):
    def __init__(
        self,
        title: str = "DAQ122",
    ):
        super().__init__()
        self.left = 0
        self.top = 0
        self.width = 1200
        self.height = 700
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(title)
        self.setCentralWidget(MainWidget(self))
        self.show()
