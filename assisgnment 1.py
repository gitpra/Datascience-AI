# Write a Python program to print "Hello, World!y
print("Hello, World")
#&8 Write a Python program that displays your name and age8
name ="ruchika"
age=32
print(f"my name is {name} and my age is {age}")
import keyword
print("paython predefined functions")
print(keyword.kwlist)
# Write a program that checks if a given word is a Python keyword.
import keyword
s = 'for'
if keyword.iskeyword(s):
    print(f"'{s} is a paython keyword")
else:
    print(f"'{s} is not a paython keyword")

#Create a list and tuple in Python, and demonstrate how attempting to change an element works differently for each
my_list=[10,20,30,40]
print(f"'original list: {my_list}")
my_list[2]=15
print(f"'change list: {my_list}")
my_tupple=(100,200,300)
print(f"'original tupple: {my_tupple}")
# my_tupple[3]=150
# print(f"'change tupple:{my_tupple}")


#Write a function to demonstrate the behavior of mutable and immutable arguments.
#mutable objects 

print("demonstrating mutable arguments(list)")
my_list = [1,2,3]
my_list.append(4)
print(my_list)
my_list.insert(2,5)
print(my_list)
my_list.remove(2)
print(my_list)
poped_element =my_list[0]
print("popped_element")


#immuntable 
#my_tupple=(1,2,3,4,5)
#my_tupple.append(6)
#print(my_tupple)


#Write a program that performs basic arithmetic operations on two user-input numbers.

number1= input("enter your first number")
number1 =int(number1)
number2= input("enter your second number")
number2=int(number2)
sum=number1+number2
print("the sum is:",sum)


#Write a program to demonstrate the use of logical operators.
#logical operators are and ,or and not 

# and operator if both condition is true else it is false
x=5;
y=10;
if x>3 and y<15:
    print("both condition is true") #this get printed only 
if x>9 and y<9:
    print("both conditions is false") #its not printed bec its false

# for or operator only one condition is true and its get printed 

a=2
b=8

if a>3 or b<10:
    print("atleast one condition is true ")

#if both conditions ar false it get false
if a>5 or b>12:
 print("this wont be printed")

#for not operator  its used for the reveresed the string 

is_ruchika=True
if not is_ruchika:
    print("it is not ruchika")
else:
    print("It is ruchika") #this get printed 

#Write a Python program to convert user input from string to integer, float, and boolean types.
# convert string to integer
print("---converting  to integer---")
user_input_int_str = input("please enter integer number: ")
try:
 integer_value=int(user_input_int_str)
 print(f"the data type is now integer{(integer_value)}")
except ValueError:
 print(f"Error:'{user_input_int_str}' cannot be converted to integer")
#convert string to float
print("-----converting to float---")
user_input_int_float = input("please enter your float number")
try:
 float_value=float(user_input_int_float)
 print(f"the data type is now float{(float_value)}")
except ValueError:
 print(f"Error:'{user_input_int_float}' cannot be converted to float")

#convert string to boolean types
print("-----converting to boolean---")
user_input__bool_str = input("please enter your 'true' or 'false'")
boolean_value= user_input__bool_str.lower()=='true'
print(f"the input{user_input__bool_str} is now the boolean :{boolean_value}")
print(f"the data type is:{type(boolean_value)} ")


#10. Write code to demonstrate type casting with list elements.
str_numbers = ['1', '2', '3', '4', '5']
int_numbers = [int(x) for x in str_numbers]
print(f"Original list of strings: {str_numbers}")
print(f"New list of integers: {int_numbers}")
print(f"Data type of first element: {type(int_numbers[0])}")
print("-" * 30)

# 11. Write a program that checks if a number is positive, negative, or zero. 
def check_numberstatus():
 try:
    user_input = input("enter your number: ")
    number= float(user_input)
    if(number>0):
      print("your number is positive")
    elif(number<0):
      print("your number is negative")
    else:
     print("the number is zero")
 except ValueError:
    print("enter valid number")

check_numberstatus()
#12. Write a for loop to print numbers from 1 to 10.
for i in range(1,11):
 print(i)

 #13. Write a Python program to find the sum of all even numbers between 1 and 50.
total_sum=0
for i in range(1,50):
   if i % 2==0:
     print(i)
     total_sum +=i
print(f"even number sum for 1 to 50 is:{total_sum}")
# 14. Write a program to reverse a string using a while loop.
def reverse_string_while_loop(input_string):

    reversed_string = ""
    index = len(input_string) - 1  # Start from the last character's index

    while index >= 0:
        reversed_string += input_string[index]
        index -= 1  # Move to the previous character

    return reversed_string


original_string="hello Ruchika"
reverse_string= reverse_string_while_loop(original_string)
print(f"original string:{original_string}")
print(f"reverse string{reverse_string}")

#15. Write a Python program to calculate the factorial of a number provided by the user using a while loop.

try:
    num = int(input("Enter a non-negative integer: "))
except ValueError:
    print("Invalid input. Please enter a valid integer.")
    exit()

if num < 0:
    print("Factorial is not defined for negative numbers.")
elif num == 0:
    print("The factorial of 0 is 1.")
else:
    factorial = 1
    temp_num = num
    
    while temp_num > 0:
        factorial *= temp_num
        temp_num -= 1
    
    print(f"The factorial of {num} is {factorial}.")


""""
Question and answer

1. What is Python, and why is it popular?
paython is interpreter languange and high level programmin g language It is known for the language simplicity
as well as easy to use it has inbuilt library functionality which is easy to use and its open platform so anyone can easily 
access it and used it is platform indepedent also so its quite profitable for large as well as small based company.

2.An interpreter is a program that directly executes code. 
For Python, it's the software that takes your written Python code and runs it. Instead of translating the entire program into machine code all at once (like a compiler), a Python interpreter reads and executes the code line by line. What is an interpreter in Python.
when you run paython interperform this steps lexical analysis and parsing , bytecode compliation and executed by PVM.

3.what are predefined keywords in paython ?
predefined keywords:
True, False, None: Boolean values and a null value.

and, or, not: Logical operators.

if, elif, else: Conditional statements for controlling program flow.

for, while, break, continue: Loops and loop control.

def: Used to define a function.

class: Used to define a class.

import, from: Used to import modules.

try, except, finally: Used for error and exception handling.

4. Can keywords be used as variable names?
No keywords can not be used as variable names in paython 

5.   What is mutability in Python

Mutable objects can be altered in place without creating a new object. When you modify a mutable object, its unique identity (memory address) remains the same.

Examples of mutable data types include:

    list: You can add, remove, or change elements within a list.

dict: You can add, remove, or modify key-value pairs in a dictionary.

set: You can add or remove elements from a set.

6.  Why are lists mutable, but tuples are immutable 
The key difference between lists and tuples in Python is a design choice related to their intended use and underlying implementation. 
Lists are designed to be dynamic and flexible, while tuples are designed for immutability and data integrity.

7. What is the difference between “==” and “is” operators in Python 
The == operator compares the values of two objects. It returns True if the objects have the same content, regardless of whether they are stored at the 
same memory location. This is what you typically use to check if two variables have the same data.

8.what is the logical operator in paython?
paython has three logical operator and or and not 

9.what is the type casting in paython?
Python provides several built-in functions to perform type casting. 
These functions don't change the original variable; instead, they return a new object of the desired type.

10. What is the difference between implicit and explicit type casting
In programming, type casting is the process of converting a variable from one data type to another. The difference between implicit and explicit type casting lies in whether the conversion is performed automatically by the compiler or manually by the programmer.

11.  What is the purpose of conditional statements in Python 
Conditional statements evaluate a boolean expression (an expression that results in either True or False). If the expression is true, the code block indented under the statement is executed. If it's false, that block is skipped, and the program either moves to the next elif (else if) or else statement, or continues with the rest of the code.
The main types of conditional statements in Python are:

    if statement: Executes a block of code only if the condition is True.

    elif statement: An optional part of an if statement, it checks for another condition if the previous if or elif statements were all False.

    else statement: An optional part of an if statement, it executes a block of code if all preceding if and elif conditions were False.



12.  How does the elif statement work 
The elif statement in Python, short for "else if," is used to check multiple conditions 
sequentially after an initial if statement. It's a way to handle multiple outcomes in a single conditional block.

13. What is the difference between for and while loops
The primary difference between for and while loops is how they determine when to stop. A for loop is used for iterating a known number of times, typically over a sequence 
(like a list or string), while a while loop is used for iterating as long as a certain condition is true.

14. Describe a scenario where a while loop is more suitable than a for loop.
A while loop is more suitable than a for loop when you don't know in advance how many times the loop needs to run. The loop's 
termination depends on a condition being met, rather than on iterating through a fixed sequence.

"""