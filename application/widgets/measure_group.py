import logging
import time
from multiprocessing import Queue
from typing import Dict, List

import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal

from api import get_daq_class
from api.structures import DAQADCChannel
from store.data import MeasureManager
from store.state import State


logger = logging.getLogger(__name__)


class ReceiverThread(QtCore.QThread):
    stop_signal = pyqtSignal()

    def __init__(self, duration: int, data_queue):
        super().__init__()
        self.duration = duration
        self.data_queue = data_queue
        self.read_elements_count = int(State.read_elements_count.value)
        self.sample_rate = State.sample_rate
        self.voltage = State.voltage
        self.selected_channels = sorted([_ for _ in State.selected_channels])

    def run(self) -> None:
        DAQ122 = get_daq_class()
        with DAQ122() as daq:
            if not daq.is_connected():
                self.finish()
                return

            if not daq.configure_sampling_parameters(self.voltage, self.sample_rate):
                self.finish()
                return

            if not daq.config_adc_channel(DAQADCChannel.AIN_ALL):
                self.finish()
                return

            daq.start_collection()
            time.sleep(1)  # Wait for data to accumulate

            start = time.time()
            while State.is_measuring:
                for channel in self.selected_channels:
                    success, data = daq.read_data(
                        read_elements_count=self.read_elements_count,
                        channel_number=channel - 1,
                        timeout=5000
                    )
                    if success:
                        duration = time.time() - start
                        self.data_queue.put({"channel": channel, "voltage": list(data), "time": duration})
                        if duration > self.duration:
                            self.stop_signal.emit()

        self.finish()

    def finish(self):
        self.finished.emit()


class ProcessorThread(QtCore.QThread):
    def __init__(self, data_queue, processed_queue, measure):
        super().__init__()
        self.data_queue = data_queue
        self.processed_queue = processed_queue
        self.is_average = State.is_average
        self.measure = measure

    def run(self):
        while State.is_measuring or State.is_waiting:
            if not self.data_queue.empty():
                data = self.data_queue.get()
                mean_voltage = np.mean(data["voltage"])
                self.processed_queue.put({"channel": data["channel"], "voltage": mean_voltage, "time": data["time"]})
                if self.is_average:
                    self.measure.data["data"][data["channel"]]["voltage"].append(mean_voltage)
                else:
                    self.measure.data["data"][data["channel"]]["voltage"].append(data["voltage"])
                self.measure.data["data"][data["channel"]]["time"].append(data["time"])

        self.finished.emit()


class PlotterThread(QtCore.QThread):
    plot_data = pyqtSignal(list)

    def __init__(self, processed_queue):
        super().__init__()
        self.processed_queue = processed_queue
        self.data = []

    def run(self):
        while State.is_measuring or State.is_waiting:
            if not self.processed_queue.empty():
                self.plot_data.emit([self.processed_queue.get()])

        self.finished.emit()


class MeasureGroup(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.thread_receiver = None
        self.thread_processor = None
        self.thread_plotter = None
        self.data_queue = None
        self.processed_queue = None
        self.measure = None

        self.setTitle("Measure")

        vlayout = QtWidgets.QVBoxLayout()
        hlayout = QtWidgets.QHBoxLayout()
        flayout = QtWidgets.QFormLayout()

        self.duration = QtWidgets.QSpinBox(self)
        self.duration.setRange(10, 3600)
        self.duration.setValue(State.duration)
        self.duration.valueChanged.connect(self.set_duration)

        self.plot_window = QtWidgets.QSpinBox(self)
        self.plot_window.setRange(10, 500)
        self.plot_window.setValue(State.plot_window)
        self.plot_window.valueChanged.connect(self.set_plot_window)

        self.read_elements = QtWidgets.QSpinBox(self)
        self.read_elements.setRange(10, 1000)
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
        flayout.addRow("Plot points count:", self.plot_window)
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

        self.data_queue = Queue()
        self.processed_queue = Queue()

        data = {channel: {"voltage": [], "time": []} for channel in State.selected_channels}
        self.measure = MeasureManager.create(
            data={
                "sample_rate": State.sample_rate.value,
                "voltage": State.voltage.Voltage5V.name,
                "elements_per_request": int(State.read_elements_count.value),
                "data": data,
            }
        )
        self.measure.save(finish=False)

        self.thread_receiver = ReceiverThread(duration=int(self.duration.value()), data_queue=self.data_queue)
        self.thread_receiver.stop_signal.connect(self.stop_measure)
        self.thread_receiver.finished.connect(lambda: self.btn_start.setEnabled(True))

        self.thread_processor = ProcessorThread(data_queue=self.data_queue, processed_queue=self.processed_queue, measure=self.measure)
        self.thread_plotter = PlotterThread(processed_queue=self.processed_queue)
        self.thread_plotter.plot_data.connect(self.plot_data)
        self.thread_plotter.finished.connect(self.finish_measure)

        self.btn_start.setEnabled(False)
        State.is_measuring = True
        self.thread_receiver.start()
        self.thread_processor.start()
        self.thread_plotter.start()

    @staticmethod
    def stop_measure():
        State.is_waiting = True
        State.is_measuring = False
        logger.info("Wait to finish measuring...")

    def finish_measure(self):
        self.thread_receiver = None
        self.thread_processor = None
        self.thread_plotter = None
        self.measure.save(finish=True)
        self.measure = None
        State.is_waiting = False
        State.is_measuring = False
        logger.info("Measure finished!")

    def plot_data(self, data: List[Dict]):
        # self.parent().plot_widget.add_plots(data)
        print({"channel": data[0]['channel'], 'voltage': data[0]['voltage'][0], 'time': data[0]['time']})

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
