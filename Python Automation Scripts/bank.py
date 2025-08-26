import mysql.connector as sql
import random
import time 
import colorama,re
import datetime as dt

mycon = sql.connect(host = "localhost", user = "root" , passwd = "", database = "bank")

mycursor = mycon.cursor()

# mycursor.execute("CREATE DATABASE bank") 
# mycursor.execute("CREATE TABLE customer(id INT(4) AUTO_INCREMENT PRIMARY KEY,fullname VARCHAR(255),email VARCHAR(255) UNIQUE,password VARCHAR(255) UNIQUE,accountNumber VARCHAR(255),date VARCHAR(255),accountBalance VARCHAR(255))")
 



 

class Bank():
    def __init__(self) :
        self.home()
        self.account = random.randint(0000000000,999999999)
    def home(self):
        colorama.init()
        # self.account = random.randint(0000000000,999999999)
        print(colorama.Fore.GREEN+"WELCOME TO GOD'S GRACE BANK".center(100,"~"))
        # print(colorama.Fore.RESET)
        print("1.Sign Up\n2.Login")
        option = int(input("Option:").strip())
        if option == 1:
            print("Do you have an account with us?\n1.Yes\n2.No")
            choice = int(input("Option:").strip())
            if choice == 1:
                self.login()
            elif choice == 2:
                # self.account = random.randint(0000000000,999999999)
                self.sign()
            else:
                print("Invalid input\nPlease try again later")
                time.sleep(5)
                self.home()
        elif option == 2:
            self.login() 
        else :
            print("Invalid input\nPlease try again later")
            time.sleep(5)
            self.home() 

    def sign(self):
        self.account = random.randint(0000000000,999999999)
        print("You're about to create an account with us ...")
        fullname = input("Fullname:").strip().lower()
        email =  input("Email:").strip().lower()      
        password = int(input("Enter your 4-digit pin:".strip()))
        accountbal=0
        # account_no =(self.account)
        # print(account_no)
        dat = dt.datetime.now()
        date = dat 
        print(date)
        pattern=r'^\w+@\w+\.\w+$'
        matches = re.match(pattern,email)
        # print(matches)
        if matches:
             print(f"You've successfully create an account with us\nHere is your account number:{self.account}")
        else:
            print("Invalid email")
        query="INSERT INTO customer(fullname,email,password,accountNumber,date,accountBalance) VALUE(%s,%s,%s,%s,%s,%s)"
        value = (fullname,email,password,self.account,date,accountbal)
        mycursor.execute(query,value)
        mycon.commit()
        print(mycursor.rowcount,"row added")
        self.home()

    def login(self):
        print("YOU'RE ABOUT TO LOGIN")
        password = int(input("Your 4-digits pin:").strip())
        accoun = int(input("Account number:".strip()))
        query = "SELECT * FROM customer WHERE password = %s and accountNumber = %s"
        value= (password,accoun)
        mycursor.execute(query,value)
        details = mycursor.fetchall()
        # account = details[0][4]
        print(details)      
        if details:
            print("1.Deposit\n2.Withdraw\n3.CheckBalance\n4.Transfer\n5.Close account\n6.Details\n7.Recharge\n8.Exit")
            option = int(input("Option:").strip())
            if option == 1:
                self.deposit()
            elif option == 2:
                self.withdraw()
            elif option == 3:
                self.balance() 
            elif option == 4:
                self.transfer() 
            elif option == 5:
                self.close() 
            elif option == 6:
                self.detail()
            elif option == 7:
                  self.recharge()
            elif option == 8:
                exit()
            else:
                print("Input numbers from 1-7")
                time.sleep(3)
                self.login() 

    def deposit(self):
        print("YOU'RE ABOUT TO DEPOSIT")
        deposit = int(input("Enter the amount you wish to deposit:"))
        account_no = input("Your account_no:")
        password = int(input("Your 4-digits pin:").strip())
        que = "SELECT * FROM customer WHERE accountNumber = %s and password = %s"
        val = (account_no,password)
        mycursor.execute(que,val)
        result  = mycursor.fetchall()
        print(result)
        account_balance = result[0][6]
        balance = int(account_balance)+int(deposit)
        query = "UPDATE customer SET accountBalance=%s WHERE accountNumber = %s"
        val = (balance, account_no)
        mycursor.execute(query,val)
        mycon.commit()
        print(f"You've successfully deposited #{deposit}\nThanks for banking with us")
        # print("You now have",result[0][6])

    def withdraw(self) :
        print("You're about to withdraw") 
        withdraw = int(input("Enter the amount you wish to withdraw:").strip()) 
        account = input("Input your account number:")
        password =int(input("Input your 4 digit pin:").strip())
        q="SELECT * FROM customer WHERE accountNumber = %s and password = %s"
        v = (account,password)
        mycursor.execute(q,v)
        result = mycursor.fetchall()
        print(result)
        accountbal=result[0][6]
        if int(accountbal) > int(withdraw):
            balance = int(accountbal) - int(withdraw)
            query = "UPDATE customer SET accountBalance = %s WHERE accountNumber = %s"
            value = (balance,account)
            mycursor.execute(query,value)
            mycon.commit()
            print(f"Dear customer, your withdrawal of {withdraw} is successful")
        else:
            print("Insufficient balance\nTry and fund your account") 

    def balance(self):
        print("You're about to check your balance")
        account = input("Enter your account number:").strip()
        password =int(input("Input your 4 digit pin:").strip())
        p = "SELECT * FROM customer WHERE accountNumber = %s and password=%s"
        q = (account,password)
        mycursor.execute(p,q)
        result = mycursor.fetchall()
        accountbal=result[0][6]
        print("Dear customer, this is your account balance",accountbal)
    
    def transfer(self):
        print("You're about to transfer")
        account = input("Your account number:").strip()
        password = int(input("Your password:").strip())
        q = "SELECT * FROM customer WHERE accountNumber=%s and password=%s"
        v = (account,password)
        mycursor.execute(q,v)
        result = mycursor.fetchall()
        accountbal = result[0][6]
        if result:
            amount = int(input("Input the amount you wish to transfer:").strip())
            if int(accountbal) > int(amount):
                total = int(accountbal)-int(amount)
                quey = "UPDATE customer SET accountBalance = %s WHERE accountNumber = %s"
                vale = (total,account)
                mycursor.execute(quey,vale)
                mycon.commit
                numb = int(input("Enter reciever's account number:").strip()) 
                name  = input("Input reciver's account name:").strip().lower()
                query = "SELECT * FROM customer WHERE accountNumber = %s and fullname = %s"
                val = (numb,name)
                mycursor.execute(query,val)
                resut = mycursor.fetchall()
                accout = resut[0][6]
                print(resut)
                if resut:
                    tital  = int(accout) +int(amount)
                    qury = "UPDATE customer SET accountBalance = %s WHERE accountNumber = %s"
                    value = (tital,numb)
                    mycursor.execute(qury,value)
                    mycon.commit()
                    print(f"Dear customer,you've successfully transfer {amount} to {numb} and your balance is", total)
                else:
                    print("Invalid input")    
            else:
                print("Insufficient funds\nPlease fund your account")
        else:
            print("Invalid inputs\nPlease try again later")
            self.login()
    
    def close(self):
       print("You're about to delete your account")
       account = input("Enter your account number:")
       password = int(input("Your password:").strip())
       q = "SELECT * FROM customer WHERE accountNumber=%s and password=%s"
       v = (account,password)
       mycursor.execute(q,v)
       result = mycursor.fetchone()
       if result:
            print("These are your details".center(50,"`"))
            # print("Your id = ",result[0] )
            print("Your name = ",result[1])
            print("Your email = ",result[2])
            print("Your password= ",result[3])
            print("Your account number= ",result[4])
            print("The date you registered = ",result[5])
            print("Your account balance = ",result[6])
            print("Are you sure you want close your account")
            print("1.YES\n2.NO")
            option = int(input("Option:").strip())
            if option == 1:
                print(colorama.Fore.RED+"You're about to delete your account")
                account = int(input("Enter your account number:").strip())
                password = int(input("Your password:").strip())
                print(colorama.Fore.RESET)
                delete = "DELETE FROM customer WHERE accountNumber=%s and password =%s"
                value = (account,password)
                mycursor.execute(delete,value)
                
                
                print(f"Dear customer you've successfully delete {account} account\nThank you for banking with us")
                
            elif option == 2:
                self.login()
            else:
                print("Input number from number 1-2\n Try again later")
                    
    


    def detail(self):
        account = input("Your account number:").strip()
        password = int(input("Your password:").strip())
        q = "SELECT * FROM customer WHERE accountNumber=%s and password=%s"
        v = (account,password)
        mycursor.execute(q,v)
        result = mycursor.fetchone()
        if result:
            # print("Your id = ",result[0] )
            print("Your name = ",result[1])
            print("Your email = ",result[2])
            print("Your password= ",result[3])
            print("Your account number= ",result[4])
            print("The date you registered = ",result[5])
            print("Your account balance = ",result[6])

    def recharge(self):
        print("You're about to recharge")
        account = input("Enter account number:").strip()
        password = int(input("Your password:").strip())
        q="SELECT * FROM customer WHERE accountNumber=%s and password=%s"
        v=(account,password)
        mycursor.execute(q,v)
        result = mycursor.fetchall()
        accountbal=result[0][6]
        if result:
            recharge = int(input("Enter the reciver phone number:").strip())
            account = input("Enter account number:").strip()
            amount = int(input("Amount:#").strip())
            if int(accountbal) > int(amount):
               total=int(accountbal)-int(amount)
               print("1.MTN\n2.GLO\n3.ETISALAT\n4.AIRTEL")
               option = int(input("Option:").strip())
               if option == 1:
                   print(f"Dear customer, the recharge of {amount} MTN card was successful\nYur balance is #",total)
               elif option==2:
                   print(f"Dear customer, the recharge of {amount} GLO card was successful\nYour balance is #",total)
               elif option==3:
                   print(f"Dear customer, the recharge of {amount} ETISALAT card was successful\nyour balance is #",total)
               elif option==4:
                   print(f"Dear customer, the recharge of {amount} AIRTEL card was successful\nyour balance is #",total)
               query = "UPDATE customer SET accountBalance = %s WHERE accountNumber = %s"
               value = (total,account)
               mycursor.execute(query,value)
               mycon.commit()
            else:
                   print("Insufficient fund\nPlease fund your wallet")
        else:
            print("Invalid input\nPlease try agian later")       
               
       
            
 

grace = Bank()            



