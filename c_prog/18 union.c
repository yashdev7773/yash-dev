#include<stdio.h>

union Data {
    int intVal;
    float floatVal;
    char str[20];
};

int main() {
    union Data data;

    // First, use and print the integer member
    data.intVal = 10;
    printf("data.intVal: %d\n", data.intVal);

    // Now, assign to the float member. This overwrites the integer.
    data.floatVal = 220.5;
    // To see the float value, we must access the float member with the correct specifier.
    printf("data.floatVal: %f\n", data.floatVal);
    
    // The following line now attempts to read the memory as an integer again,
    // which will yield a garbage value. It is the logical error.
    printf("data.intVal (after float assignment): %d\n", data.intVal);

    return 0;
}