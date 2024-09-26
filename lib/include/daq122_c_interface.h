#ifndef DAQ122_C_INTERFACE_H
#define DAQ122_C_INTERFACE_H
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef void* DAQ122Handle;

DAQ122Handle DAQ122_Create();
void DAQ122_Delete(DAQ122Handle handle);

bool DAQ122_ConnectedDevice(DAQ122Handle handle);
bool DAQ122_UseUSBBackend(DAQ122Handle handle);
bool DAQ122_InitializeDevice(DAQ122Handle handle);
bool DAQ122_ConfigureSamplingParameters(DAQ122Handle handle, uint64_t sample_rate, uint64_t voltage);
bool DAQ122_ConfigADCChannel(DAQ122Handle handle, uint8_t channel);
bool DAQ122_StartCollection(DAQ122Handle handle);
bool DAQ122_StopCollection(DAQ122Handle handle);
bool DAQ122_TryReadData(DAQ122Handle handle, uint8_t channel, double *read_buffer, uint32_t read_size, uint32_t timeout);

#ifdef __cplusplus
}
#endif

#endif // DAQ122_C_INTERFACE_H
