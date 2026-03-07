#include<stdio.h>

int addNumbers(int a, int b);
int main()
{
    int result;
    result = addNumbers(10,20);
    printf("The sum is: %d\n", result);
    return 0;
}

addNumbers(int a, int b)
{
    return a + b;
}
