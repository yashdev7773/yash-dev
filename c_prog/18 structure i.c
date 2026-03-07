#include<stdio.h>

#include <string.h>

struct Person
{
    char name[50];
    int age;
    float height;
};

int main()
{
    struct Person Person1;

    strcpy(Person1.name, "Smith");
    Person1.age = 27;
    Person1.height = 5.9;

    printf("Person Information:\n");
    printf("Name: %s\n", Person1.name);
    printf("Age: %d\n", Person1.age);
    printf("Height: %.2f\n", Person1.height);

    return 0;
}