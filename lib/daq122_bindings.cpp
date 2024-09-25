#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "libdaq/device/DAQ122/daq122.h"

namespace py = pybind11;

PYBIND11_MODULE(daq122, m) {
    py::class_<libdaq::device::DAQ122>(m, "DAQ122")
        .def(py::init<>())
        .def("ConnectedDevice", &libdaq::device::DAQ122::ConnectedDevice)
        .def("UseUSBBackend", &libdaq::device::DAQ122::UseUSBBackend)
        .def("InitializeDevice", &libdaq::device::DAQ122::InitializeDevice)
        .def("ConfigureADCParameters", &libdaq::device::DAQ122::ConfigureADCParameters)
        .def("ConfigADCChannel", &libdaq::device::DAQ122::ConfigADCChannel)
        .def("StartADCCollection", &libdaq::device::DAQ122::StartADCCollection)
        .def("StopADCCollection", &libdaq::device::DAQ122::StopADCCollection)
        .def("ReceiveData", &libdaq::device::DAQ122::ReceiveData)
        .def("ParseData", &libdaq::device::DAQ122::ParseData)
        .def("SendConnected", &libdaq::device::DAQ122::SendConnected)
        .def("SendStartCollection", &libdaq::device::DAQ122::SendStartCollection)
        .def("SendStopCollection", &libdaq::device::DAQ122::SendStopCollection)
        .def("InitADCChannel", &libdaq::device::DAQ122::InitADCChannel)
        .def("BuildSendPacket", &libdaq::device::DAQ122::BuildSendPacket)
        .def("SendCommand", &libdaq::device::DAQ122::SendCommand)
        .def("SendConfigureCommand", &libdaq::device::DAQ122::SendConfigureCommand);
}
