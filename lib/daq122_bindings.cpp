#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "libdaq/device/daq122.h"

using namespace libdaq::device;
namespace py = pybind11;

PYBIND11_MODULE(daq122, m) {
    py::class_<DAQ122>(m, "DAQ122")
        .def(py::init<>())
        .def("ConnectedDevice", &DAQ122::ConnectedDevice)
        .def("UseUSBBackend", &DAQ122::UseUSBBackend)
        .def("InitializeDevice", &DAQ122::InitializeDevice)
        .def("ConfigureADCParameters", &DAQ122::ConfigureADCParameters)
        .def("ConfigADCChannel", &DAQ122::ConfigADCChannel)
        .def("StartADCCollection", &DAQ122::StartADCCollection)
        .def("StopADCCollection", &DAQ122::StopADCCollection);
}
