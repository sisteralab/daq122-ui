import logging
import time

import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal

from api import get_daq_class
from api.structures import DAQADCChannel
from store.data import MeasureManager
from store.state import State


logger = logging.getLogger(__name__)


class MeasureThread(QtCore.QThread):
    data_plot = pyqtSignal(list)
    log = pyqtSignal(str)

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
        self.selected_channels = sorted(State.selected_channels)

    def run(self) -> None:
        DAQ122 = get_daq_class()
        with DAQ122() as daq:
            if not daq.is_connected():
                self.finish()
                return
            self.log.emit("Device Connected!")

            if not daq.configure_sampling_parameters(self.voltage, self.sample_rate):
                self.finish()
                return
            self.log.emit("Sampling parameters configured")

            if not daq.config_adc_channel(DAQADCChannel.AIN_ALL):
                self.finish()
                return
            self.log.emit("Channels configured")

            daq.start_collection()
            time.sleep(1)  # Wait for data to accumulate

            start = time.time()
            while State.is_measuring:
                data_plot = []
                time.sleep(self.read_elements_count / self.sample_rate.value)
                for channel in self.selected_channels:
                    success, data = daq.read_data(
                        read_elements_count=self.read_elements_count,
                        channel_number=channel - 1,
                        timeout=5000
                    )
                    if success:
                        duration = time.time() - start
                        mean = np.mean(data)
                        if self.is_average:
                            self.measure.data["data"][channel].append(mean)
                        else:
                            self.measure.data["data"][channel].extend(list(data))

                        data_plot.append({"channel": channel, "voltage": mean, "time": duration})

                        if duration > self.duration:
                            State.is_measuring = False
                if data_plot:
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

        self.is_plot_data = QtWidgets.QCheckBox(self)
        self.is_plot_data.setText("Plot data")
        self.is_plot_data.setToolTip("Plotting might take a lot CPU resources!")
        self.is_plot_data.setChecked(State.is_plot_data)
        self.is_plot_data.stateChanged.connect(self.set_is_plot_data)

        self.plot_window_label = QtWidgets.QLabel("Plot points count:", self)
        self.plot_window_label.setHidden(not State.is_plot_data)

        self.plot_window = QtWidgets.QSpinBox(self)
        self.plot_window.setRange(1, 60)
        self.plot_window.setValue(State.plot_window)
        self.plot_window.valueChanged.connect(self.set_plot_window)
        self.plot_window.setHidden(not State.is_plot_data)

        self.read_elements = QtWidgets.QSpinBox(self)
        self.read_elements.setRange(1, 1000)
        self.read_elements.setValue(State.read_elements_count.value)
        self.read_elements.valueChanged.connect(self.set_read_elements)
        State.read_elements_count.signal_value.connect(lambda val: self.read_elements.setValue(int(val)))

        self.is_average = QtWidgets.QCheckBox(self)
        self.is_average.setText("Average EpR")
        self.is_average.setToolTip("Averaging Elements per Request")
        self.is_average.setChecked(State.is_average)
        self.is_average.stateChanged.connect(self.set_average)

        flayout.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        flayout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        flayout.addRow("Measuring Time, s:", self.duration)
        flayout.addRow("Elements per Request:", self.read_elements)
        flayout.addRow(self.is_average)
        flayout.addRow(self.is_plot_data)
        flayout.addRow(self.plot_window_label, self.plot_window)

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
        self.thread_measure.log.connect(lambda x: logger.info(x))
        self.btn_start.setEnabled(False)
        self.thread_measure.finished.connect(self.finish_measure)
        State.is_measuring = True
        self.thread_measure.start()

    @staticmethod
    def stop_measure():
        State.is_measuring = False

    def finish_measure(self):
        self.btn_start.setEnabled(True)

    def plot_data(self, data: list):
        if self.is_plot_data.isChecked():
            self.parent().plot_widget.add_plots(data)
        self.parent().monitor_widget.add_data(data)

    @staticmethod
    def set_duration(value):
        State.duration = int(value)

    def set_is_plot_data(self, state):
        if state == QtCore.Qt.CheckState.Checked:
            self.plot_window.setHidden(False)
            self.plot_window_label.setHidden(False)
            State.is_plot_data = True
            return
        self.plot_window.setHidden(True)
        self.plot_window_label.setHidden(True)
        State.is_plot_data = False

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
