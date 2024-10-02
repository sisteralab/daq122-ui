#if USE_DAQ112M
#pragma once

#include "libdaq/device/base_device.h"
#include "libdaq/device/DAQ112M/daq_112_config.h"

namespace libdaq {
namespace device {
class DAQ112M : public BaseDevice {
 public:
  DAQ112M();
  ~DAQ112M() override;

  bool UseModbusRTUBackend(const std::string &uart_name, int baud_rate, int address) override;

  bool InitializeDevice() override;
  bool ConnectedDevice() override;

  bool ConfigSensorModule(uint8_t channel, DAQThermocoupleModule thermocouple_module);
  bool ConfigTemperatureCompensation(uint8_t channel, double temperature_compensation);

  bool StartADCCollection() override;
  bool StopADCCollection() override;

 protected:
  void ReceiveThreadFunction() override;
};
}
}
#endif
