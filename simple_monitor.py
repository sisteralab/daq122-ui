import time

import matplotlib.pyplot as plt
import numpy as np

from api.dag122 import DAQVoltage, DAQSampleRate, DAQADCChannel, DAQ122

# Example usage with context management
if __name__ == "__main__":
    with DAQ122(".\libdaq-2.0.0.dll") as mess:
        if mess.is_connected():
            print("Device is connected")

        if mess.configure_sampling_parameters(DAQVoltage.Voltage5V, DAQSampleRate.SampleRate500):
            print("Sampling parameters configured")

        if mess.config_adc_channel(DAQADCChannel.AIN_ALL):
            mess.start_collection()
            time.sleep(0.5)  # Wait for data to accumulate

            count = 0
            start = time.time()
            data_list = np.array([0, 0, 0]).reshape(1, 3)

            plt.ion()

            while True:

                success, data = mess.read_data(read_elements_count=100, channel_number=DAQADCChannel.AIN1.value)
                if success:
                    pressure = list(data)[0]

                    count += 1
                    duration = time.time() - start
                    data_list = np.concatenate((data_list, np.array([duration, pressure, count]).reshape(1,3)), axis=0)
                    print(f"\r {duration:5.3f}: {pressure:8.6f}  {count} ", end="")
                    if count > 2000:
                        break

                    plt.cla()
                    plt.plot(data_list[:, 0], data_list[:, 1])
                    plt.pause(0.001)

            plt.ioff()

    print(data_list)
