#include <stdio.h>

struct Person 
{
    char name[50];
    int age;
    float salary;
};
int main()
{
    struct Person person1 = {"Komal", 30, 50000.50};
    
    printf("Name: %d\n", person1.name);
    printf("Age: %d\n", person1.age);
    printf("salary: %.2f\n", person1.salary);
    
    return 0;
    
}