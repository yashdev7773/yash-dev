#include <stdio.h>

int main()
{
    int arr[5] = {5,10,15};
    int *ptr = arr;
    
    for (int i = 0; i <3; i++)
    {
        printf("Value at arr[%d] using pointer: %d\n", i, *(ptr + i));
        
    }
    return 0;
}