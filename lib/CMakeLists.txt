cmake_minimum_required(VERSION 3.12)
project(daq122_bindings)

set(CMAKE_CXX_STANDARD 11)

# Найти Python3
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Получить пути к pybind11
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

# Укажите путь к CMake-файлам pybind11
set(CMAKE_PREFIX_PATH ${PYBIND11_CMAKE_DIR})

# Найти pybind11
find_package(pybind11 REQUIRED)

# Добавление директорий с заголовочными файлами
include_directories(libdaq ${Python3_INCLUDE_DIRS} ${PYBIND11_INCLUDE_DIR})

# Добавление исходных файлов
add_library(daq122 MODULE daq122_bindings.cpp)

# Связывание с Python и pybind11
target_include_directories(daq122 PRIVATE ${Python3_INCLUDE_DIRS} ${PYBIND11_INCLUDE_DIR})
target_link_libraries(daq122 PRIVATE ${Python3_LIBRARIES} pybind11::module)

# Установка свойств для создания динамической библиотеки
set_target_properties(daq122 PROPERTIES PREFIX "" SUFFIX ".so")
