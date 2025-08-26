import mysql.connector as sql
import colorama,re
import datetime as dt
import time as tim
import pygame
# from playsound import playsound  
# mycon = sql.connect(host="127.0.0.1",user="root",passwd="")
mycon=sql.connect(host="127.0.0.1",user="root",passwd="",database="clock")
mycursor=mycon.cursor()

# mycursor.execute("CREATE DATABASE clock")
# mycursor.execute("CREATE TABLE clock(id INT(4) AUTO_INCREMENT PRIMARY KEY,fullname VARCHAR(50),password VARCHAR(50),email VARCHAR(50),date VARCHAR(50))")
# mycursor.execute("ALTER TABLE clock ADD(username VARCHAR(50))")
# mycursor.execute("ALTER TABLE clock ADD(email VARCHAR(50) UNIQUE,username VARCHAR(50) UNIQUE)")
class clock():
    def __init__(self) :
        colorama.init()
        self.home()

    def home(self):
        print(colorama.Fore.BLUE+"~~~~~~~~~~~~~".center(100))
        print(colorama.Fore.BLUE+"DIGITAL CLOCK".center(100))
        print(colorama.Fore.BLUE+"~~~~~~~~~~~~~".center(100))
        print(colorama.Fore.RESET)
        print("1.Sign Up\n2.Login\n3.Log Out")
        user = input("Enter option:")
        if user == "1":
            self.sign()
        elif user == "2":
            self.login()
        elif user == "3":
            exit()
        else:
            print("Input number from number 1-3\nTo create account(1)\nTo login(2)\nLog Out(3)")

    def sign(self):
        print(colorama.Fore.GREEN+"~~~~~~~".center(70))
        print(colorama.Fore.GREEN+"SIGN UP".center(70))
        print(colorama.Fore.GREEN+"~~~~~~~".center(70)) 
        print(colorama.Fore.RESET) 
        print(colorama.Fore.RED+"YOU'RE ABOUT TO CREATE AN ACCOUNT WITH US")
        print(colorama.Fore.RESET)  
        fullname=input("Fullname:").strip().lower()
        username=input("Username:").strip().lower()
        email = input("Email:").strip().lower()
        password= input("Password:").strip().lower()
        time = dt.datetime.now()
        print(time)
        pattern=r'^\w+@\w+\.\w+$'
        matches = re.match(pattern,email)
        # print(matches)
        if matches:
            print("You've successfully create an account with us")
        else:
            print("Invalid email")
        query="INSERT INTO clock(fullname,password,email,date,username) VALUES(%s,%s,%s,%s,%s)"
        value =(fullname,password,email,time,username)
        mycursor.execute(query,value)
        mycon.commit()
        print(mycursor.rowcount,"record inserted") 

     

    def login(self):
        print(colorama.Fore.GREEN+"You're about to login into your account")
        print(colorama.Fore.RESET)
        username=input("Username:").strip().lower()
        password= input("Password:").strip().lower()
        query="SELECT * FROM clock WHERE username=%s and password=%s"
        value=(username,password)
        mycursor.execute(query,value)
        output = mycursor.fetchall()
        print(output)
        if output:
            print("1.Time\n2.Date\n3.Day,Hour,Month,Year\n4.Alarm\n5.Exit")  
        else:
            print("Invalid input")      
        option=input("Option:")    
        if option == "1":
            self.time()
        elif option =="2":
            self.date()
        elif option =="3":
            self.day()
        elif option == "4":
            self.alarm()
        elif option =="5":
            self.login()

    def time(self):
        string =tim.strftime("%H:%M:%S %p")
        print(string)
        exit()   
   
    def date(self):
        dte=dt.datetime.now()
        print(dte.date())  
    
    def day(self): 
        fet=dt.datetime.now()
        print(f"Today is :{fet.day}")  
        print(f"We're in the {fet.month} month")
        print(f"We're in {fet.year}") 
    
    def alarm(self):
        pygame.init()
        alarm_hour = int(input("Enter Hour:"))
        alarm_minute = int(input("Enter minute:"))
        alarm_time = input("am/pm:")
        if alarm_time =="pm":
            alarm_hour +=12
        while True:
           if alarm_hour == dt.datetime.now().hour and alarm_minute == dt.datetime.now().minute:
                file = print("1.Fine\n2.Ugly\n3.Beauty\n4.Handsome\n5.Joggle")
                fole="Alarm.mp3"
                fle="Alarm1 (1).mp3"
                ugly="Alarm1 (2).mp3"
                hands="Alarm1 (3).mp3"
                Jogg="Alarm1 (4).mp3"

                option = input("Option:")
                if option == "1":
                    pygame.mixer.music.load(fole)
                    pygame.mixer.music.play()
                    # tim.sleep(60)
                    pygame.mixer.music.stop()
                    pygame.quit()
                    self.login()
                
                elif option == "2":
                    pygame.mixer.music.load(fle)
                    pygame.mixer.music.play()
                    # tim.sleep(60)
                    pygame.mixer.music.stop()
                    pygame.quit()
                    self.login()    
                
                elif option == "3":
                    pygame.mixer.music.load(ugly)
                    pygame.mixer.music.play()
                    # tim.sleep(60)
                    pygame.mixer.music.stop()
                    pygame.quit()
                    self.login() 
                
                elif option == "4":
                    pygame.mixer.music.load(hands)
                    pygame.mixer.music.play()
                    # tim.sleep(60)
                    pygame.mixer.music.stop()
                    pygame.quit()
                    self.login() 
                
                elif option == "5":
                    pygame.mixer.music.load(Jogg)
                    pygame.mixer.music.play()
                    # tim.sleep(60)
                    pygame.mixer.music.stop()
                    pygame.quit()
                    self.login()      
   
agogo = clock()



 