#ifndef DAQ122_C_INTERFACE_H
#define DAQ122_C_INTERFACE_H

#ifdef __cplusplus
extern "C" {
#endif

typedef void* DAQ122Handle;

DAQ122Handle DAQ122_Create();
void DAQ122_Destroy(DAQ122Handle handle);

bool DAQ122_ConnectedDevice(DAQ122Handle handle);
bool DAQ122_UseUSBBackend(DAQ122Handle handle);
bool DAQ122_InitializeDevice(DAQ122Handle handle);
bool DAQ122_ConfigureADCParameters(DAQ122Handle handle, int sample_rate, int voltage);
bool DAQ122_ConfigADCChannel(DAQ122Handle handle, uint8_t channel);
bool DAQ122_StartADCCollection(DAQ122Handle handle);
bool DAQ122_StopADCCollection(DAQ122Handle handle);

#ifdef __cplusplus
}
#endif

#endif // DAQ122_C_INTERFACE_H
