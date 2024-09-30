import time

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
                "data": {},
            }
        )
        self.measure.save(finish=False)

    def run(self) -> None:
        DAQ122 = get_daq_class()
        with DAQ122() as daq:
            if not daq.is_connected():
                self.finish()
                return
            print("Device Connected!")

            if not daq.configure_sampling_parameters(State.voltage, State.sample_rate):
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
                    success, data = daq.read_data(read_elements_count=State.sample_rate.value, channel_number=channel-1, timeout=5000)
                    if success:
                        duration = time.time() - start
                        read_data = list(data)
                        channel_data = {
                            "channel": f"AIN{channel}",
                            "voltage": list(data),
                            "time": duration,
                        }
                        self.measure.data["data"]["channel"] = channel_data
                        data_plot.append({"channel": channel, "voltage": read_data[0], "time": duration})

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

        flayout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        flayout.addRow("Time, s:", self.duration)
        flayout.addRow("Plot Window, s:", self.plot_window)

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

        self.thread_measure = MeasureThread(self, int(self.duration.value()))
        self.thread_measure.data_plot.connect(self.plot_data)
        self.btn_start.setEnabled(False)
        self.thread_measure.finished.connect(lambda: self.btn_start.setEnabled(True))

    @staticmethod
    def stop_measure():
        State.is_measuring = False

    def plot_data(self, data: list):
        self.parent().parent().plot_widget.add_plots(data)

    @staticmethod
    def set_duration(value):
        State.duration = int(value)

    @staticmethod
    def set_plot_window(value):
        State.plot_window = int(value)
