#include<stdio.h>

int main()
{
    for (int cont = 1; cont <= 10; cont++){ // Removed semicolon
        if(cont == 5){
            printf("Breaking out at 5!\n");
            break;
        }
        printf("Count: %d\n", cont); // Corrected variable name
    }
    return 0;
}