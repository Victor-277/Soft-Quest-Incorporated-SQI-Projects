import mysql.connector as sql
import random,colorama,datetime,re,time

mycon = sql.connect(host = "localhost", user ="root", passwd ="", database ="register")
mycursor = mycon.cursor()

# mycursor.execute("CREATE DATABASE register")
# mycursor.execute("CREATE TABLE register (id INT(4) PRIMARY KEY AUTO_INCREMENT,fullname VARCHAR(255),age VARCHAR(255) ,date VARCHAR(255),userID VARCHAR(255),email VARCHAR(255) UNIQUE)")
# mycursor.execute("ALTER TABLE register ADD password VARCHAR(50)")



mycursor = mycon.cursor()

class Register():
    def __init__(self) -> None:
        colorama.init()
        self.landing_page()
    def landing_page(self):
        number =random.randint(1,100)
        print(colorama.Fore.BLUE+"You're about to register for TEEN program")
        print("1.Register\n2.Details")
        option = int(input("option:").strip())
        if option == 1:
            self.register()
        elif option == 2:
            self.details()
        else:
            print("Invalid input")

    def register(self): 
        number =random.randint(1,100)   
        print(colorama.Fore.BLUE+"You're about to register for TEEN program")
        fullname = input("Fullname:").strip().lower()
        Age = int(input(" Age:").strip())
        dat =datetime.datetime.now() 
        date = dat.date()   
        # print(date)
        userID = number
        email = input("Email:").strip().lower()
        password = int(input("Password (4-digit):").strip())
        pattern=r'^\w+@\w+\.\w+$'
        matches = re.match(pattern,email)
        # print(matches)
        if matches:
            print("Processing ...")
            time.sleep(2)
            if (int(Age) > 13) and  (int(Age)<= 18):
                print("You've successfully registered")
                print(fullname,",this is your user ID",userID)
        
            else:
                print(fullname,"You are too old\nThe program is for teen")
        else:
            print("Invalid email")
        query = "INSERT INTO register(fullname,age,date,userID,email,password) VALUE(%s,%s,%s,%s,%s,%s)"
        value =(fullname,Age,date,userID,email,password)
        mycursor.execute(query,value)
        mycon.commit()
        print(mycursor.rowcount,"row added")    

    def details(self):
        email= input("Input your email:").strip()
        password = int(input("Your password:").strip())
        q = "SELECT * FROM register WHERE email=%s and password=%s "
        v = (email,password)
        mycursor.execute(q,v)
        result = mycursor.fetchone()
        if result:
            # print("Your id = ",result[0] )
            print("Your name = ",result[1])
            print("Your age = ",result[2])
            print("The date you registered = ",result[3])
            print("Your ID= ",result[4])
            print("The date you email = ",result[5])
        

        


        
                





program = Register()    