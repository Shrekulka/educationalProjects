cmake_minimum_required(VERSION 3.26)
project(TCP_Server)

set(CMAKE_CXX_STANDARD 23)

add_executable(TCP_Server main.cpp pch.h CommandParser.cpp CommandParser.h ConnectionHandler.h SimpleCommandHandler.cpp SimpleCommandHandler.h TCPServer.cpp TCPServer.h NetworkException.h)
