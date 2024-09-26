import ctypes
import os

from api.structures import DAQVoltage, DAQSampleRate, DAQADCChannel


class DAQ122:
    """
    A class to interface with the DAQ122 data acquisition system.

    Attributes:
        dll_path (str): The path to the DAQ122 DLL (SO).
    """

    def __init__(self, dll_path: str = None):
        """
        Initializes the DAQ122 device interface.

        Parameters:
            dll_path (str): The path to the DLL file for the DAQ device.
        """
        if dll_path is None:
            dll_path = self._define_dll()
        self.dll = ctypes.CDLL(dll_path)
        self._setup_function_prototypes()
        self.obj = None
        self.sample_rate = None

    def _define_dll(self):
        raise NotImplementedError

    def _setup_function_prototypes(self):
        raise NotImplementedError

    def __enter__(self) -> "DAQ122":
        self.create_device()
        if not self.initialize_device():
            raise Exception("Failed to initialize the DAQ device.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_collection()
        self.delete_device()

    def create_device(self):
        if self.obj is None:
            self.obj = self.dll.DAQ122_New()
        if not self.obj:
            raise Exception("Failed to create DAQ122 object")

    def delete_device(self):
        if self.obj:
            self.dll.DAQ122_Delete(self.obj)
            self.obj = None

    def initialize_device(self) -> bool:
        if not self.dll.DAQ122_InitializeDevice(self.obj):
            raise RuntimeError("Device initialization failed.")
        return True

    def is_connected(self) -> bool:
        if not self.dll.DAQ122_ConnectedDevice(self.obj):
            raise RuntimeError("Device connection failed.")
        return True

    def configure_sampling_parameters(self, voltage: DAQVoltage, sample_rate: DAQSampleRate) -> bool:
        self.sample_rate = sample_rate
        if not self.dll.DAQ122_ConfigureSamplingParameters(self.obj, voltage.value, sample_rate.value):
            raise RuntimeError("Failed to configure sampling parameters.")
        return True

    def config_adc_channel(self, channel: DAQADCChannel) -> bool:
        if not self.dll.DAQ122_ConfigADCChannel(self.obj, channel.value):
            raise RuntimeError("Failed to configure ADC channel.")
        return True

    def start_collection(self):
        if not self.dll.DAQ122_StartCollection(self.obj):
            raise RuntimeError("Failed to start data collection.")

    def stop_collection(self):
        if not self.dll.DAQ122_StopCollection(self.obj):
            raise RuntimeError("Failed to stop data collection.")

    def read_data(self, read_elements_count: int = 100, channel_number: int = 0, timeout: int = 1000):
        if read_elements_count > self.sample_rate.value:
            raise ValueError("read_elements_count must not be greater than sample_rate")
        data_buffer = (ctypes.c_double * self.sample_rate.value)()
        label = self.dll.DAQ122_TryReadData(self.obj, channel_number, data_buffer, read_elements_count, timeout)
        return label, data_buffer
