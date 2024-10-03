#pragma once
#include "libdaq/backend/base_backend.h"
#include "libdaq/backend/base_backend_option.h"

#include <modbus.h>

namespace libdaq {
namespace backend {
class ModbusRTUBackend : public BaseBackend {
 public:
  ModbusRTUBackend() = default;
  ~ModbusRTUBackend() override;

  bool Initialize(const BaseBackendOption &runtime_option) override;
  bool Open() override;
  bool ReadData(uint8_t mode, int addr, unsigned char *data, int read_size) override;
  bool WriteData(uint8_t mode, int addr, unsigned char *data, int write_size) override;

  enum {
    ReadBits = 0x01,
    ReadInputBits,
    ReadRegisters,
    ReadInputRegisters,
    WriteBit,
    WriteRegister,
    WriteBits = 0x0F,
    WriteRegisters = 0x10,
  };

 private:
  ModbusOption modbus_option_;
  modbus_t *modbus_t_ = nullptr;
};
}
}
