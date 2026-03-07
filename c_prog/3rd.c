#include<stdio.h>

int main()
{
    int WeeklyTemperatures[7] = {
        25,
        28,
        30,
        26,
        27,
        29,
        31
    };

    for (int day = 0; day < 7; day++) {
        printf("Day %d Temperature: %d\n", day + 1, WeeklyTemperatures[day]);

    }
    return 0;
}