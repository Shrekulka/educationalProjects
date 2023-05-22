cmake_minimum_required(VERSION 3.20)
project(map_and__multimap)

set(CMAKE_CXX_STANDARD 23)

add_executable(map_and__multimap main.cpp pch.h Word.cpp Word.h Opposite.cpp Opposite.h)
