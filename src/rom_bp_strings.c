#include <stdint.h>
#include <stdio.h>

const int rom_11_capacity = 2048;
const char *rom_11_bit = "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";

// Sets dest to the placeholder string for the ith element in the json of the blueprint
int rom_11_placeholder(char dest[8], int i)
{
    sprintf(dest, "%d", 0xFF000000 + i);
    return 0;
}

// Returns the index of the placeholder if valid, or -1 of not
int64_t is_rom_11_placeholder(int placeholder)
{
    if ((placeholder & 0xFF000000) == 0)
        return -1;

    if ((placeholder & 0x00FFFFFF) < rom_11_capacity)
        return placeholder & 0x00FFFFFF;
    return -1;
}