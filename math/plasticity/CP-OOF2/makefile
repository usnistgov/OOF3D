# 
# Makefile to build the thing on Linux.

SOURCES := $(shell find . -name '*.cpp')
OBJECTS := $(SOURCES:%.cpp=%.o)

main: $(OBJECTS)
	g++ -std=c++11 -g $(OBJECTS) -o main

%.o : %.cpp %.hpp
	g++ -std=c++11 -g -c $< -o $@

clean:
	rm -vf main *.o 
