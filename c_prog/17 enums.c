#include<stdio.h>

enum Color
{
    RED,
    GREEN,
    BLUE,
};
int main()
{
    enum Color ChosenColor;
    
    ChosenColor = GREEN;
    
    switch(ChosenColor)
    {
        case RED:
            printf("You chose Red.\n");
            break;
        case GREEN:
            printf("You chose Green.\n");
            break;
        case BLUE:
            printf("You chose Blue.\n");
            break;
            
        default:
            printf("Invalid color choice.\n");
    }
    return 0;
}