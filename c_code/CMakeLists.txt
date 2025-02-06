cmake_minimum_required(VERSION 3.13)
include(pico_sdk_import.cmake)

project(pico-sequencer)

pico_sdk_init()

add_executable(sequencer
    main.c
)

target_link_libraries(sequencer pico_stdlib)
pico_add_extra_outputs(sequencer)
