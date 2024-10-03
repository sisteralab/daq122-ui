class DeviceError(Exception):
    ...


class DeviceCreateError(DeviceError):
    ...


class DeviceInitializeError(DeviceError):
    ...


class DeviceRunTimeError(DeviceError):
    ...


class DeviceReadElementsCountError(DeviceError):
    ...


class DeviceCloseError(DeviceError):
    ...


class DllError(DeviceError):
    ...
