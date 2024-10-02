import argparse
import time
import numpy as np
import csv
from api import get_daq_class
from api.exceptions import DeviceError
from api.structures import DAQSampleRate, DAQVoltage, DAQADCChannel


def save_to_csv(filename, data, channels):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        header = ['Time'] + [f'Channel_{ch}' for ch in channels]
        writer.writerow(header)
        # Write data
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='DAQ122 CLI',
        description='Measuring via DAQ122 ADC',
        epilog='LOL'
    )
    parser.add_argument('-s', '--sample-rate', action='store', default=DAQSampleRate.SampleRate500.value, choices=[sr.value for sr in DAQSampleRate], type=int)
    parser.add_argument('-e', '--epr', action='store', default=100, type=int)
    parser.add_argument('-c', '--channel', action='append', choices=list(range(1, 9)), type=int)
    parser.add_argument('-v', '--voltage', action='store', default="Voltage5V", choices=[vt.name for vt in DAQVoltage], type=str)
    parser.add_argument('-a', '--average', action='store_true')
    parser.add_argument('-p', '--plot-window', default=20, type=int)
    parser.add_argument('-d', '--duration', default=60, type=int)
    parser.add_argument('-o', '--output', default='data.csv', type=str, help='Output CSV file')

    args = parser.parse_args()

    voltage = DAQVoltage[args.voltage]
    sample_rate = DAQSampleRate.get_by_value(args.sample_rate)

    data_to_save = []

    DAQ122 = get_daq_class()

    try:
        with DAQ122() as daq:
            if daq.is_connected():
                print("Device is connected")

            if daq.configure_sampling_parameters(voltage, sample_rate):
                print("Sampling parameters configured")

            if daq.config_adc_channel(DAQADCChannel.AIN_ALL):
                daq.start_collection()
                time.sleep(1)

                count = 0
                start = time.time()
                data_to_save = []

                while True:
                    row_data = [time.time() - start]
                    for channel in args.channel:
                        success, data = daq.read_data(read_elements_count=args.epr, channel_number=channel, timeout=5000)
                        if success:
                            read_data = list(data)
                            average_data = np.mean(read_data)
                            row_data.append(average_data)

                            count += 1
                            duration = time.time() - start
                            print(f"\r {duration:5.3f}: {average_data:8.6f}  {count} ", end="")
                            if duration > args.duration:
                                break
                    data_to_save.append(row_data)
                    if duration > args.duration:
                        break

    except (DeviceError, KeyboardInterrupt) as e:
        ...
    finally:
        save_to_csv(args.output, data_to_save, args.channel)
        print(f"\nData saved to {args.output}")
