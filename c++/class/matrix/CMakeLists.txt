cmake_minimum_required(VERSION 3.20)
project(matrix)

set(CMAKE_CXX_STANDARD 23)

add_executable(matrix main.cpp pch.h Matrix.cpp Matrix.h Row.cpp Row.h)
