ifndef CXX
    CXX=g++
endif

ifdef DEBUG
    CPPFLAGS=-O0 -g
else
    CPPFLAGS=-O3
endif

all: lamport vector_clock
    $(MAKE) clean

lamport: lamport.o
    $(CXX) $(CPPFLAGS) -o $@ $^

vector_clock: vector_clock.o
    $(CXX) $(CPPFLAGS) -o $@ $^

%.o: %.cpp
    $(CXX) $(CPPFLAGS) -c -o $@ $<

clean:
    -rm *.o

distclean: clean
    -rm lamport vector_clock
