import random

words=['programming','tiger','cat','lamp','code','camel','cristiano','ronaldo','messi','laptop','isaac','grace','mathematics','english','television','monitor','victor','water','youtube','project','doctor','microscope','etc']
class quote():
    def __init__(self) -> None:
       
        self.guess()

    def guess(self):
        print("Word guessing game".center(100,"."))
        random_word = random.choice(words)
        print("These are the words")
        print(words)
        # print("our random word", random_word)
        user_guesses = ''
        chances = 0
        while True:
             guess = input("Make a guess:").strip().lower()
             chances +=1
             if guess == random_word:
                 print("Correct")
                 break
             else:
                 print("Incorrect\nplease try again")
                 print("You failed\nplease try again later")    
                 
        print(f"This took you {chances} guesses")         
 

clas = quote()            
