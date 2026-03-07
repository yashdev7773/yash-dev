#include<stdio.h>

int addNumbers (int a, int b)
{
    return a + b;
}

int main()
{
    int result;
    result = addNumbers(5,7);
    
    printf("The sum is: %d\n", result);
    return 0;
}