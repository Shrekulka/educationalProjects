cmake_minimum_required(VERSION 3.26)
project(simple_time_and_date_server C)

set(CMAKE_C_STANDARD 11)

add_executable(simple_time_and_date_server main.c
        error.h
        error.c
        common.h
        config.h
        utils.h
        utils.c)
