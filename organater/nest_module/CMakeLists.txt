cmake_minimum_required(VERSION 3.5)
# 💡 library_nameを 'nest_module' に設定
project(nest_module CXX)

find_package(NEST QUIET)
if (NOT NEST_FOUND)
    message(FATAL_ERROR "Could not find NEST. Make sure NEST is built and installed.")
endif()

include(NestModule)

# 💡 ソースファイルをここで定義
set(MY_MODULE_SOURCES
    module.cpp
    models/local_learning_synapse.cpp
)

add_nest_module(
    library_name nest_module
    sources ${MY_MODULE_SOURCES}
)