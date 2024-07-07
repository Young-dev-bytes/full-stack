#!/usr/bin/python
for step in range(6):
    print("hello")
for number in range(1, 101):
    if number % 3 == 0 and number % 5 == 0:
        print("FizzBuzz")
    elif number % 3 == 0:
        print("Fizz") 
    elif number % 5 == 0:
        print("Buzz")
    else:    
        print(number)  

# func blocks: 4 indentation
def my_func():
    if number % 3 == 0 and number % 5 == 0:
        print("FizzBuzz")
    elif number % 3 == 0:
        print("Fizz") 
    elif number % 5 == 0:
        print("Buzz")
    else:    
        print(number)  
    print("hello") 

   
