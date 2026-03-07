#include<stdio.h>
int main()
{
// sum of digits in a given number
     int n,d,sum=0;
     printf("Enter value of n :\n");
     scanf("%d" ,&n);
     while(n>0)
     {
        d = n%10;
        sum = sum%d;
        n = n/10;
     }
     printf("Sum of digits is : %d\n", sum);     
}