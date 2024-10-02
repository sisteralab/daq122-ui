import ctypes
import logging

from api.exceptions import (
    DeviceInitializeError,
    DeviceCloseError,
    DeviceCreateError,
    DeviceRunTimeError,
    DeviceReadElementsCountError,
)
from api.structures import DAQVoltage, DAQSampleRate, DAQADCChannel

logger = logging.getLogger(__name__)


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
        self.initialize_device()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.stop_collection()
            self.delete_device()
            del self
        except (OSError, WindowsError) as e:
            raise DeviceCloseError(str(e))

    def create_device(self):
        if self.obj is None:
            try:
                self.obj = self.dll.DAQ122_New()
            except (OSError, WindowsError):
                logger.debug("Failed to create DAQ122 object")
                raise DeviceCreateError("Failed to create DAQ122 object")
        if not self.obj:
            logger.debug("Failed to create DAQ122 object")
            raise DeviceCreateError("Failed to create DAQ122 object")
        logger.debug("Device created")

    def delete_device(self):
        if self.obj:
            self.dll.DAQ122_Delete(self.obj)
            self.obj = None
            logger.debug("Device deleted")

    def initialize_device(self) -> bool:
        if not self.dll.DAQ122_InitializeDevice(self.obj):
            logger.debug("Failed to initialize the DAQ device.")
            raise DeviceInitializeError("Failed to initialize the DAQ device.")
        logger.debug("Device initialized")
        return True

    def is_connected(self) -> bool:
        if not self.dll.DAQ122_ConnectedDevice(self.obj):
            logger.debug("Device connection failed.")
            raise DeviceRunTimeError("Device connection failed.")
        logger.debug("Device state: connected")
        return True

    def configure_sampling_parameters(self, voltage: DAQVoltage, sample_rate: DAQSampleRate) -> bool:
        self.sample_rate = sample_rate
        if not self.dll.DAQ122_ConfigureSamplingParameters(self.obj, voltage.value, sample_rate.value):
            logger.debug("Failed to configure sampling parameters.")
            raise DeviceRunTimeError("Failed to configure sampling parameters.")
        logger.debug("Sampling parameters configured")
        return True

    def config_adc_channel(self, channel: DAQADCChannel) -> bool:
        if not self.dll.DAQ122_ConfigADCChannel(self.obj, channel.value):
            logger.debug("Failed to configure ADC channel.")
            raise DeviceRunTimeError("Failed to configure ADC channel.")
        logger.debug("ADC channels configured")
        return True

    def start_collection(self):
        if not self.dll.DAQ122_StartCollection(self.obj):
            logger.debug("Failed to start data collection.")
            raise DeviceRunTimeError("Failed to start data collection.")
        logger.debug("Start collection")

    def stop_collection(self):
        if not self.dll.DAQ122_StopCollection(self.obj):
            logger.debug("Failed to stop data collection.")
            raise DeviceRunTimeError("Failed to stop data collection.")
        logger.debug("Stop collection")

    def read_data(self, read_elements_count: int = 100, channel_number: int = 0, timeout: int = 1000):
        if read_elements_count > self.sample_rate.value:
            logger.debug("read_elements_count must not be greater than sample_rate")
            raise DeviceReadElementsCountError("read_elements_count must not be greater than sample_rate")
        data_buffer = (ctypes.c_double * self.sample_rate.value)()
        label = self.dll.DAQ122_TryReadData(self.obj, channel_number, data_buffer, read_elements_count, timeout)
        return label, data_buffer
