#pragma once
namespace libdaq {
namespace device {
/**
 * @brief DAQ热电偶型号
 */
enum DAQThermocoupleModule {
  Unknown=0,        ///< 未知传感器
  K,        ///< K型
  T,        ///< T型
  J,
  E,
  B,
  N,
  R,
  S,
  WRe3_25,
  WRe5_26,
  WRe5_20
};

}  // namespace device
}  // namespace libdaq
