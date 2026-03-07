# Program to generate Fibonacci sequence
terms = int(input("How many terms do you want in the Fibonacci sequence? "))

# First two terms
a, b = 0, 1
count = 0

if terms <= 0:
    print("Please enter a positive integer.")
elif terms == 1:
    print("Fibonacci sequence up to", terms, "term:")
    print(a)
else:
    print("Fibonacci sequence:")
    while count < terms:
        print(a)
        nth = a + b
        # Update values
        a, b = b, nth
        count += 1