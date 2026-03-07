#include<stdio.h>

int main()
{
    int x = 5, y = 10;

    _Bool isGreater = x > y;
    _Bool isEqual = x == y;
    
    printf(" is x greater than y? %d\n", isGreater);
    printf(" is x equal to y %d\n", isEqual);
    
    return 0;
}