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
CMAKE_SOURCE_DIR = /Users/shrekulka/educationalProjects/c++/class/rectangle

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/shrekulka/educationalProjects/c++/class/rectangle/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/rectangle.dir/depend.make
# Include the progress variables for this target.
include CMakeFiles/rectangle.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/rectangle.dir/flags.make

CMakeFiles/rectangle.dir/main.cpp.o: CMakeFiles/rectangle.dir/flags.make
CMakeFiles/rectangle.dir/main.cpp.o: ../main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/educationalProjects/c++/class/rectangle/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/rectangle.dir/main.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/rectangle.dir/main.cpp.o -c /Users/shrekulka/educationalProjects/c++/class/rectangle/main.cpp

CMakeFiles/rectangle.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/rectangle.dir/main.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/educationalProjects/c++/class/rectangle/main.cpp > CMakeFiles/rectangle.dir/main.cpp.i

CMakeFiles/rectangle.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/rectangle.dir/main.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/educationalProjects/c++/class/rectangle/main.cpp -o CMakeFiles/rectangle.dir/main.cpp.s

CMakeFiles/rectangle.dir/Rectangle.cpp.o: CMakeFiles/rectangle.dir/flags.make
CMakeFiles/rectangle.dir/Rectangle.cpp.o: ../Rectangle.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/shrekulka/educationalProjects/c++/class/rectangle/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/rectangle.dir/Rectangle.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/rectangle.dir/Rectangle.cpp.o -c /Users/shrekulka/educationalProjects/c++/class/rectangle/Rectangle.cpp

CMakeFiles/rectangle.dir/Rectangle.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/rectangle.dir/Rectangle.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/shrekulka/educationalProjects/c++/class/rectangle/Rectangle.cpp > CMakeFiles/rectangle.dir/Rectangle.cpp.i

CMakeFiles/rectangle.dir/Rectangle.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/rectangle.dir/Rectangle.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/shrekulka/educationalProjects/c++/class/rectangle/Rectangle.cpp -o CMakeFiles/rectangle.dir/Rectangle.cpp.s

# Object files for target rectangle
rectangle_OBJECTS = \
"CMakeFiles/rectangle.dir/main.cpp.o" \
"CMakeFiles/rectangle.dir/Rectangle.cpp.o"

# External object files for target rectangle
rectangle_EXTERNAL_OBJECTS =

rectangle: CMakeFiles/rectangle.dir/main.cpp.o
rectangle: CMakeFiles/rectangle.dir/Rectangle.cpp.o
rectangle: CMakeFiles/rectangle.dir/build.make
rectangle: CMakeFiles/rectangle.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/shrekulka/educationalProjects/c++/class/rectangle/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX executable rectangle"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/rectangle.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/rectangle.dir/build: rectangle
.PHONY : CMakeFiles/rectangle.dir/build

CMakeFiles/rectangle.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/rectangle.dir/cmake_clean.cmake
.PHONY : CMakeFiles/rectangle.dir/clean

CMakeFiles/rectangle.dir/depend:
	cd /Users/shrekulka/educationalProjects/c++/class/rectangle/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/shrekulka/educationalProjects/c++/class/rectangle /Users/shrekulka/educationalProjects/c++/class/rectangle /Users/shrekulka/educationalProjects/c++/class/rectangle/cmake-build-debug /Users/shrekulka/educationalProjects/c++/class/rectangle/cmake-build-debug /Users/shrekulka/educationalProjects/c++/class/rectangle/cmake-build-debug/CMakeFiles/rectangle.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/rectangle.dir/depend
