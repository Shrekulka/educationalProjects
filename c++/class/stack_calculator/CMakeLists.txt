cmake_minimum_required(VERSION 3.20)
project(stack_calculator)

set(CMAKE_CXX_STANDARD 23)

add_executable(stack_calculator main.cpp Stack.h pch.h)
