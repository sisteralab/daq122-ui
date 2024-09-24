import json
import time

import matplotlib.pyplot as plt
import numpy as np

from api.dag122 import DAQVoltage, DAQSampleRate, DAQADCChannel, DAQ122

# Example usage with context management
if __name__ == "__main__":
    full_data = []
    try:
        with DAQ122(".\libdaq-2.0.0.dll") as mess:
            if mess.is_connected():
                print("Device is connected")

            if mess.configure_sampling_parameters(DAQVoltage.Voltage5V, DAQSampleRate.SampleRate100K):
                print("Sampling parameters configured")

            if mess.config_adc_channel(DAQADCChannel.AIN_ALL):
                mess.start_collection()
                time.sleep(1)  # Wait for data to accumulate

                count = 0
                start = time.time()
                data_list = np.array([0, 0, 0]).reshape(1, 3)

                plt.ion()

                while True:

                    success, data = mess.read_data(read_elements_count=100000, channel_number=0, timeout=5000)
                    if success:
                        read_data = np.array(data)
                        pressure = read_data[0]
                        full_data.extend(read_data)
                        # full_data.extend([_ for _ in read_data if _])

                        count += 1
                        duration = time.time() - start
                        print(f"\r {duration:5.3f}: {pressure:8.6f}  {count} ", end="")
                        if duration > 360:
                            break

                plt.ioff()
    except (Exception, KeyboardInterrupt) as e:
        print(f"Exception: {e}")
        plt.ioff()

    with open("meas_stab_10k.json", 'w') as f:
        json.dump(full_data, f, indent=4)
