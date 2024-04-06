#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "horizon_compiler.h"
#include "horizon_parser.h"
#include "../fcerrors.h"

// Parse program to build the symbol table and check for errors
// Returns the pointer to a newly allocated program_t
// If there are any errors, they will be added to the err_array, as many as
// err_array_size allows. The program_t return will have the total error count.
// After running horizon_parse, run horizon_free on the pointer to free its
// allocated memory, regardless of if the program was error-free or not.
program_t *horizon_parse(FILE *fd, error_t *err_array, int err_array_size)
{
    fseek(fd, 0, SEEK_END);
    int size = ftell(fd);
    rewind(fd);

    program_t program = { ARCH_HORIZON };
    char *program_buf = malloc(size + 1);

    program.lines_buf = program_buf;

    // Read whole program in
    program.len_lines = 0;
    fread(program_buf, 1, size, fd);
    for (int i = 0; i < size; i++)
    {
        program_buf[i] = toupper(program_buf[i]);
    }

    // Allocate the needed program space
    int symbol_space = 100;
    program.symbols = malloc(sizeof(symbol_t) * symbol_space);
    program.len_symbols_space = symbol_space;

    uint32_t num;
    int retval;

    ho_add_symbol(&program, "RAM", 1234, HO_SYM_CONST);
    int line = 1;
    while (retval != ERR_EOF)
    {
        // This will consume whitespace even without newlines
        while (!ho_match_newline(&program_buf))
            line++;
        if (retval == ERR_EOF)
            break;

        int lines_consumed = 0;
        retval = ho_parse_statement(&program, &lines_consumed, &program_buf);
        if (retval != NO_ERR)
        {
            ho_parser_perror(NULL, retval, line);
            retval = ho_match_error(&program_buf);
        } else
        {
            retval = ho_match_newline(&program_buf);
        }

        line += lines_consumed;
        line++;
    }

    printf("unparsed text: %s\n", program_buf);

    program_t *ret = malloc(sizeof(program_t));
    *ret = program;
    return ret;
}


// Frees memory allocated by horizon_parse
void horizon_free(program_t *program)
{
    if (!program)
        return;
    if (program->lines_buf)
        free(program->lines_buf);
    if (program->len_symbols)
    {
        for (int i = 0; i < program->len_symbols; i++)
            free(program->symbols[i].name);
    }
    if (program->symbols)
        free(program->symbols);
    free(program);
    return;
}

// Parse the program at the given src_filepath and save the result in the given
// destination path dst_filename.
// The options struct changes the way the procedure operates
void horizon_compile(const char *dst_filename, const char *src_filename, struct horizon_compiler_opt *options)
{
    horizon_perror(HOR_ERR_NOT_IMPLEMENTED);
    return;
}

// Print formatted error message to the console
void horizon_perror(int error)
{
    printf("Error: ");

    switch (error)
    {
        // No error
        case HOR_OK:
            printf("\r       \r");
            break;

        // Implementation
        case HOR_ERR_NOT_IMPLEMENTED:
            printf("not implemented\n");
            fflush(stdout);
            break;

        // Compiling

        // Runtime
        default:
            printf("unknown error code\n");
    }
}
