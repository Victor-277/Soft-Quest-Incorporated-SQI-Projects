import mysql.connector as sql
import random
import time 
import colorama,re
import datetime as dt
import secrets
import string

mycon = sql.connect(host = "localhost", user = "root" , passwd = "", database="cbt")

mycursor = mycon.cursor()

# mycursor.execute("CREATE DATABASE cbt") 
# mycursor.execute("CREATE TABLE customer(id INT(4) AUTO_INCREMENT PRIMARY KEY,fullname VARCHAR(50),email VARCHAR(255) UNIQUE,password VARCHAR(50) UNIQUE,registrationNumber VARCHAR(50),date VARCHAR(50),score VARCHAR(50))")



class cbt:
    def __init__(self)  :
        self.home()
        self.generate_password()
        self.reg = random.randint(0000000000,999999999)
    def home(self):
        colorama.init()
        print(colorama.Fore.GREEN+"GOD'S GRACE CBT".center(100,"~"))
        print(colorama.Fore.RESET)
        print("1.Sign Up\n2.Login\n3.Maximum score")
        option = int(input("Option:").strip())
        if option == 1:
            print("Have you registered with us?\n1.Yes\n2.No")
            choice = int(input("Option:").strip())
            if choice == 1:
                self.login()
            elif choice == 2:
                self.sign()
            else:
                print("Invalid input\nPlease try again later")
                time.sleep(5)
                self.home()
        elif option == 2:
            self.login() 
        elif option == 3:
                self.max()
        else :
            print("Invalid input\nPlease try again later")
            time.sleep(5)
            self.home() 
        
 

    def generate_password(self, length=12):
            characters = string.digits
            password = ''.join(secrets.choice(characters) for _ in range(length))
            return password
    
        
    def sign(self):
            self.reg= random.randint(0000000000,999999999)
            print("You're about to register with us ...")
            fullname = input("Fullname:").strip().lower()
            email =  input("Email:").strip().lower()      
            password = self.generate_password()
            print(password) 
            score=0
            # reg_no =(self.reg)
            # print(reg_no)
            dat = dt.datetime.now()
            date = dat 
            print(date)
            pattern=r'^\w+@\w+\.\w+$'
            matches = re.match(pattern,email)
            print(matches)
            if matches:
                 print(f"You've successfully registered with us\nHere is your registration number:{self.reg}")
            else:
              print("Invalid email")
            query="INSERT INTO customer(fullname,email,password,registrationNumber,date,score) VALUE(%s,%s,%s,%s,%s,%s)"
            value = (fullname,email,password,self.reg,date,score)
            mycursor.execute(query,value)
            mycon.commit()
            print(mycursor.rowcount,"row added")
            self.login()
            
    def login(self):
        print("YOU'RE ABOUT TO LOGIN")
        password = int(input("Your password:").strip())
        reg = int(input("Registration number:".strip()))
        query = "SELECT * FROM customer WHERE password = %s and registrationNumber = %s"
        value= (password,reg)
        mycursor.execute(query,value)
        details = mycursor.fetchall()
        # account = details[0][4]
        # print(details)      
        if details:
        
         

    
         questions = [
             
            ("a","1.Which player scored the fastest hat-trick in the Premier League?\na)Sadio Mane\nb)Thierry Henry\nc)Cristiano Ronaldo\nd)Patrick Vieira"),
             
            ("c","2.Which player, with 653 games, has made the most Premier League appearances\na)Sergio Aguero\nb)John Terry\nc)Gareth Barry\nd)Ryan Giggs"),
            
            ("a","3.Three players share the record for most Premier League red cards (8). Who are they?\na)Patrick Vieira, Richard Dunne and Duncan Ferguson\nb)John Terry,Peter Schmeichel and Nemanja Vidic\nc)Rio Ferdinand,Steven Gerrard and Ashley Cole\nd Dennis Bergkamp ,Paul Scholes and Eric Cantona"),

            ("d","4.With 260 goals, who is the Premier League's all-time top scorer?\na)Didier Drogba\nb)Erling Haaland\nc)Lionel Messi\nd)Alan Shearer"),

            ("c","5.When was the inaugural Premier League season?\na)2022-2023\nb)1940-1941\nc)1992-93\nd)1991-1992"),

            ("a","6. Which team won the first Premier League title?\na) Manchester United\nb)Liverpool\nc)Arsenal\nd)Manchester City"),

            ("a","7.With 202 clean sheets, which goalkeeper has the best record in the Premier League?\na)Petr Cech \nb)Thibaut Courtois\nc)David De Gea\nd)Peter Schmeichel"),

            ("c","8.How many clubs competed in the inaugural Premier League season?\na)20\nb)15\nc)22\nd)32"),

            ("b","9.Which three players shared the Premier League Golden Boot in 2018-19?\na)Pierre-Emerick Aubameyang,Eden Hazard and Sadio Mane\nb)Pierre-Emerick Aubameyang, Mohamed Salah and Sadio Mane\nc)Eden Hazard ,Pierre-Emerick Aubameyang and Mohamed Salah\nd)Julian Alvarez ,Mohamed Salah and Sadio Mane"),

            ("a","10.The fastest goal scored in Premier League history came in 7.69 seconds. Who scored it?\na)Shane Long\nb)Cristiano Ronaldo\nc)Roy Keane\nd)Thierry Henry"),

            ("c","11. There have been two World Cup trophies. What was the name of the first?\na)FIFA World Cup Trophy\nb)Golden cup\nc)Jules Rimet Trophy\nd)Victory Trophy"),

            ("a","12.Which country won the first ever World Cup in 1930?\na) Uruguay\nb)Brazil\nc) Germany\nd) Italy"),
            
            ("b","13.Which country has won the most World Cups?\na)Germany\nb)Brazil\nc) Argentina\nd)Italy"),

            ("c","14.Three countries have won the World Cup twice. Can you name them?\na)Italy,Portugal,Argentina\nb)France,Portugal,Argentina\nc)Argentina, France and Uruguay\nd)Italy,Portugal,France"),

            ("a","15.Which country has appeared in three World Cup finals, but never won the competition?\na)Netherlands\nb)Germany\nc)Brazil\nd)Argentina"),

            ("a","16.The 2026 World Cup will be hosted across three different countries. Can you name them?\na)United States, Canada and Mexico\nb)Italy, Switzerland, Austria\nc)France, Germany, Spain\nd)Brazil, Argentina, Chile"),

            ("c","17.In which World Cup did Diego Maradona score his infamous 'Hand of God' goal?\na) 1982\nb)1994\nc)1986\nd)1990"),

            ("b","18.The record number of World Cup goals is 16, scored by who?\na)Just Fontaine \nb)Miroslav Klose\nc)Gerd Muller\nd)Sándor Kocsis"),

            ("a","19. Three people have won the World Cup as a player and as a coach. Mario Zagallo, Didier Deschamps and... can you name the third?\na)Franz Beckenbauer\nb) Pelé\nc)Zinedine Zidane\nd)Johan Cruyff"),

            ("c","20.Two English players have won the World Cup Golden Boot. Who are they?\na)Bobby Charlton and Michael Owen\nb)Alan Shearer and Wayne Rooney\nc)Gary Lineker (1986) and Harry Kane (2018)\nd) Frank Lampard and Steven Gerrard"),

         ]
   
     
         score = 0

         for ans,question in questions:
             print(question)
             candidate = input("Your answer: ")

             if candidate  == ans:
                score += 1

         print(f'Dear candidate, this is your score: {score} out of {len(questions)}')

         que = "SELECT * FROM customer WHERE registrationNumber = %s and password = %s"
         val = (reg,password)
         mycursor.execute(que,val)
         result  = mycursor.fetchall()
        #  print(result)
         scores = result[0][6]
         balance = int(scores)+int(score)
         query = "UPDATE customer SET score=%s WHERE registrationNumber = %s"
         val = (balance, reg)
         mycursor.execute(query,val)
         mycon.commit()
         print(f"Your score is {score}")
            
        else:
            print("Invalid input")
            time.sleep(3)
            self.login() 
    def max(self):
        mycursor.execute("SELECT fullname, MAX(score) FROM customer;")
        result = mycursor.fetchone()
         
        if result:
           fullname, score = result
           print(f"The maximum score is {score} for {fullname}.")
        else:
            print("No records found.")
 
 
ques = cbt()    
 


 