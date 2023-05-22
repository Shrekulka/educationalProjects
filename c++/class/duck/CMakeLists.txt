cmake_minimum_required(VERSION 3.20)
project(duck)

set(CMAKE_CXX_STANDARD 23)

add_executable(duck main.cpp Flyable.cpp Flyable.h Flight.cpp Flight.h NotFlight.cpp NotFlight.h Quackable.cpp Quackable.h Quack.cpp Quack.h NotQuack.cpp NotQuack.h Duck.cpp Duck.h MallardDuck.cpp MallardDuck.h RedHatDuck.cpp RedHatDuck.h RubberDuck.cpp RubberDuck.h MedicineDuck.cpp MedicineDuck.h Hunter.cpp Hunter.h Lake.cpp Lake.h stdafx.h)
