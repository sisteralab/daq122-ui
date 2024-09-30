from PyQt5 import QtWidgets, QtCore

from store.state import State


class ChannelCheckBox(QtWidgets.QCheckBox):
    def __init__(self, parent, channel: int):
        super().__init__(parent)
        self.channel = channel
        self.setText(f"AI{channel}")
        self.stateChanged.connect(self.set_channel)

    def set_channel(self, state):
        if state == QtCore.Qt.CheckState.Checked:
            State.selected_channels.append(self.channel)
        else:
            State.selected_channels.remove(self.channel)
