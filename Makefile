# Arquivo: Makefile
# Descrição: Makefile para o projeto Mandelbrot
# Autores: Assistente (Gemini)
# Data: 23/02/2026

# Identifica o sistema operacional para definir o nome da biblioteca
ifeq ($(OS),Windows_NT)
    LIB_NAME = mandelbrot.dll
    PYTHON_CMD = python
    RM_CMD = del /Q *.dll 2>nul || exit 0
else
    UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S),Darwin)
        LIB_NAME = libmandelbrot.dylib
    else
        LIB_NAME = libmandelbrot.so
    endif
    PYTHON_CMD = python3
    RM_CMD = rm -f *.so *.dll *.dylib
endif

CC = gcc
CFLAGS = -O2 -shared -fPIC
LDFLAGS = -lm

all: $(LIB_NAME)

$(LIB_NAME): src/mandelbrot.c src/mandelbrot.h
	$(CC) $(CFLAGS) -o $(LIB_NAME) src/mandelbrot.c $(LDFLAGS)

run: all
	$(PYTHON_CMD) src/main.py

demo: all
	@echo "Executando demonstração..."
	$(PYTHON_CMD) src/main.py --demo

clean:
	$(RM_CMD)
