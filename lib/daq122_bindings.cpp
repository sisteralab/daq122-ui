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
}
