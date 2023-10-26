cmake_minimum_required(VERSION 3.26)
project(function_for_converting_IP_addresses C)

set(CMAKE_C_STANDARD 23)

add_executable(function_for_converting_IP_addresses main.c
        common.h
        socket_address_utility.h
        socket_address_utility.c
        config.h)
