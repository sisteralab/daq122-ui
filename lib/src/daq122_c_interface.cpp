#include "daq122_c_interface.h"
#include "libdaq/device/DAQ122/daq122.h"

extern "C" {

DAQ122Handle DAQ122_New() {
    return new libdaq::device::DAQ122();
}

void DAQ122_Delete(DAQ122Handle handle) {
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

bool DAQ122_ConfigureSamplingParameters(DAQ122Handle handle, uint64_t sample_rate, uint64_t voltage) {
    return static_cast<libdaq::device::DAQ122*>(handle)->ConfigureADCParameters(
        static_cast<libdaq::device::DAQADCSampleRate>(sample_rate),
        static_cast<libdaq::device::DAQVoltage>(voltage)
    );
}

bool DAQ122_ConfigADCChannel(DAQ122Handle handle, uint8_t channel) {
    return static_cast<libdaq::device::DAQ122*>(handle)->ConfigADCChannel(channel);
}

bool DAQ122_StartCollection(DAQ122Handle handle) {
    return static_cast<libdaq::device::DAQ122*>(handle)->StartADCCollection();
}

bool DAQ122_StopCollection(DAQ122Handle handle) {
    return static_cast<libdaq::device::DAQ122*>(handle)->StopADCCollection();
}

bool DAQ122_TryReadData(DAQ122Handle handle, uint8_t channel, double *read_buffer, uint32_t read_size, uint32_t timeout) {
    return static_cast<libdaq::device::DAQ122*>(handle)->TryReadADCData(
        channel,
        read_buffer,
        read_size,
        timeout
    );
}

} // extern "C"
