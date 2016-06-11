#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void reverse_str(char* begin)
{
    char* end = begin + strlen(begin) - 1;
    char swp;
    while (begin < end)
    {
        swp = *end;
        *end-- = *begin;
        *begin++ = swp;
    }
}

int main(int argc, char* argv[])
{
    char* forward = argv[1];
    char* reverse = strdup(forward);
    if (reverse != NULL)
    {
        reverse_str(reverse);

        printf("forward: %s\n", forward);
        printf("reverse: %s\n", reverse);

        free(reverse);
    }
    else
        printf("reversing of string failed due to insufficient memory.\n");

    return 0;
}
