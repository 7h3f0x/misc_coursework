
# Source Files

1. `lamport.cpp`: source file for question1 in the tutorial
2. `vector_clock.cpp`: source file for question2 in the tutorial
2. `Makefile`: build file for the programs
3. `input`: my sample input to test the programs
4. `output_lamport`: output of the `lamport` program for my sample input
4. `output_vector_clock`: output of the `vector_clock` program for my sample input

# Compiling the programs

In order to compile the files, one needs the
[make](https://www.gnu.org/software/make/) program and a C++ compiler
(preferably [g++](https://gcc.gnu.org/)).  To invoke the build process, just run
the `make` command in root of this directory. This uses `g++` by default, but
other compilers can also be used by specifying them on the command line.
Specific program can also be built by specifying on command line

Example:

```bash

# default build
make

# build with clang++ compiler
make CXX=clang++

# create a debug build
make DEBUG=1

# build just the lamport program
make lamport

```

# Running the program

The programs take input from user. It can be used with input file using the
shell's input redirection feature as shown below:

```bash
./lamport < input
```

