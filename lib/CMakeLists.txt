cmake_minimum_required(VERSION 3.12)
project(daq122_bindings)

set(CMAKE_CXX_STANDARD 11)

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

execute_process(
    COMMAND ${Python3_EXECUTABLE} -m pybind11 --includes
    OUTPUT_VARIABLE PYBIND11_INCLUDE_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

execute_process(
    COMMAND ${Python3_EXECUTABLE} -m pybind11 --cmakedir
    OUTPUT_VARIABLE PYBIND11_CMAKE_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

set(CMAKE_PREFIX_PATH ${PYBIND11_CMAKE_DIR})

find_package(pybind11 REQUIRED)

include_directories(${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/third_party ${Python3_INCLUDE_DIRS} ${PYBIND11_INCLUDE_DIR})

add_library(daq122 MODULE daq122_bindings.cpp)

target_include_directories(daq122 PRIVATE ${Python3_INCLUDE_DIRS} ${PYBIND11_INCLUDE_DIR})
target_link_libraries(daq122 PRIVATE ${Python3_LIBRARIES} pybind11::module)

set_target_properties(daq122 PROPERTIES PREFIX "" SUFFIX ".so")
