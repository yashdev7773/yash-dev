#include<stdio.h>
int main()
{
// sum of digits in a given number
// product of digits in a given number
     int n,d,sum=0, prod=1;
     printf("Enter value of n :\n");
     scanf("%d" ,&n);
     while(n>0)
     {
        d = n%10;
        sum = sum+d;
        prod = prod*d;
        n = n/10;
     }
     printf("Sum of digits is : %d\n" ,sum); 
     printf("Product of digits is : %d\n" ,prod);    
}
