# target: all - Default target
all:
	gcc src/fccommands.c src/fctools.c src/helpers.c src/overture/*.c src/horizon/*.c -lSDL2 -lSDL2_ttf -lz -g -o fctools
	gcc src/fcc.c src/horizon/*_parser.c src/horizon/*_compiler.c src/helpers.c -lz -g -o fcc

# target: release - Build with optimizations and without debug symbols
release:
	gcc src/fccommands.c src/fctools.c src/helpers.c src/overture/*.c src/horizon/*.c -lSDL2 -lSDL2_ttf -lz -O3 -o fctools
	gcc src/fcc.c src/horizon/*_parser.c src/horizon/*_compiler.c src/helpers.c -lz -O3 -o fcc

# target: help - Display available targets
help:
	grep -E "^# target:" Makefile
