#pragma once

#include <vector>

extern "C" {
#include "event2/event.h"
#include "event2/bufferevent.h"
}
#include "backend/base_backend.h"
#include "backend/base_backend_option.h"

namespace libdaq {
namespace backend {
class TCPClientBackend : public BaseBackend {
 public:
  TCPClientBackend() = default;
  ~TCPClientBackend() override;
  bool Initialize(const BaseBackendOption &runtime_option) override;
  bool Open() override;
  bool ReadData(unsigned char *data, int read_size, int *actual_size, int timeout) override;
  bool WriteData(unsigned char *data, int write_size, int *actual_size, int timeout) override;

 private:
  TCPSocketOption tcp_socket_option_;
#ifdef WIN32
  SOCKET socket_ = 0;
#endif
  static bool InitializeWinsock();
  bool CreateSocket();
  bool SetSocketNonBlockingMode() const;
  bool ConnectToDevice() const;
  bool SetSocketTimeout() const;
};
}
}
