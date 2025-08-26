import time
import pandas as pd
class market():
    def __init__(self):
          self.landing_page()
    
    def landing_page(self): 
        items = ['Soap', 'Earpod', 'Rice', 'Beans']
        prices = [1000, 25000, 3000, 2000]

        y=1
        time.sleep(1)
        print('\nAvailable items')
        for item,price in zip(items,prices):
             print(f'\n{y} {item}: #{price:}')
             y+=1
        user = int(input("Option:"))
        if user == 1:
            tet=int(input("How many:"))
            total_cost = prices[user - 1] * tet

        elif user == 2:
            tet=int(input("How many:"))
            total_cost = prices[user - 1] * tet

        elif user == 3:
            tet=int(input("How many:"))
            total_cost = prices[user - 1] * tet

        else:
                  print("Invalid input")
        print(f'You are about to purchase {items[user - 1]} which costs #{total_cost}')
     


mar = market()         
 