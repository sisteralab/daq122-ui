import ctypes
import os

from api.base_daq122 import DAQ122
from api.structures import DAQSampleRate, DAQVoltage


class LinDAQ122(DAQ122):
    """
    A class to interface with the DAQ122 data acquisition system iin Linux.
    """

    def _define_dll(self):
        return os.path.join(os.getcwd(), r"daq122.so")

    def _setup_function_prototypes(self):
        # Set up function prototypes according to the actual DLL functions
        self.dll.DAQ122_New.restype = ctypes.c_void_p
        self.dll.DAQ122_Delete.argtypes = [ctypes.c_void_p]

        self.dll.DAQ122_InitializeDevice.argtypes = [ctypes.c_void_p]
        self.dll.DAQ122_InitializeDevice.restype = ctypes.c_bool

        self.dll.DAQ122_ConnectedDevice.argtypes = [ctypes.c_void_p]
        self.dll.DAQ122_ConnectedDevice.restype = ctypes.c_bool

        self.dll.DAQ122_ConfigureSamplingParameters.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int
        ]
        self.dll.DAQ122_ConfigureSamplingParameters.restype = ctypes.c_bool

        self.dll.DAQ122_ConfigADCChannel.argtypes = [ctypes.c_void_p, ctypes.c_uint64]
        self.dll.DAQ122_ConfigADCChannel.restype = ctypes.c_bool

        self.dll.DAQ122_StartCollection.argtypes = [ctypes.c_void_p]
        self.dll.DAQ122_StartCollection.restype = ctypes.c_bool

        self.dll.DAQ122_StopCollection.argtypes = [ctypes.c_void_p]
        self.dll.DAQ122_StopCollection.restype = ctypes.c_bool

        self.dll.DAQ122_TryReadData.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32,  # channel
            ctypes.POINTER(ctypes.c_double),  # data
            ctypes.c_uint32,  # read_size
            ctypes.c_uint32  # timeout
        ]
        self.dll.DAQ122_TryReadData.restype = ctypes.c_bool

    def configure_sampling_parameters(self, voltage: DAQVoltage, sample_rate: DAQSampleRate) -> bool:
        self.sample_rate = sample_rate
        if not self.dll.DAQ122_ConfigureSamplingParameters(self.obj, sample_rate.value, voltage.value):
            raise RuntimeError("Failed to configure sampling parameters.")
        return True
