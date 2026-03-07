# Count to n and print each number
n = int(input("Enter the value of n: "))
def count_to_n(x = n):
for i in range(1, x + 1):
print(i, end=' ')
print()

print("Going to count to {} ... ".format(n))
count_to_n(n)
#-
print("first modification for 2nd commit")
print("Modification for the 4th commit")

print("Added to see checkout is safe")
<<<<<<< HEAD
print("added this line from techteam main branch for rebase")
=======
print("Message to check .gitignore file")
print("added this file from web github")
print("first line from techteam branch from github web")
print("second line from techteam1 brach from github web")
>>>>>>> 3d518802e4ea2394573bdb274a88085247fd1dce
