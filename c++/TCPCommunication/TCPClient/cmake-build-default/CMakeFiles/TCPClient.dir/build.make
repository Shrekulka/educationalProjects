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
CMAKE_SOURCE_DIR = /Users/shrekulka/educationalProjects/c++/TCPCommunication/TCPClient

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/shrekulka/educationalProjects/c++/TCPCommunication/TCPClient/cmake-build-default

# Include any dependencies generated for this target.
include CMakeFiles/TCPClient.dir/depend.make
# Include the progress variables for this target.
include CMakeFiles/TCPClient.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/TCPClient.dir/flags.make

CMakeFiles/TCPClient.dir/main.cpp.o: CMakeFiles/TCPClient.dir/flags.make
CMakeFiles/TCPClient.dir/main.cpp.o: /Users/shrekulka/educationalProjects/c++/TCPCommunication/TCPClient/main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/educationalProjects/c++/TCPCommunication/TCPClient/cmake-build-default/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/TCPClient.dir/main.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/TCPClient.dir/main.cpp.o -c /Users/shrekulka/educationalProjects/c++/TCPCommunication/TCPClient/main.cpp

CMakeFiles/TCPClient.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/TCPClient.dir/main.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/educationalProjects/c++/TCPCommunication/TCPClient/main.cpp > CMakeFiles/TCPClient.dir/main.cpp.i

CMakeFiles/TCPClient.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/TCPClient.dir/main.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/educationalProjects/c++/TCPCommunication/TCPClient/main.cpp -o CMakeFiles/TCPClient.dir/main.cpp.s

# Object files for target TCPClient
TCPClient_OBJECTS = \
"CMakeFiles/TCPClient.dir/main.cpp.o"

# External object files for target TCPClient
TCPClient_EXTERNAL_OBJECTS =

TCPClient: CMakeFiles/TCPClient.dir/main.cpp.o
TCPClient: CMakeFiles/TCPClient.dir/build.make
TCPClient: CMakeFiles/TCPClient.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/shrekulka/educationalProjects/c++/TCPCommunication/TCPClient/cmake-build-default/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable TCPClient"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/TCPClient.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/TCPClient.dir/build: TCPClient
.PHONY : CMakeFiles/TCPClient.dir/build

CMakeFiles/TCPClient.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/TCPClient.dir/cmake_clean.cmake
.PHONY : CMakeFiles/TCPClient.dir/clean

CMakeFiles/TCPClient.dir/depend:
	cd /Users/shrekulka/educationalProjects/c++/TCPCommunication/TCPClient/cmake-build-default && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/shrekulka/educationalProjects/c++/TCPCommunication/TCPClient /Users/shrekulka/educationalProjects/c++/TCPCommunication/TCPClient /Users/shrekulka/educationalProjects/c++/TCPCommunication/TCPClient/cmake-build-default /Users/shrekulka/educationalProjects/c++/TCPCommunication/TCPClient/cmake-build-default /Users/shrekulka/educationalProjects/c++/TCPCommunication/TCPClient/cmake-build-default/CMakeFiles/TCPClient.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/TCPClient.dir/depend
