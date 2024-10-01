import time

import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal

from api import get_daq_class
from api.structures import DAQADCChannel
from store.data import MeasureManager
from store.state import State


class MeasureThread(QtCore.QThread):
    data_plot = pyqtSignal(list)

    def __init__(self, parent, duration: int):
        super().__init__(parent)
        self.duration = duration
        self.measure = MeasureManager.create(
            data={
                "sample_rate": State.sample_rate.value,
                "voltage": State.voltage.Voltage5V.name,
                "data": {channel: [] for channel in State.selected_channels},
            }
        )
        self.measure.save(finish=False)
        self.read_elements_count = State.read_elements_count.value
        self.sample_rate = State.sample_rate
        self.voltage = State.voltage
        self.is_average = State.is_average

    def run(self) -> None:
        DAQ122 = get_daq_class()
        with DAQ122() as daq:
            if not daq.is_connected():
                self.finish()
                return
            print("Device Connected!")

            if not daq.configure_sampling_parameters(self.voltage, self.sample_rate):
                self.finish()
                return
            print("Sampling parameters configured")

            if not daq.config_adc_channel(DAQADCChannel.AIN_ALL):
                self.finish()
                return
            print("Channels configured")

            daq.start_collection()
            time.sleep(1)  # Wait for data to accumulate

            start = time.time()
            while State.is_measuring:
                data_plot = []
                for channel in State.selected_channels:
                    success, data = daq.read_data(
                        read_elements_count=self.read_elements_count,
                        channel_number=channel - 1,
                        timeout=5000
                    )
                    if success:
                        duration = time.time() - start
                        read_data = np.array(data)
                        mean = np.mean(read_data)
                        if self.is_average:
                            self.measure.data["data"][channel].append(mean)
                        else:
                            self.measure.data["data"][channel].extend(read_data)
                        data_plot.append({"channel": channel, "voltage": mean, "time": duration})

                        del data, read_data

                        if duration > self.duration:
                            break
                if not data_plot:
                    continue
                self.data_plot.emit(data_plot)

        self.finish()

    def finish(self):
        self.measure.save(finish=True)
        self.finished.emit()


class MeasureGroup(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.thread_measure = None
        self.setTitle("Measure")

        vlayout = QtWidgets.QVBoxLayout()
        hlayout = QtWidgets.QHBoxLayout()
        flayout = QtWidgets.QFormLayout()

        self.duration = QtWidgets.QSpinBox(self)
        self.duration.setRange(1, 3600)
        self.duration.setValue(State.duration)
        self.duration.valueChanged.connect(self.set_duration)

        self.plot_window = QtWidgets.QSpinBox(self)
        self.plot_window.setRange(1, 60)
        self.plot_window.setValue(State.plot_window)
        self.plot_window.valueChanged.connect(self.set_plot_window)

        self.read_elements = QtWidgets.QSpinBox(self)
        self.read_elements.setRange(1, 1000)
        self.read_elements.setValue(State.read_elements_count.value)
        self.read_elements.valueChanged.connect(self.set_read_elements)
        State.read_elements_count.signal_value.connect(lambda val: self.read_elements.setValue(int(val)))

        self.is_average = QtWidgets.QCheckBox(self)
        self.is_average.setText("Average EpR")
        self.is_average.setToolTip("Averaging Elements per Request")
        self.is_average.stateChanged.connect(self.set_average)

        flayout.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        flayout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        flayout.addRow("Time, s:", self.duration)
        flayout.addRow("Plot Window, s:", self.plot_window)
        flayout.addRow("Elements per Request:", self.read_elements)
        flayout.addRow(self.is_average)

        self.btn_start = QtWidgets.QPushButton("Start", self)
        self.btn_start.clicked.connect(self.start_measure)
        self.btn_stop = QtWidgets.QPushButton("Stop", self)
        self.btn_stop.clicked.connect(self.stop_measure)
        hlayout.addWidget(self.btn_start)
        hlayout.addWidget(self.btn_stop)

        vlayout.addLayout(flayout)
        vlayout.addLayout(hlayout)

        self.setLayout(vlayout)

    def start_measure(self):
        if not len(State.selected_channels):
            return
        self.parent().plot_widget.clear()
        self.thread_measure = MeasureThread(self, int(self.duration.value()))
        self.thread_measure.data_plot.connect(self.plot_data)
        self.btn_start.setEnabled(False)
        self.thread_measure.finished.connect(lambda: self.btn_start.setEnabled(True))
        State.is_measuring = True
        self.thread_measure.start()

    @staticmethod
    def stop_measure():
        State.is_measuring = False

    def plot_data(self, data: list):
        self.parent().plot_widget.add_plots(data)

    @staticmethod
    def set_duration(value):
        State.duration = int(value)

    @staticmethod
    def set_plot_window(value):
        State.plot_window = int(value)

    @staticmethod
    def set_read_elements(value):
        State.read_elements_count.value = int(value)

    @staticmethod
    def set_average(state):
        value = state == QtCore.Qt.CheckState.Checked
        State.is_average = value
