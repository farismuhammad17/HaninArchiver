CXX ?= g++

ifeq ($(OS),Windows_NT)
    LIB_EXT = .dll
    LDFLAGS = -shared
else
    UNAME_S := $(shell uname -s)
    LIB_EXT = .so
    LDFLAGS = -shared
    ifeq ($(UNAME_S), Darwin)
        LDFLAGS += -undefined dynamic_lookup
    endif
endif

CXXFLAGS = -std=c++17 -Wall -O3 -fPIC -g -Iinclude -Ilibs -I.

SRC = HaneenArchiver/core/byte_checker.cpp
LIB_OUT = HaneenArchiver/core/byte_checker$(LIB_EXT)

all: $(LIB_OUT)

$(LIB_OUT): $(SRC)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o $(LIB_OUT) $(SRC)

clean:
	rm -f *.so *.so.dSYM *.dll

.PHONY: all clean
