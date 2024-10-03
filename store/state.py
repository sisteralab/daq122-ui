from typing import List

from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty

from api.structures import DAQSampleRate, DAQVoltage, DAQADCChannel


class ReadElementsCountModel(QObject):
    signal_value = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 100

    @pyqtProperty("int", notify=signal_value)
    def value(self):
        return self._value

    @value.setter
    def value(self, value: int):
        if value > State.sample_rate:
            value = State.sample_rate
        self._value = value
        self.signal_value.emit(value)


class State:
    sample_rate: DAQSampleRate = DAQSampleRate.SampleRate500
    voltage: DAQVoltage = DAQVoltage.Voltage5V
    channel: DAQADCChannel = DAQADCChannel.AIN_ALL
    selected_channels: List[int] = []
    is_measuring: bool = False
    plot_window: int = 20
    duration: int = 60
    read_elements_count = ReadElementsCountModel()
    is_average: bool = True
    is_plot_data: bool = False
    store_data: bool = True
