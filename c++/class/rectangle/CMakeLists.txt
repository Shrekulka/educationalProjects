cmake_minimum_required(VERSION 3.20)
project(rectangle)

set(CMAKE_CXX_STANDARD 23)

add_executable(rectangle main.cpp Rectangle.cpp Rectangle.h pch.h)
