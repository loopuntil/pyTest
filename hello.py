#comment
"""
This is a comment
written in 
more than just one line
"""
msg = "Hello World"
print(msg)

x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

a,b=1,2
print(a+b)

print(type(x))

x = 1 # int
y = 2.8 # float
z = 1j # complex

#convert from int to float:
a = float(x)

#convert from float to int:
b = int(y)

#convert from int to complex:
c = complex(x)

print(a)
print(b)
print(c)

print(type(a))
print(type(b))
print(type(c))

#Import the random module, and display a random number between 1 and 9:
import random

print(random.randrange(1,10))

#Specify a Variable Type

x = int(1)   # x will be 1
y = int(2.8) # y will be 2
z = int("3") # z will be 3

#Get the character at position 1 

a = "Hello, World!"
print(a[1])

#Substring. Get the characters from position 0 to position 5 (not included):

print(a[0:5])

#The strip() method removes any whitespace from the beginning or the end:
c="a  "
print(c.strip()+"-") # returns "Hello, World!"

#The len() method returns the length of a string:
print("len:"+str(len(a)))

#The lower() method returns the string in lower case:
print(a.lower())

print(a.upper())

print(a.replace("H", "J"))

print(a.split(","))

quantity = 3
itemno = 567
price = 49.95
myorder = "I want {} pieces of item {} for {} dollars."
print(myorder.format(quantity, itemno, price))


