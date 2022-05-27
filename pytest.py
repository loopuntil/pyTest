from collections import deque
import pandas as pd # 引用套件並縮寫為 pd
import numpy as np

queue = deque(["Eric", "John", "Michael"])

queue.append('ken')
print(queue)

table = [x*y for x in range(10)[1:] for y in range(10)[1:]]

print(table)

table = [[x*y for x in range(10)[1:]] for y in range(10)[1:]]


print('**********')
print(table)

'''
當不知道參數個數時
args = 序列元組
kwargs = 字典(關鍵字/值配對)
'''
def student_info(*args, **kwargs):
    print("args = ", args)
    print("kwargs = ", kwargs)

student_info('Math', 'Art', name = 'John', age = '22')

courses = ['Math', 'Art']
info = {'name': 'John', 'age': 22}

'''
可以將原本的courses列表、info字典直接前面加上星號填入函數參數，
這些參數會直接解封(unpacking)填入函數參數列表中
'''

student_info(courses, info)   # 沒加星號
student_info(*courses, **info)   # 有加星號(unpacking)

print('*courses: ', *courses)
print('**info: ', dict(**info))

class MyC:    
    """A simple example class"""    
    i = 12345    
    def f(self):        
        return 'hello world'

x = MyC()

print(x.i)
f = x.f
print(f)

class Dog:
    kind = 'canine'         # class variable shared by all instances
    def __init__(self, name):
        self.name = name    # instance variable unique to each instance


d = Dog('Fido')
e = Dog('Buddy')
d.kind                  # shared by all dogs'canine'
e.kind                  # shared by all dogs'canine'
d.name                  # unique to d'Fido'
e.name                  # unique to e'Buddy'

class Person:
    def __init__(self, name, gender, height, weight, birthday):
        self.name = name
        self.gender = gender
        self.__height = height
        self.__weight = weight
        self.birthday = birthday

    def get_BMI(self):
        return (self.__weight/ ((self.__height/100)**2))


p1 = Person("Peter", "male", 180.0, 70.0, "1987/8/7")


print(p1.get_BMI())


class Car:
    def __init__(self, wheel_number, door_number, power):
        self.wheel_number = wheel_number
        self.door_number = door_number
        self.power = power

class EletricCar(Car):
    def __init__(self, wheel_number, door_number, power, brand):
        super(EletricCar, self).__init__(wheel_number, door_number, power)
        self.brand = brand

    def get_spec(self):
        print(f"wheel_number: {self.wheel_number}")
        print(f"door_number: {self.door_number}")
        print(f"door_number: {self.door_number}")
        print(f"brand: {self.brand}")

c = EletricCar(4,5,"Motor","Tesla")

c.get_spec()

groups = ["Modern Web", "DevOps", "Cloud", "Big Data", "Security", "自我挑戰組"]
ironmen = [46, 8, 12, 12, 6, 58]

ironmen_dict = {"groups": groups,
                "ironmen": ironmen
                }

ironmen_df = pd.DataFrame(ironmen_dict)

print(ironmen_df) # 看看資料框的外觀
print(type(ironmen_df)) # pandas.core.frame.DataFrame

class MyTest:
    def __init__(self,a,b):
       self.a =a
       self.b=b

test = MyTest('aa','bb')

print('a:'+test.a)
print('b',test.b)

class MyTest1(MyTest):
    def __init__(self, a, b,c):
        super().__init__(a, b)
        self.c =c
    def printABC(self):
        print('a:'+str(self.a)+', b:'+str(self.b)+', c:'+str(self.c))


myT1 = MyTest1(1,2,3)
myT1.printABC()

area = pd.Series({'Alaska': 120000, 'Texas': 8875742,
                  'California': 453788}, name='area')
population = pd.Series({'California': 42577, 'Texas': 26448443,
                        'New York': 757367836}, name='population')
print(area.index & population.index)


