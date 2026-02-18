cmake_minimum_required(VERSION 3.20)
project(gsocialsim_tests LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include parent directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../include)

# Test: Subscription Service
add_executable(test_subscription_service
    test_subscription_service.cpp
    ../src/subscription_service.cpp
)

# Test: Belief Dynamics
add_executable(test_belief_dynamics
    test_belief_dynamics.cpp
    ../src/belief_dynamics.cpp
)

# Test: Belief Dynamics (Simplified)
add_executable(test_belief_dynamics_simple
    test_belief_dynamics_simple.cpp
    ../src/belief_dynamics.cpp
)

# Test: Population Layer
add_executable(test_population_layer
    test_population_layer.cpp
    ../src/population_layer.cpp
    ../src/geo_world.cpp
    ../src/utils.cpp
)

# Test: Agent Demographics
add_executable(test_agent_demographics
    test_agent_demographics.cpp
    ../src/agent.cpp
    ../src/agent_demographics.cpp
    ../src/demographic_sampling.cpp
    ../src/population_layer.cpp
    ../src/belief_dynamics.cpp
    ../src/content_targeting.cpp
    ../src/feed_queue.cpp
    ../src/geo_world.cpp
    ../src/country.cpp
    ../src/utils.cpp
)

# Compile options
target_compile_options(test_subscription_service PRIVATE -O2)
target_compile_options(test_belief_dynamics PRIVATE -O2)
target_compile_options(test_population_layer PRIVATE -O2)
target_compile_options(test_agent_demographics PRIVATE -O2)
