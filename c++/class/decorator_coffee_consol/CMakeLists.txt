cmake_minimum_required(VERSION 3.20)
project(decorator_coffee_consol)

set(CMAKE_CXX_STANDARD 23)

add_executable(decorator_coffee_consol main.cpp Additives.cpp Additives.h pch.h Beverage.cpp Beverage.h DarkMocha.cpp DarkMocha.h DarkRoast.cpp DarkRoast.h Latte.cpp Latte.h Milk.cpp Milk.h Mocha.cpp Mocha.h Whip.cpp Whip.h WhiteMocha.cpp WhiteMocha.h)
