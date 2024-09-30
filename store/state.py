from api.structures import DAQSampleRate, DAQVoltage, DAQADCChannel


class State:
    sample_rate: DAQSampleRate = DAQSampleRate.SampleRate500
    voltage: DAQVoltage = DAQVoltage.Voltage5V
    channel: DAQADCChannel = DAQADCChannel.AIN_ALL
    selected_channels: list = []
    is_measuring: bool = False
    plot_window: int = 20
    duration: int = 60
