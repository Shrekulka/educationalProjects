cmake_minimum_required(VERSION 3.26)
project(tcp_client_for_determining_time_and_date C)

set(CMAKE_C_STANDARD 23)

add_executable(tcp_client_for_determining_time_and_date main.c
        common.h
        socket.h
        config.h
        error.h
        error.c
        timeutil.h
        timeutil.c
)
