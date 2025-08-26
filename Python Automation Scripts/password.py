import random
import string

lenght = int(input("Enter lenght:").strip())

 
chars = string.ascii_letters
chars +=string.digits
chars +=string.punctuation


password = ""

for i in range(lenght):
    character = random.choice(chars)
    password +=character

print("Your password is :", password)    