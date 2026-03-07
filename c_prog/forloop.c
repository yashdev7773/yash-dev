// For loop to compute factorial of given number
#include<stdio.h>
int main()
{
    int n,i=1,fact=1;
    printf("Enter value of n : \n");
    scanf("%d", &n);
//for(i=1;i<=n;i++)
    while(i<=n)
    {
        fact = fact*i;
        i++;
    }
    printf("Factorial result is : %d\n" , fact);
}

