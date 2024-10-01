from PyQt5 import QtWidgets

from api import get_daq_class
from api.exceptions import DeviceError


class InitializeGroup(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super(InitializeGroup, self).__init__(parent)

        self.setTitle("Device init")

        layout = QtWidgets.QFormLayout()

        self.status = QtWidgets.QLabel("Not initialized", self)
        self.btnInitialize = QtWidgets.QPushButton("Initialize", self)
        self.btnInitialize.clicked.connect(self.initialize)

        layout.addRow("Device:", QtWidgets.QLabel("DAQ122", self))
        layout.addRow("Status:", self.status)
        layout.addRow(self.btnInitialize)

        self.setLayout(layout)

    def initialize(self):
        DAQ122 = get_daq_class()
        try:
            with DAQ122() as daq:
                if daq.is_connected():
                    self.status.setText("Success Connected!")
        except DeviceError as e:
            self.status.setText(str(e))
