#Program to calculate the factorial of a number
number = int(input("Enter a Positive number: "))
factorial = 1
if number < 0:
    print("Sorry, factorial does not exist for negative number.")
elif number == 0:
    print("The factorial of 0 is 1.")
else:
    for i in range(1, number +1):
        factorial *= i
    print("The factorial of", number, "is", factorial)
