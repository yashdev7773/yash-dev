#include <stdio.h>

int add(int a, int b);

int main()
{
    int result;
    result = add(40, 20);
    printf("The sum is %d\n", result);

    return 0;
}

int add(int a, int b)
{
    return a + b;
}