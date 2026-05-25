cmake_minimum_required(VERSION 3.26)
project(byte_order_detection C)

set(CMAKE_C_STANDARD 23)

add_executable(byte_order_detection main.c
        common.h
        config.h
        functions.h
        functions.c
        utils.h
        os_specific.h)
