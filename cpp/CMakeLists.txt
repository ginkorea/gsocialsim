cmake_minimum_required(VERSION 3.20)
project(gsocialsim_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(gsocialsim_cpp
    src/main.cpp
    src/kernel.cpp
    src/agent.cpp
    src/agent_demographics.cpp
    src/belief_dynamics.cpp
    src/data_source.cpp
    src/stimulus_ingestion.cpp
    src/subscription_service.cpp
    src/network.cpp
    src/network_manager.cpp
    src/population_layer.cpp
    src/demographic_sampling.cpp
    src/content_targeting.cpp
    src/global_social_reality.cpp
    src/feed_queue.cpp
    src/geo_world.cpp
    src/country.cpp
    src/utils.cpp
)

target_include_directories(gsocialsim_cpp PRIVATE include)
target_compile_options(gsocialsim_cpp PRIVATE -O3)
