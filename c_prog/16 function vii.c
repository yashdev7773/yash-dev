#include <stdio.h>

int factorial(int n); // Function declaration

int main()
{
    int num = 5;
    printf("Factorial of %d is %d\n", num, factorial(num));
    return 0;
}

int factorial (int n)
{
    if (n == 0) {
        return 1;
    } else {
        // The error is here: 'Factorial' should be 'factorial'
        return n * factorial (n - 1); 
    }
}