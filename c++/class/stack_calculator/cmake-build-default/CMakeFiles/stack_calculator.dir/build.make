# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.26

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
CMAKE_COMMAND = /opt/homebrew/Cellar/cmake/3.26.4/bin/cmake

# The command to remove a file.
RM = /opt/homebrew/Cellar/cmake/3.26.4/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/shrekulka/educationalProjects/c++/class/stack_calculator

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/shrekulka/educationalProjects/c++/class/stack_calculator/cmake-build-default

# Include any dependencies generated for this target.
include CMakeFiles/stack_calculator.dir/depend.make
# Include the progress variables for this target.
include CMakeFiles/stack_calculator.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/stack_calculator.dir/flags.make

CMakeFiles/stack_calculator.dir/main.cpp.o: CMakeFiles/stack_calculator.dir/flags.make
CMakeFiles/stack_calculator.dir/main.cpp.o: /Users/shrekulka/educationalProjects/c++/class/stack_calculator/main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/educationalProjects/c++/class/stack_calculator/cmake-build-default/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/stack_calculator.dir/main.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/stack_calculator.dir/main.cpp.o -c /Users/shrekulka/educationalProjects/c++/class/stack_calculator/main.cpp

CMakeFiles/stack_calculator.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/stack_calculator.dir/main.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/educationalProjects/c++/class/stack_calculator/main.cpp > CMakeFiles/stack_calculator.dir/main.cpp.i

CMakeFiles/stack_calculator.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/stack_calculator.dir/main.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/educationalProjects/c++/class/stack_calculator/main.cpp -o CMakeFiles/stack_calculator.dir/main.cpp.s

# Object files for target stack_calculator
stack_calculator_OBJECTS = \
"CMakeFiles/stack_calculator.dir/main.cpp.o"

# External object files for target stack_calculator
stack_calculator_EXTERNAL_OBJECTS =

stack_calculator: CMakeFiles/stack_calculator.dir/main.cpp.o
stack_calculator: CMakeFiles/stack_calculator.dir/build.make
stack_calculator: CMakeFiles/stack_calculator.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/shrekulka/educationalProjects/c++/class/stack_calculator/cmake-build-default/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable stack_calculator"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/stack_calculator.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/stack_calculator.dir/build: stack_calculator
.PHONY : CMakeFiles/stack_calculator.dir/build

CMakeFiles/stack_calculator.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/stack_calculator.dir/cmake_clean.cmake
.PHONY : CMakeFiles/stack_calculator.dir/clean

CMakeFiles/stack_calculator.dir/depend:
	cd /Users/shrekulka/educationalProjects/c++/class/stack_calculator/cmake-build-default && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/shrekulka/educationalProjects/c++/class/stack_calculator /Users/shrekulka/educationalProjects/c++/class/stack_calculator /Users/shrekulka/educationalProjects/c++/class/stack_calculator/cmake-build-default /Users/shrekulka/educationalProjects/c++/class/stack_calculator/cmake-build-default /Users/shrekulka/educationalProjects/c++/class/stack_calculator/cmake-build-default/CMakeFiles/stack_calculator.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/stack_calculator.dir/depend

