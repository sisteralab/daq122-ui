cmake_minimum_required(VERSION 3.12)
project(daq122)

set(CMAKE_CXX_STANDARD 11)


include(${CMAKE_SOURCE_DIR}/cmake/daq.cmake)


set(SOURCES
    daq122_c_interface.cpp
)

add_library(daq122 SHARED ${SOURCES})

set_target_properties(daq122 PROPERTIES
    PREFIX ""
    LINKER_LANGUAGE CXX
)

install(TARGETS daq122
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)
