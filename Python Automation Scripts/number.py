import random

nu = 1
nb = 1000
gussess = 0
number = random.randint(nu,nb)

while True:
    guess = int(input(f"Enter number:"))
    gussess +=1
    if guess < number:
        print(f"{guess} is too low")
    elif guess > number:
        print(f"{guess} is too high")
    else:
        print(f"{guess} is correct")
        break

print(f"This round took you {gussess}")