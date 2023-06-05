cmake_minimum_required(VERSION 3.20)
project(class_string)

set(CMAKE_CXX_STANDARD 23)

add_executable(class_string main.cpp pch.h String.cpp String.h)
