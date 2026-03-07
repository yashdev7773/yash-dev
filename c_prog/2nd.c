#include<stdio.h>

int main() {
    int n[10]; // Declare n as an array of 10 ints
    int i, j;

    for (i = 0; i < 10; i++) {
        n[i] = i + 10;
    }

    for (j = 0; j < 10; j++) {
        printf("Element [%d] = %d\n", j, n[j]);
    }

    return 0;
}