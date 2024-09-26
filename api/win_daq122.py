import ctypes

from api.base_daq122 import DAQ122


class WinDAQ122(DAQ122):
    """
    A class to interface with the DAQ122 data acquisition system in Windows.
    """

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
                                                ctypes.c_uint32]  # timeout
        self.dll.DAQ122_TryReadData.restype = ctypes.c_bool

        self.dll.DAQ122_ADCDataBufferIsValid.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32]
        self.dll.DAQ122_ADCDataBufferIsValid.restype = ctypes.c_bool
