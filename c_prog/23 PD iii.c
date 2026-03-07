#include <stdio.h>

#define DEBUG 

int main() {
    #ifdef DEBUG
    printf("Debug mode is ON\n");
    #endif //DEBUG

    #ifndef DEBUG
    printf("Debug mode is OFF\n");
    #endif //DEBUG

    printf("This is a simple program.\n");
    return 0;
}
