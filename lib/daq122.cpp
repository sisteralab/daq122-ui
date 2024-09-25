#include "libdaq.h"

extern "C" {
    libdaq::device::DAQ122* DAQ122_new() {
        return new libdaq::device::DAQ122();
    }

    void DAQ122_delete(libdaq::device::DAQ122* daq) {
        delete daq;
    }

    int DAQ122_TryReadADCData(libdaq::device::DAQ122* daq, unsigned char channel, double* data) {
        return daq->TryReadADCData(channel, data);
    }
}