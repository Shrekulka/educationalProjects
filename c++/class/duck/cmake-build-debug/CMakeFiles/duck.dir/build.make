# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.20

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /Applications/CLion.app/Contents/bin/cmake/mac/bin/cmake

# The command to remove a file.
RM = /Applications/CLion.app/Contents/bin/cmake/mac/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/shrekulka/c++Projects/class/duck

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/shrekulka/c++Projects/class/duck/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/duck.dir/depend.make
# Include the progress variables for this target.
include CMakeFiles/duck.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/duck.dir/flags.make

CMakeFiles/duck.dir/main.cpp.o: CMakeFiles/duck.dir/flags.make
CMakeFiles/duck.dir/main.cpp.o: ../main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/duck.dir/main.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/duck.dir/main.cpp.o -c /Users/shrekulka/c++Projects/class/duck/main.cpp

CMakeFiles/duck.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/duck.dir/main.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/c++Projects/class/duck/main.cpp > CMakeFiles/duck.dir/main.cpp.i

CMakeFiles/duck.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/duck.dir/main.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/c++Projects/class/duck/main.cpp -o CMakeFiles/duck.dir/main.cpp.s

CMakeFiles/duck.dir/Flyable.cpp.o: CMakeFiles/duck.dir/flags.make
CMakeFiles/duck.dir/Flyable.cpp.o: ../Flyable.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/duck.dir/Flyable.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/duck.dir/Flyable.cpp.o -c /Users/shrekulka/c++Projects/class/duck/Flyable.cpp

CMakeFiles/duck.dir/Flyable.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/duck.dir/Flyable.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/c++Projects/class/duck/Flyable.cpp > CMakeFiles/duck.dir/Flyable.cpp.i

CMakeFiles/duck.dir/Flyable.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/duck.dir/Flyable.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/c++Projects/class/duck/Flyable.cpp -o CMakeFiles/duck.dir/Flyable.cpp.s

CMakeFiles/duck.dir/Flight.cpp.o: CMakeFiles/duck.dir/flags.make
CMakeFiles/duck.dir/Flight.cpp.o: ../Flight.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/duck.dir/Flight.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/duck.dir/Flight.cpp.o -c /Users/shrekulka/c++Projects/class/duck/Flight.cpp

CMakeFiles/duck.dir/Flight.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/duck.dir/Flight.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/c++Projects/class/duck/Flight.cpp > CMakeFiles/duck.dir/Flight.cpp.i

CMakeFiles/duck.dir/Flight.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/duck.dir/Flight.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/c++Projects/class/duck/Flight.cpp -o CMakeFiles/duck.dir/Flight.cpp.s

CMakeFiles/duck.dir/NotFlight.cpp.o: CMakeFiles/duck.dir/flags.make
CMakeFiles/duck.dir/NotFlight.cpp.o: ../NotFlight.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object CMakeFiles/duck.dir/NotFlight.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/duck.dir/NotFlight.cpp.o -c /Users/shrekulka/c++Projects/class/duck/NotFlight.cpp

CMakeFiles/duck.dir/NotFlight.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/duck.dir/NotFlight.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/c++Projects/class/duck/NotFlight.cpp > CMakeFiles/duck.dir/NotFlight.cpp.i

CMakeFiles/duck.dir/NotFlight.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/duck.dir/NotFlight.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/c++Projects/class/duck/NotFlight.cpp -o CMakeFiles/duck.dir/NotFlight.cpp.s

CMakeFiles/duck.dir/Quackable.cpp.o: CMakeFiles/duck.dir/flags.make
CMakeFiles/duck.dir/Quackable.cpp.o: ../Quackable.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building CXX object CMakeFiles/duck.dir/Quackable.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/duck.dir/Quackable.cpp.o -c /Users/shrekulka/c++Projects/class/duck/Quackable.cpp

CMakeFiles/duck.dir/Quackable.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/duck.dir/Quackable.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/c++Projects/class/duck/Quackable.cpp > CMakeFiles/duck.dir/Quackable.cpp.i

CMakeFiles/duck.dir/Quackable.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/duck.dir/Quackable.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/c++Projects/class/duck/Quackable.cpp -o CMakeFiles/duck.dir/Quackable.cpp.s

CMakeFiles/duck.dir/Quack.cpp.o: CMakeFiles/duck.dir/flags.make
CMakeFiles/duck.dir/Quack.cpp.o: ../Quack.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Building CXX object CMakeFiles/duck.dir/Quack.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/duck.dir/Quack.cpp.o -c /Users/shrekulka/c++Projects/class/duck/Quack.cpp

CMakeFiles/duck.dir/Quack.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/duck.dir/Quack.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/c++Projects/class/duck/Quack.cpp > CMakeFiles/duck.dir/Quack.cpp.i

CMakeFiles/duck.dir/Quack.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/duck.dir/Quack.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/c++Projects/class/duck/Quack.cpp -o CMakeFiles/duck.dir/Quack.cpp.s

CMakeFiles/duck.dir/NotQuack.cpp.o: CMakeFiles/duck.dir/flags.make
CMakeFiles/duck.dir/NotQuack.cpp.o: ../NotQuack.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "Building CXX object CMakeFiles/duck.dir/NotQuack.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/duck.dir/NotQuack.cpp.o -c /Users/shrekulka/c++Projects/class/duck/NotQuack.cpp

CMakeFiles/duck.dir/NotQuack.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/duck.dir/NotQuack.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/c++Projects/class/duck/NotQuack.cpp > CMakeFiles/duck.dir/NotQuack.cpp.i

CMakeFiles/duck.dir/NotQuack.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/duck.dir/NotQuack.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/c++Projects/class/duck/NotQuack.cpp -o CMakeFiles/duck.dir/NotQuack.cpp.s

CMakeFiles/duck.dir/Duck.cpp.o: CMakeFiles/duck.dir/flags.make
CMakeFiles/duck.dir/Duck.cpp.o: ../Duck.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "Building CXX object CMakeFiles/duck.dir/Duck.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/duck.dir/Duck.cpp.o -c /Users/shrekulka/c++Projects/class/duck/Duck.cpp

CMakeFiles/duck.dir/Duck.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/duck.dir/Duck.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/c++Projects/class/duck/Duck.cpp > CMakeFiles/duck.dir/Duck.cpp.i

CMakeFiles/duck.dir/Duck.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/duck.dir/Duck.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/c++Projects/class/duck/Duck.cpp -o CMakeFiles/duck.dir/Duck.cpp.s

CMakeFiles/duck.dir/MallardDuck.cpp.o: CMakeFiles/duck.dir/flags.make
CMakeFiles/duck.dir/MallardDuck.cpp.o: ../MallardDuck.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_9) "Building CXX object CMakeFiles/duck.dir/MallardDuck.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/duck.dir/MallardDuck.cpp.o -c /Users/shrekulka/c++Projects/class/duck/MallardDuck.cpp

CMakeFiles/duck.dir/MallardDuck.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/duck.dir/MallardDuck.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/c++Projects/class/duck/MallardDuck.cpp > CMakeFiles/duck.dir/MallardDuck.cpp.i

CMakeFiles/duck.dir/MallardDuck.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/duck.dir/MallardDuck.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/c++Projects/class/duck/MallardDuck.cpp -o CMakeFiles/duck.dir/MallardDuck.cpp.s

CMakeFiles/duck.dir/RedHatDuck.cpp.o: CMakeFiles/duck.dir/flags.make
CMakeFiles/duck.dir/RedHatDuck.cpp.o: ../RedHatDuck.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_10) "Building CXX object CMakeFiles/duck.dir/RedHatDuck.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/duck.dir/RedHatDuck.cpp.o -c /Users/shrekulka/c++Projects/class/duck/RedHatDuck.cpp

CMakeFiles/duck.dir/RedHatDuck.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/duck.dir/RedHatDuck.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/c++Projects/class/duck/RedHatDuck.cpp > CMakeFiles/duck.dir/RedHatDuck.cpp.i

CMakeFiles/duck.dir/RedHatDuck.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/duck.dir/RedHatDuck.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/c++Projects/class/duck/RedHatDuck.cpp -o CMakeFiles/duck.dir/RedHatDuck.cpp.s

CMakeFiles/duck.dir/RubberDuck.cpp.o: CMakeFiles/duck.dir/flags.make
CMakeFiles/duck.dir/RubberDuck.cpp.o: ../RubberDuck.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_11) "Building CXX object CMakeFiles/duck.dir/RubberDuck.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/duck.dir/RubberDuck.cpp.o -c /Users/shrekulka/c++Projects/class/duck/RubberDuck.cpp

CMakeFiles/duck.dir/RubberDuck.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/duck.dir/RubberDuck.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/c++Projects/class/duck/RubberDuck.cpp > CMakeFiles/duck.dir/RubberDuck.cpp.i

CMakeFiles/duck.dir/RubberDuck.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/duck.dir/RubberDuck.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/c++Projects/class/duck/RubberDuck.cpp -o CMakeFiles/duck.dir/RubberDuck.cpp.s

CMakeFiles/duck.dir/MedicineDuck.cpp.o: CMakeFiles/duck.dir/flags.make
CMakeFiles/duck.dir/MedicineDuck.cpp.o: ../MedicineDuck.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_12) "Building CXX object CMakeFiles/duck.dir/MedicineDuck.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/duck.dir/MedicineDuck.cpp.o -c /Users/shrekulka/c++Projects/class/duck/MedicineDuck.cpp

CMakeFiles/duck.dir/MedicineDuck.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/duck.dir/MedicineDuck.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/c++Projects/class/duck/MedicineDuck.cpp > CMakeFiles/duck.dir/MedicineDuck.cpp.i

CMakeFiles/duck.dir/MedicineDuck.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/duck.dir/MedicineDuck.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/c++Projects/class/duck/MedicineDuck.cpp -o CMakeFiles/duck.dir/MedicineDuck.cpp.s

CMakeFiles/duck.dir/Hunter.cpp.o: CMakeFiles/duck.dir/flags.make
CMakeFiles/duck.dir/Hunter.cpp.o: ../Hunter.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_13) "Building CXX object CMakeFiles/duck.dir/Hunter.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/duck.dir/Hunter.cpp.o -c /Users/shrekulka/c++Projects/class/duck/Hunter.cpp

CMakeFiles/duck.dir/Hunter.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/duck.dir/Hunter.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/c++Projects/class/duck/Hunter.cpp > CMakeFiles/duck.dir/Hunter.cpp.i

CMakeFiles/duck.dir/Hunter.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/duck.dir/Hunter.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/c++Projects/class/duck/Hunter.cpp -o CMakeFiles/duck.dir/Hunter.cpp.s

CMakeFiles/duck.dir/Lake.cpp.o: CMakeFiles/duck.dir/flags.make
CMakeFiles/duck.dir/Lake.cpp.o: ../Lake.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_14) "Building CXX object CMakeFiles/duck.dir/Lake.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/duck.dir/Lake.cpp.o -c /Users/shrekulka/c++Projects/class/duck/Lake.cpp

CMakeFiles/duck.dir/Lake.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/duck.dir/Lake.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/c++Projects/class/duck/Lake.cpp > CMakeFiles/duck.dir/Lake.cpp.i

CMakeFiles/duck.dir/Lake.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/duck.dir/Lake.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/c++Projects/class/duck/Lake.cpp -o CMakeFiles/duck.dir/Lake.cpp.s

# Object files for target duck
duck_OBJECTS = \
"CMakeFiles/duck.dir/main.cpp.o" \
"CMakeFiles/duck.dir/Flyable.cpp.o" \
"CMakeFiles/duck.dir/Flight.cpp.o" \
"CMakeFiles/duck.dir/NotFlight.cpp.o" \
"CMakeFiles/duck.dir/Quackable.cpp.o" \
"CMakeFiles/duck.dir/Quack.cpp.o" \
"CMakeFiles/duck.dir/NotQuack.cpp.o" \
"CMakeFiles/duck.dir/Duck.cpp.o" \
"CMakeFiles/duck.dir/MallardDuck.cpp.o" \
"CMakeFiles/duck.dir/RedHatDuck.cpp.o" \
"CMakeFiles/duck.dir/RubberDuck.cpp.o" \
"CMakeFiles/duck.dir/MedicineDuck.cpp.o" \
"CMakeFiles/duck.dir/Hunter.cpp.o" \
"CMakeFiles/duck.dir/Lake.cpp.o"

# External object files for target duck
duck_EXTERNAL_OBJECTS =

duck: CMakeFiles/duck.dir/main.cpp.o
duck: CMakeFiles/duck.dir/Flyable.cpp.o
duck: CMakeFiles/duck.dir/Flight.cpp.o
duck: CMakeFiles/duck.dir/NotFlight.cpp.o
duck: CMakeFiles/duck.dir/Quackable.cpp.o
duck: CMakeFiles/duck.dir/Quack.cpp.o
duck: CMakeFiles/duck.dir/NotQuack.cpp.o
duck: CMakeFiles/duck.dir/Duck.cpp.o
duck: CMakeFiles/duck.dir/MallardDuck.cpp.o
duck: CMakeFiles/duck.dir/RedHatDuck.cpp.o
duck: CMakeFiles/duck.dir/RubberDuck.cpp.o
duck: CMakeFiles/duck.dir/MedicineDuck.cpp.o
duck: CMakeFiles/duck.dir/Hunter.cpp.o
duck: CMakeFiles/duck.dir/Lake.cpp.o
duck: CMakeFiles/duck.dir/build.make
duck: CMakeFiles/duck.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_15) "Linking CXX executable duck"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/duck.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/duck.dir/build: duck
.PHONY : CMakeFiles/duck.dir/build

CMakeFiles/duck.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/duck.dir/cmake_clean.cmake
.PHONY : CMakeFiles/duck.dir/clean

CMakeFiles/duck.dir/depend:
	cd /Users/shrekulka/c++Projects/class/duck/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/shrekulka/c++Projects/class/duck /Users/shrekulka/c++Projects/class/duck /Users/shrekulka/c++Projects/class/duck/cmake-build-debug /Users/shrekulka/c++Projects/class/duck/cmake-build-debug /Users/shrekulka/c++Projects/class/duck/cmake-build-debug/CMakeFiles/duck.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/duck.dir/depend
