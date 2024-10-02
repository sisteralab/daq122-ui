from enum import IntEnum


class EnumMixin:
    @classmethod
    def get_by_index(cls, index: int):
        return list(cls)[index]

    @classmethod
    def get_by_value(cls, value):
        for name, member in cls.__members__.items():
            if member.value == value:
                return member
        return None


class DAQVoltage(EnumMixin, IntEnum):
    Voltage5V = 6
    Voltage10V = 7


class DAQSampleRate(EnumMixin, IntEnum):
    SampleRate100 = 100
    SampleRate500 = 500
    SampleRate1K = 1000
    SampleRate5K = 5000
    SampleRate10K = 10000
    SampleRate50K = 50000
    SampleRate100K = 100000
    SampleRate200K = 200000


class DAQADCChannel(EnumMixin, IntEnum):
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