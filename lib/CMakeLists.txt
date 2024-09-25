cmake_minimum_required(VERSION 3.12)
project(daq122_bindings)

set(CMAKE_CXX_STANDARD 11)

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)

# Добавление директорий с заголовочными файлами
include_directories(libdaq)

# Добавление исходных файлов
add_library(daq122 MODULE daq122_bindings.cpp)

# Связывание с Python и pybind11
target_include_directories(daq122 PRIVATE ${Python3_INCLUDE_DIRS} ${pybind11_INCLUDE_DIRS})
target_link_libraries(daq122 PRIVATE ${Python3_LIBRARIES} pybind11::module)

# Установка свойств для создания динамической библиотеки
set_target_properties(daq122 PROPERTIES PREFIX "" SUFFIX ".so")
