import ctypes
import os
from enum import IntEnum


class DAQVoltage(IntEnum):
    Voltage5V = 6
    Voltage10V = 7


class DAQSampleRate(IntEnum):
    SampleRate100 = 100
    SampleRate500 = 500
    SampleRate1K = 1000
    SampleRate5K = 5000
    SampleRate10K = 10000
    SampleRate50K = 50000
    SampleRate100K = 100000
    SampleRate200K = 200000


class DAQADCChannel(IntEnum):
    NoChannel = 0b00000000
    AIN1 = 0b00000001
    AIN2 = 0b00000001 << 1
    AIN3 = 0b00000001 << 2
    AIN4 = 0b00000001 << 3
    AIN5 = 0b00000001 << 4
    AIN6 = 0b00000001 << 5
    AIN7 = 0b00000001 << 6
    AIN8 = 0b00000001 << 7
    AIN_ALL = 0b11111111


class DAQ122:
    """
    A class to interface with the DAQ122 data acquisition system.

    Attributes:
        dll_path (str): The path to the DAQ122 DLL.
    """

    def __init__(self, dll_path: str = None):
        """
        Initializes the DAQ122 device interface.

        Parameters:
            dll_path (str): The path to the DLL file for the DAQ device.
        """
        if dll_path is None:
            dll_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], r"libdaq-2.0.0.dll")
        self.dll = ctypes.CDLL(dll_path)
        self._setup_function_prototypes()
        self.obj = None
        self.sample_rate = None

    def _setup_function_prototypes(self):
        # Set up function prototypes according to the actual DLL functions
        self.dll.DAQ122_New.restype = ctypes.POINTER(ctypes.c_uint32)
        self.dll.DAQ122_Delete.argtypes = [ctypes.POINTER(ctypes.c_uint32)]

        self.dll.DAQ122_InitializeDevice.argtypes = [ctypes.POINTER(ctypes.c_uint32)]
        self.dll.DAQ122_InitializeDevice.restype = ctypes.c_bool

        self.dll.DAQ122_ConnectedDevice.argtypes = [ctypes.POINTER(ctypes.c_uint32)]
        self.dll.DAQ122_ConnectedDevice.restype = ctypes.c_bool

        self.dll.DAQ122_ConfigureSamplingParameters.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint64,
                                                                ctypes.c_uint64]
        self.dll.DAQ122_ConfigureSamplingParameters.restype = ctypes.c_bool

        self.dll.DAQ122_ConfigADCChannel.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint64]
        self.dll.DAQ122_ConfigADCChannel.restype = ctypes.c_bool

        self.dll.DAQ122_StartCollection.argtypes = [ctypes.POINTER(ctypes.c_uint32)]
        self.dll.DAQ122_StartCollection.restype = ctypes.c_bool

        self.dll.DAQ122_StopCollection.argtypes = [ctypes.POINTER(ctypes.c_uint32)]
        self.dll.DAQ122_StopCollection.restype = ctypes.c_bool

        self.dll.DAQ122_TryReadData.argtypes = [ctypes.POINTER(ctypes.c_uint32),
                                                ctypes.c_uint32,  # channel
                                                ctypes.POINTER(ctypes.c_double),  # data
                                                ctypes.c_uint32,  # read size
                                                ctypes.c_uint32]  # timeout, 默认值需通过 functools.partial 或者 lambda 实现
        self.dll.DAQ122_TryReadData.restype = ctypes.c_bool

        self.dll.DAQ122_ADCDataBufferIsValid.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32]
        self.dll.DAQ122_ADCDataBufferIsValid.restype = ctypes.c_bool

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
