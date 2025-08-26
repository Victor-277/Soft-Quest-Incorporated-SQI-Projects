import random
import colorama

class Fixture:
    def __init__(self):        
        colorama.init()
        self.teams = []
        self.login()
        self.welcome()
        self.add()
        
    def login(self):
        print("Do you have an account with us?\n1.Yes \n2.No")    
        login = input("Input the number:").strip()
        if login == '1':
             
            self.welcome()
        elif login == '2':
            
            self.login()
        else:
            print("Input the correct number")
            self.login()

    def welcome(self):
        colorama.init()
        print(colorama.Fore.GREEN + " WELCOME TO GRACE LEAGUE APP ".center(100, "<"))
        print(colorama.Fore.RESET)

    def add(self):
        print("Input your teams here")
        while True:
            team = input("Enter team name (or type 'done' to finish): ").strip()
            if team.lower() == 'done':
                break
            elif team:
                self.teams.append(team)
            else:
                print("Team name cannot be empty. Please try again.")
        self.display_teams()

    def display_teams(self):
        if self.teams:
            print("\nTeams in the league:")
         
            for idx, team in enumerate(self.teams, 1):
                print(f"{idx}. {team}")
            self.generate_fixtures()
        else:
            print("No teams added")

    def generate_fixtures(self):
        if len(self.teams) % 2 != 0:
            self.teams.append("Bye")  

        random.shuffle(self.teams)

        print("\nGenerated Fixtures:")
        for i in range(0, len(self.teams), 2):
            print(f"{self.teams[i]} vs {self.teams[i + 1]}")
fix = Fixture()


 