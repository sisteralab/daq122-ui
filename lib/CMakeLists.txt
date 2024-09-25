cmake_minimum_required(VERSION 3.12)
project(daq122_bindings)

set(CMAKE_CXX_STANDARD 11)

# Найти Python3
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Указать путь к pybind11
set(PYBIND11_INCLUDE_DIR $(python -c "import pybind11; print(pybind11.get_include())"))
set(PYBIND11_LIBRARY_DIR $(python -c "import pybind11; print(pybind11.get_cmake_dir())"))

# Добавление директорий с заголовочными файлами
include_directories(libdaq ${PYBIND11_INCLUDE_DIR})

# Добавление исходных файлов
add_library(daq122 MODULE daq122_bindings.cpp)

# Связывание с Python и pybind11
target_include_directories(daq122 PRIVATE ${Python3_INCLUDE_DIRS} ${PYBIND11_INCLUDE_DIR})
target_link_libraries(daq122 PRIVATE ${Python3_LIBRARIES} ${PYBIND11_LIBRARY_DIR}/pybind11::module)

# Установка свойств для создания динамической библиотеки
set_target_properties(daq122 PROPERTIES PREFIX "" SUFFIX ".so")
