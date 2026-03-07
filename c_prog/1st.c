#include <stdio.h>

int main ()
{
    FILE *filePointer;
        
    filePointer = fopen ("example.txt", "w");

    if(filePointer == NULL){
        printf("Error creating file!");

    }
    fprintf(filePointer, "Hello, this is a c programming file");
    
    fclose(filePointer);
    printf("File created successfully. \n");

    return 0 ;
}