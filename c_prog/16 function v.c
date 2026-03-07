#include<stdio.h>

int sum (int a, int b)
{
    return a + b;
}

int main ()
{
    int result;

    result = sum(6, 9);

    printf("The sun is: %d\n", result);
    return 0;

}