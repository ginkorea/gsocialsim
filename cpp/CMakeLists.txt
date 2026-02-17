cmake_minimum_required(VERSION 3.20)
project(gsocialsim_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(gsocialsim_cpp
    src/main.cpp
    src/kernel.cpp
    src/agent.cpp
    src/data_source.cpp
    src/stimulus_ingestion.cpp
    src/utils.cpp
)

target_include_directories(gsocialsim_cpp PRIVATE include)
target_compile_options(gsocialsim_cpp PRIVATE -O3)
