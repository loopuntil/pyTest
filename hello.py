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

#Returns True if a sequence with the specified value is present in the object

x = ["apple", "banana"]
print("banana" in x)

print( not(((3>2) and (1 is 1)) or True) )

thislist = ["apple", "banana", "cherry"]
for x in thislist:
  print(x)

thislist = ["apple", "banana", "cherry"]
if "apple" in thislist:
  print("Yes, 'apple' is in the fruits list")

thislist.append("orange")
print(thislist)

thislist.insert(1, "orange")
print(thislist)

c =thislist.pop()
print(thislist)
print(c)

del thislist[0]
print(thislist)

thislist.clear()
print(thislist)

thislist = ["apple", "banana", "cherry"]
mylist = thislist.copy()
print(mylist)

thislist = list(("a", "b", "c")) # note the double round-brackets
print(thislist)

thisset = {"apple", "banana", "cherry"}

thisset.add("orange")

print(thisset)

thisset = {"apple", "banana", "cherry"}

thisset.update(["orange", "mango", "grapes"])

print(thisset)

thisdict =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

for x, y in thisdict.items():
    print(x, y)


a = 200
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")

print("A") if a > b else print("=") if a == b else print("B")

i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1

print('--------------')

i = 0
while i < 6:
  i += 1 
  if i == 3:
    continue
  print(i)  

print('*******')

for x in range(6):
  print(x)

print('********')

adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]
  
for x in adj:
  for y in fruits:
    print(x, y)

def my_function(country = "Norway"):
  print("I am from " + country)

my_function()
my_function('Taiwan')


def my_function(food):
      for x in food:
        print(x)

fruits = ["apple", "banana", "cherry"]
my_function(fruits)

def fbi(n):
  if(n < 2):
    return n
  return fbi(n-1) + fbi(n-2)

for x in range(5):
  print(fbi(x))

x = lambda a, b : a * b
print(x(5, 6))

def myfunc(n):
      return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11)) 
print(mytripler(11))


class Person:
    def __init__(self, name, age):
      self.name = name
      self.age = age

p1 = Person("John", 36)

print(p1.name)
print(p1.age)


class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)


x = Person("John", "Doe")
x.printname()

class Student(Person):
  pass

x = Student("Mike", "Olsen")
x.printname()


class Student(Person):
    def __init__(self, fname, lname, year):
      super().__init__(fname, lname)
      self.graduationyear = year

    def welcome(self):
      print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)  

x = Student("Mike", "Olsen", 2019)
x.welcome()