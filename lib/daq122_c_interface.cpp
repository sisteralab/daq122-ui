#include "daq122_c_interface.h"
#include "libdaq/device/DAQ122/daq122.h"

extern "C" {

DAQ122Handle DAQ122_Create() {
    return new libdaq::device::DAQ122();
}

void DAQ122_Destroy(DAQ122Handle handle) {
    delete static_cast<libdaq::device::DAQ122*>(handle);
}

bool DAQ122_ConnectedDevice(DAQ122Handle handle) {
    return static_cast<libdaq::device::DAQ122*>(handle)->ConnectedDevice();
}

bool DAQ122_UseUSBBackend(DAQ122Handle handle) {
    return static_cast<libdaq::device::DAQ122*>(handle)->UseUSBBackend();
}

bool DAQ122_InitializeDevice(DAQ122Handle handle) {
    return static_cast<libdaq::device::DAQ122*>(handle)->InitializeDevice();
}

bool DAQ122_ConfigureADCParameters(DAQ122Handle handle, int sample_rate, int voltage) {
    return static_cast<libdaq::device::DAQ122*>(handle)->ConfigureADCParameters(
        static_cast<libdaq::device::DAQADCSampleRate>(sample_rate),
        static_cast<libdaq::device::DAQVoltage>(voltage)
    );
}

bool DAQ122_ConfigADCChannel(DAQ122Handle handle, uint8_t channel) {
    return static_cast<libdaq::device::DAQ122*>(handle)->ConfigADCChannel(channel);
}

bool DAQ122_StartADCCollection(DAQ122Handle handle) {
    return static_cast<libdaq::device::DAQ122*>(handle)->StartADCCollection();
}

bool DAQ122_StopADCCollection(DAQ122Handle handle) {
    return static_cast<libdaq::device::DAQ122*>(handle)->StopADCCollection();
}

} // extern "C"
