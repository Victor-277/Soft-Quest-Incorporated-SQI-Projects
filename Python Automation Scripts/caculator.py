import time,colorama

class calculator:
      def __init__(self) :
            self.name = "Calculator"
            self.calculator()
      def calculator(self):
            colorama.init()     
            print("Which operation do you want to perform ?".center(50,"~"))
            print("1.Addtion\n2.Mutiplication\n3.Subtraction\n4.Division\n5.Set") 
            user = int(input("Input your Value:"))
            if user == 1:
                  self.addition()
            elif user == 2:
                  self.multiplication()
            elif user == 3:
                  self.subtraction()
            elif user == 4:
                  self.division()
            elif user == 5:
                 self.set()

            else:
                  print("Invalid input\nPlease try again later")

      def addition(self):

            val1 = int(input("Input value 1:").strip())
            val2 = int(input("Input value 2:").strip())
            result = val1 + val2
            time.sleep(2)
            print(colorama.Fore.RED+"This is your result:",result) 
            print(colorama.Fore.RESET)
            time.sleep(2)
            self.calculator()
      def multiplication(self):
            val3= int(input("Input value 1:").strip())
            val4 = int(input("Input value 2:").strip())
            time.sleep(2)
            result  =val3 * val4
            print(colorama.Fore.RED+"This is your result:",result) 
            print(colorama.Fore.RESET)
            time.sleep(2)
            self.calculator() 

      def subtraction(self):
            val5 = int(input("Input value 1:").strip())
            val6 = int(input("Input value 2:").strip())
            time.sleep(2)
            result = val5 - val6
            time.sleep(2)
            print(colorama.Fore.RED+"This is your result:",result) 
            print(colorama.Fore.RESET)
            time.sleep(2)
            self.calculator()

      def division(self):
            val7 = int(input("Input value 1:").strip())
            val8 = int(input("Input value 2:").strip())
            time.sleep(2)
            result = val7 / val8
            time.sleep(2)
            print(colorama.Fore.RED+"This is your result:",result) 
            print(colorama.Fore.RESET)
            time.sleep(2)
            self.calculator()

      def set(self):
            print(colorama.Fore.RED+"Which operation do you want to perform?") 
            print(colorama.Fore.RESET)
            print("1.Union\n2.Intersection\n3.Symmetric Difference")
            option= int(input("option:").strip())
            if option == 1:
                  self.union()
            elif option == 2:
                  self.intersection()
            elif option == 3:
                  self.Difference()
            else:
                  print("Invalid input")

      def union(self):
            print(colorama.Fore.RED+"please avoid the use of comma except if is neccessary")
            print(colorama.Fore.RESET)
            value1 = set(input("Input value 1 :"))
            value2 = set(input("Input value 2 :"))
            value3 =value1.union(value2)
            print(value3)
      def intersection(self):
             print(colorama.Fore.RED+"please avoid the use of comma except if is neccessary")
             print(colorama.Fore.RESET)
             value1 = set(input("Input value 1 :"))
             value2 = set(input("Input value 2 :"))
             value4 =value1.intersection(value2)
             print(value4)
      def Difference(self):
             print(colorama.Fore.RED+"please avoid the use of comma except if is neccessary")
             print(colorama.Fore.RESET) 
             value1 = set(input("Input value 1 :"))
             value2 = set(input("Input value 2 :"))
             value5 = value1.symmetric_difference(value2)
             print(value5)
set = calculator()                   
    

