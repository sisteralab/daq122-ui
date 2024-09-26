import ctypes

from api.base_daq122 import DAQ122


class LinDAQ122(DAQ122):
    """
    A class to interface with the DAQ122 data acquisition system iin Linux.
    """

    def _setup_function_prototypes(self):
        # Set up function prototypes according to the actual DLL functions
        self.dll.DAQ122_Create.restype = ctypes.c_void_p

        self.dll.DAQ122_Delete.argtypes = [ctypes.c_void_p]

        self.dll.DAQ122_ConnectedDevice.argtypes = [ctypes.c_void_p]
        self.dll.DAQ122_ConnectedDevice.restype = ctypes.c_bool

        self.dll.DAQ122_UseUSBBackend.argtypes = [ctypes.c_void_p]
        self.dll.DAQ122_UseUSBBackend.restype = ctypes.c_bool

        self.dll.DAQ122_InitializeDevice.argtypes = [ctypes.c_void_p]
        self.dll.DAQ122_InitializeDevice.restype = ctypes.c_bool

        self.dll.DAQ122_ConfigureSamplingParameters.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        self.dll.DAQ122_ConfigureSamplingParameters.restype = ctypes.c_bool

        self.dll.DAQ122_ConfigADCChannel.argtypes = [ctypes.c_void_p, ctypes.c_uint8]
        self.dll.DAQ122_ConfigADCChannel.restype = ctypes.c_bool

        self.dll.DAQ122_StartCollection.argtypes = [ctypes.c_void_p]
        self.dll.DAQ122_StartCollection.restype = ctypes.c_bool

        self.dll.DAQ122_StopCollection.argtypes = [ctypes.c_void_p]
        self.dll.DAQ122_StopCollection.restype = ctypes.c_bool

        self.dll.DAQ122_TryReadData.argtypes = [ctypes.c_void_p, ctypes.c_uint8, ctypes.POINTER(ctypes.c_double),
                                                  ctypes.c_uint32, ctypes.c_uint32]
        self.dll.DAQ122_TryReadData.restype = ctypes.c_bool

        self.dll.DAQ122_ADCDataBufferIsValid.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32]
        self.dll.DAQ122_ADCDataBufferIsValid.restype = ctypes.c_bool
