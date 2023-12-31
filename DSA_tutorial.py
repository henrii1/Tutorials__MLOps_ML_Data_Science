# python

"""OS module"""   #designed for performing file system actions
import os

# current directiory
print(os.getcwd())

#change directory
os.chdir("C:\Python")

#list directories
a = os.listdir(os.getcwd())     #prints all the directiores from cwd
print(a)
b = os.listdir(r"C:\\emerald")   # using backslash will require two and r since \ is used for new line

# making directiories
os.mkdir("pictures")

os.makedirs("Pictures/Trip pic/November", exist_ok=True) # making  multiple subdirectories and folders. exist_okay is used so that it won't create if it already exists

#deleting
os.rmdir("Pictures")
os.removedirs("Pictures/name")

a = "Text"
combine = os.path.join(os.getcwd, a) # joins the path and creates the file

print(os.path.exists(combine))  #returns a boolean if exist or not.

#checking if its a file or a directory
print(os.path.isdir(combine)) #True
print(os.path.isfile(combine)) #False

#info about the file or folder. most times, just print the entire info, then you can pick which one you want.
print(os.stat(combine)) # you can access the attributes of stats by adding a '.' after (combine). eg below
print(os.stat(combine).st_size)

# pulling out environment variables
print(os.environ.get("PATH"))             # PATH is a variable set by default.

print(os.getlogin())  #prints the current user.


"""SYS module in python"""
import sys

# string containing a platform identifier (win32 for windows, linux for linux)
print(sys.platform)

#string contining the copyright of the interpreter
print(sys.copyright)

# version number and build number of python interpreter
print(sys.version)

# giving an output, just like print
sys.stdout.write('string')

# printing errors
sys.stderr.write("string")

# size of variable
s = 4
print(sys.getsizeof(s))

# list of command line arguments passed to a script
print(sys.argv)  # returns a list of our command line commands

"""re module"""         # regular_expression
import re
names = ['Finn Binde', "abig zes", 'goat skin']
regex = '^\w+ \w+$'
for name in names:
    result = re.search(regex, name)  # how regex are applied
    if result:
        print(result) #returns boolean
        print(name)    # returns the names that match.
        print(result.start(), result.end()) # returns the first and last index that matched. same as using print(result.span())
        print(result.span())  #same as above
        print(result.group())  # returns the index of all matching substrings.

        #working with groups, using parenthesis to split regex characters to define group, result.group(1) returns thr first group
values = ['list of urls']
regex = 'https?'
for value in values:
    if re.match(regex, value):
        print(value)              #those values that start with 'http?'

^Fran # for all starting with 'Fran:
i$  # for all words ending with 'i'
\d  # scans a string for a single numerical data, \d\d will mean two numbers
\s   # any sting containing a space
\w   # matches one word, \w\w means two words
[aeiou]{2}  # specifying regex to match to out of the characters provided, in a string.



"""Multiprocessing and Multithreading"""

#threading module doesn't do parallel work because of the GIL
# threading is mostly used when we require input from user
import threading 
import time

done = False
def worker():
    counter = 0
    while not done:
        time.sleep(1)
        counter += 1
        print(counter)     # prints 1, 2, 3  etc 

# worker()
#input("Press enter to quit")
#done = True                     #this part won't work without threading because function isn't finished.

threading.Thread(target=worker).start()  #runs in a separate thread

input("Press enter to quit")             # runs in another thread, mostly the first thread
done = True

#Daemon Threads are those that we specify for termination when others have, regardless eg.

def worker():
    counter = 0
    while True:
        time.sleep(1)
        counter += 1
        print(counter)     # prints 1, 2, 3 for ever 

threading.Thread(target=worker, daemon=True).start()

input("Press enter to quit")

#example 2
def worker(text):
    counter = 0
    while True:
        time.sleep(1)
        counter += 1
        print(f"{text}: {counter}") 

t1 = threading.Thread(target=worker, daemon=True, args=("abc",))    # Thread 1
t2 = threading.Thread(target=worker, daemon=True, args=("xyz",))    # Thread 2

t1.start()
t2.start()

t1.join()
t2.join()   # makes sure the tasks above finishes before the one below

input("Press enter to quit")

# using a function for threads
threads = []
for _ in range(10):
    t = threading.Thread(target=worker, daemon=True, args=("abc",))
    t.start()
    threads.append(t)  # a list is used because we can't use join directly before all the threads finish

for thread in threads: 
    thread.join()


# threading.main
import time
from threading import Lock, Thread
from urllib.request import urlopen

lock = Lock()

def do_cpu_work():
    for i in range(20000):
        2**i
    
def do_io_work():
    print("start")
    urlopen("https://youtube.com")
    print("end")

if __name__ == "__main__":
    threads = []
    start = time.perf_counter()

    for _ in range(10):
        t = Thread(target=do_cpu_work)
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    
    for _ in range(10):
        with lock:                               # using lock makes it run somehow asynchronously. prints start, end, start, end, instead of start, start, start ...
            t = Thread(target=do_io_work)
            threads.append(t)
            t.start()                          # threading works best for io work such as this



# Multiprocessing

import time
from multiprocessing import Process
from urllib.request import urlopen


def do_cpu_work():
    for i in range(20000):
        2**i
    
def do_io_work():
    urlopen("https://youtube.com")
 

if __name__ == "__main__":
    processes = []
    start = time.perf_counter()

    for _ in range(10):
        t = Process(target=do_cpu_work)
        processes.append(t)
        t.start()

    for process in processes:
        process.join()

    
 # Asynchronous functions

import asyncio

async def main():
    print("Hello ...")
    await asyncio.sleep(1)
    print("...world!")

async def add(x, y):
    return x + y        

if __name__ =="__main__":
    asyncio.run(main())    #prints hello, waits 1 min, prints world

    r = add(5, 6)
    #print(r)      # wouldn't print the result until we use the await method

#async method mimicks multiprocessing by allowing next tasks to run

#for multiple functions, in order to mimick multiprocessing, use 'get_event_loop'
async def counter():
    while True:
        counter += 1
        await asyncio.sleep(0)         # required for switching tasks in worker

async def monitor():
    while True:
        print("done")

if __name__ =="__main__":
    loop = asyncio.get_event_loop()
    task_one = loop.create_task(counter)
    task_two = loop.create_task(monitor)
    loop.run_forever()
    #loop.run_until_complete(task_one)  # used if task one is a finite loop


        


groceries = [] # this evaluates to false when there isn't any value within
if groceries:
    print('done') # doesn't print because it evaluates to false

# in interger is 0, it evaluates to false.

# Exceptions

#raise RuntimeError('error')
try:
    results = 14/0
except ZeroDivisionError: # we want the except to function specific to ZeroDivisionError
    results = 14/2

# except Exception: Catches all types of exceptions
except Exception as e;
    print({str(e)})

# we can also pass multiple exceptions to an except
except(ZeroDivisionError, TypeError):

# .items(), .keys(), .values() method is specifically used with dictionaries in python 3.12

#finding the methods available to an object. List, tuple, dictionary etc
for method in dir(tuple()): # this could be any other object.
    if not method.startswith('__'):         # printing all the methods associated with the class object.
        print(method)


# lists
 
# insert method
names = []
names.append('sugar') # adds sugar to end
names.insert(1, "sugar") # adds sugar to index 1

shopping = []
shopping.append(["sugar", 'salt']) # yeilds a nested list
shopping.extend(["sugar", 'salt']) # yeilds an extended list

shopping.pop(1) # removes from the list using index
shopping.remove('salt')  # use remove to specify the value

# ADDED METHODS.
shopping.clear()      #clears the list
b = shopping.copy()   # shallow copy
shopping.count("a")      # counts the number of a's in our list
shopping.extend([2, 3])  
shopping.index('ada')   # returns the index of 'ada' use a print to view
shopping.insert(1, 'ada')    # insert at an index
shopping.pop()            # pops the last value, returns it but takes it out of the list
shopping.pop(0)        # popes by index
shopping.remove('ada')  # removes by value.
shopping.reverse()      # reverses the list
shopping.sort()          # sorts alphabetically.
shopping.sort(key=lambda name: name.lower(), reverse= True)    # using the lambda function to specify sort condition, also you can reverse the sort.



# Dictionaries
a = dict(a='dave', b="mary")
my_dict = {}
my_dict['key'] = 'value'       # how to add values

keys = ['key1', 'key2', 'key3']
values = ['value1', 'value2', 'value3']
my_dict = {k: v for k, v in zip(keys, values)}   #inserting a list of keys and values

contact = {}
contact['height'] # height is meant to be the key
print(contact['height']) # should print the value associated with this key
# using the .get() method will return None if key isn't found.
result = contact.get('height')
print(result)
result = contact.get('height', '6ft')
print(result) # if result is None, the .get method assigns default value '6ft'
result.pop("age") # pops out the value and key

# Dictionary Methods.
users: dict = {0: 'Mario', 1: 'Luigi', 2: 'James'}             # using hint type to define a dictionary.
users.values()             # returns a list of the values and can be assigned to a variable and iterated over.
users.keys()               # returns a list of keys in our dict, returns a list that is iterable
users.pop(2)               # requires a key. it returns the value poped also
users.popitem()             # pops the last item in our dict. you  can use recursively to continuously remove elements at the end. also returns the item poped
my_copy = users.copy()      # shallow copy (if a value is changed in one, it reflects in the other)
print(f"{id(my_copy)} and  {id(users)}")      # using id returns the reference id of the variable.
a = users.get(1)     #users.get(333, "missing value")       # stores the values of the index, if it doesn't exist, sample code prints missing value
a = users.setdefault(1, 'Missing') #same as get but requires a default value if index isn't found
dict_from_list: dict = dict.fromkeys(a, __value = 'Unknown')   # a should be a list. the values in a becomes the keys and their value defaults to none if not set.
users.items()          # returns a nested tuples inside a list, containing key and value.
users.update({key: value})  # update a key and its value
users | {4: "ade", 5: "bade"}     # using '|' is a union and extends the dictionary
users |= {4: "ade", 5: "bade"}


"""Strings"""
#capitalize
text: str = 'string'
print(text.capitalize())     # capital letters

#casefold
text1 = "MariO"
text2 = 'mArIo'
text1.casefold()
text2.casefold()  #changes to a comparable string, maybe lowercase
check = text1 == text2
print(check)            # True

#center
text = 'abc'
print(text.center(20, '.'))      #center distance and occupier  '.......abc.......

#count
print(text.count('ab'))
#encode
print(text.encode(encoding="UTF-8", errors='strict'))     # encoded version of text.  b'abc'
#endswith
print(text.endswith(('e', 'a')))   # endswith e or a, we can use one argument also
#expandtabs()
text = 'text\ttext2'
print(text.expandtabs(20))   #create tab space at '\t' position
#find()
position= text.find('subscribe') # returns the index of where find is located from the start index
print(text[position:])  # print everything after the found word. if not found, it returns -1
#format()
text = {subject} is doing: {action}
text.format(subject= "cat" action='meow')  # print output returns 'cat is doing meow'
#format_map()
coordinates = {'x': 10, 'y': -5}
text = 'coordinates: ({x}, {y})'
print(text.format_map(coordinates))      # output will map values of x and y
#index()
text.index("banana")  #finds index, returns error if not found
#isalnum()
print(text.isalnum()) # returns boolean if only letters and numbers, returns true
#isdecimal(): numeric
#isalpha():  letters
#isnumeric(): for all kinds of letters regardless of the language
#islower(): boolean: if not lowercase, return False
#isspace(): does string contain only space?
print(''.join(['text1', 'text2', 'text3'])) # joins text with space in between, add '-' to change delimiter.
#lstrip(): text.lstrip("some")  # if text = 'some day', text becomes 'day'
#partition('-'): splits string, specify the separator
#replace()
text.replace("comment", 'subscribe')  # change comment to subscribe
#rindex(): same as index, starts from the end instead
#rsplit(sep=' '): splits into an array with separator as space
#splitlines
text = 'remember to \n comment'
print(text.splitlines()) # convert a text with \n characters into an array each newline indicating a new element.
#strip('luigi'): removing luigi from the text, text.strip('luigi)
#title(): converts a string to a title, making the first letter of each character capitalized.

#functions

# unpacking arguments '*args' converts to a tuple the parameters are positional arguments
# unpacking '**Kwargs' unpacks to a dictionary enter the parameters as keyword arguments to store

#classes

class cars(): # basic class
    pass

car = cars() # instantiating the class

dir(car) # lists all the default methods associated with this class object

class car ():
    def __init__(self, brand):
        print(f"brand is {brand}") # parameters can be used directly to perform operations
        self.car_brand = brand  # variables however must be associated to the class as a class attribute
    def count(self, val):  # class methods must be on the same line level as the __init__ and must be associated with the class
        print(self.car_brand) # within the __init__ method, we can print brand but without, we'll have to assign it to a class attribute 'self.car_brand'
        counting = val # within a normal function, we can assign without referring to the class
        return val # used within the function and never without.
    def repeat(self, num):
        recursion = self.count(num) # using a function within a function requires referring to the class


# Generally, if you want a variable to be reusable outside the class method it was defined, define it as a class attribute using the 'self.name' = value
#NB: we can use a function defined above in one defined below

def expense(self, amount):
    'do something'
    self.report() #report is used here but defined below
def report(self):
    print(f"some things")


#inheritance
class pet:
    def eat(self):
        self.food = self.food - self.appetite # we didn't define the class attributes, we just defined the operation
        print(self.food) 

class dog(pet):
    def __init__(self, food, appetite):
        self.food = food                 # we defined the class attribute after inheritance
        self.appetite = appetite

#print all the methods of a class
dogs = dog()

for attribute in dir(dogs):
    if attribute.startswith("__"):
        continue
    print(attribute)  # printing all attribute except those starting with '__'


# python modules and packages
pwd # prints the working directory
touch pandas.py # creates a file
mkdir pack 
cd pack 
cat __init__.py
cat module.py


# import modules
import pandas
from pandas import x

# from packages (the __init__.py file tells python that this directory is a package)
import pack.module # importing a module within a package

pack.module.func() # using a function from the module within a package

# another way is to import modules within the __init__.py file. that way, when the package is imported, modules automatically become available


import sys

def main(arguments):
    print("hooked")
    for argument in arguments:
        print(argument)

if __name__ == '__main__': # checks if script is being run as a main program and not imported as a module
    main(sys.argv) #prints 'hooked' the 'file_name' then all comand line arguments passed to in on the command line.

# example of __name__
%%writefile ./multiply.py
def mul(a, b):
    return a*b
if __name__ == '__main__':     # print this results only when this file is ran as the main file, not when it is imported.
    print(mul(2,3))
    print(__name__)     

'''File2: example.py'''
import multiply

print(multiply.mul(2, 1))
print(__name__)        # in this file, the if __name__ block from the multiply file won't run because it is imported and the current name of that module is not 'main'

# lambda functions, Map and Filter.

#lambda function:the don't contain the def keyword
#Definition: lambda argument: expression
lambda x,y: x+y
#same as
def add(x,y):
    return x+y

#maps use the lambda function as argument
# Map function
a = [1,2,3,4]
def square(x):
    return x*x
map(square, a)  # returns the object # arguments: function, sequence of numbers to apply function to.,
list(map(square, a)) # output will be a list of squares.

#using lambda in map
map(lambda x:x*x, a)
list(map(lambda x:x*x, a))   # same as above

#working with multiple lists with map and lambda
b = [3,4,5,6]
tuple(map(lambda x,y:x+y, a, b))

#Filter 
#filter argument: function, iterable
for i in range(1, 11):
    if i%2 == 0:
        print(list(i))

# same as
list(filter(lambda x:x%2==0, range(1, 11)))

#reduce function: used for performing computation on a list
import functools
num = [1,2,3,4]
functools.reduce(lambda x,y:x+y, num) # sums up all the element in the list 'num'




# virtual environments in python (useful for installing dependencies) the following are command line or power shell code.

python3 -m venv myenv # venv is a new environment
tree myenv #lists all python packages and modules in this environment
which python # shows the directory of the python and includes the virtual environment if within.
# activating environment for cmd
myenv\Scritps\activate   
# activating environment for powershell
.\myenv\Scripts\Activate

echo 'flask' >requirements.txt # writes 'flask' into the requirement.txt file

pip install -r requirement.txt # installing all in the requirement.txt file

deactivate # used to deactivate the virtual environment hence all installed or imported won't be available anymore.


# Testing (writing and executing them)
cd preferred_directory #
cd - # takes you to the previous directory.

%%writefile addition.py 
def add(a,b):
    return(a + b)
def sub(a, b):
    return(a - b)

%%writefile test_addition.py 
pip install pytest
import addition
import pytest 
def test_add():
    assert addition.add(4, 5) == 9
def test_sub():
    assert addition.sub(4, 5) == -1

#running the test_addition.py file should show two passed or 1 passed and one failed.

# Using Unitest
import unittest
class TestExm(unitest.TestCase): # Interit the base class'unitest.TestCase'
    def test_assertion(self):
        self.assertEquals('some string', 'others') #checking equals. you can add functions to this method
        # we can also use self.assertNotAlmostEqual

unitest.main(argv=[''], verbosity = 2, exit = False)

# fails because 'some string' != 'others'
# NB: name your test directory with 'tests' so as not to collide with inbuilt dirs
# test files and test functions should be prefixed with 'test_'
# test classes should be prefixed with captial "T" eg 'TestClass'
# test directories are like packages and will require the '__init__.py' file

#cmd or powershell
python -m venv pytest # creating a virtual environment named pytest

echo pytest >requirements.txt # write pytest into the requiremts.txt file
pip install -r requirements.txt

cd test_directory
pytest # by calling pytest in the test directory, the test is ran.
# for pytest to run the file, it has to abide by the test naming convention.

# if this is the test file that gets ran, notice that it follows the conventions and has no other thing inside except test functions.
def test_add():
    assert addition.add(4, 5) == 9
def test_sub():
    assert addition.sub(4, 5) == -1

# if there are other statements that aren't test functions, use pytest filename.py to run the test
# use pytest -vvv filename.py to see the entire script when running your code

# Test Classes
class TestStrToInt:
    def setup(self):
        print('\n this is setup')
    def teardown(self):
        print('\nthis is teardown')
    def setup_class(cls):
        print('\nthis is setup class')
    def teardown_class(cls):
        print('\nthis is teardown class')
    def test_rounds_down(self):  # all above are setup. this is the first test
        result = str_to_int('1.99') #str_to_int is the function that converts str to int. I didn't define.
        assert result == 1   
    def test_round_down_lesser(self): # second test.
        result = str_to_int('2.2')
        assert result == 2


# parameterizing test 
# we have a function 'str_to_bool' that converts 'yes', 'y' or '' to True.

#normal method
def test_str_yes():
    result = str_to_bool('yes')
    assert result == True

def test_str_y():
    result = str_to_bool('y')
    assert result == True

    ...

# using parameterization, we use pytest decorator to wrap extra capabilities

@pytest.mark.parametrize('value', ['y', 'yes','']) # making this iterable
def test_is_true(value):
    result = str_to_bool(value)
    assert result is True

# output 'F..' means 1 failure and 2 passing


# seting a debugger to better understand the cmd test output
pytest --pdb  -v test_file.py # on command line. -v is verbosity. you can use -vvv to increase this

# enter 'h' to see what command line functions you have to better explain the failure, use 'l' to list the failure line in code
# to see all the methods available to you, use 'pytest --help'



# fixtures help avoid doing the def setup method by automatically figuring out the setup and avoiding test file path collitions
# remember, all files outputed from command line are saved to a location.
class TestFixtures:
  def test_write_yes(self, tmpdir): # specifying where the test output will be saved to
    path = str(tmpdir.join('test_value')) # joining the test_value str to the path
    write_integer('Yes', path) # this function writes the str 'yes' to the path. The function also uses the 'str_to_bool' function
    with open(path, r) as _f: 
      value = _f.read()
    assert value == 'True'


# Pandas 

# Activating python virtual environment on cmd
cd path\to\your\directory
python -m venv env_name
cd env_name\Scripts
activate

# on powershell
cd path\to\your\directory
python -m venv env_name
cd env_name\Scripts
.\activate.bat #.\ is a powershell read convention

# on bash
cd path\to\your\directory
python -m venv env_name
env_name/bin/activate

# Pandas
# you do not need to download the file from the internet, just pass the url and pandas will read
file_name = 'https://github.com/henrii1/wind-turbine-power-curve-modelling/raw/main/dataset/kelmarsh_02.xlsx'

import pandas as pd
read = pd.read_excel(file_name)
read.head(10)

# Converting the tables to markdown files for teaching etc
!pip install tabulate #required dependency
from pandas.io.clipboard import to_clipboard # i want the converted file to save to clipboard
md = read.to_markdown() #writing to markdown
to_clipboard(md, excel=True) #using 'to_clipboard', i want the file to paste as an excel table


#use queries with pandas
df.query('ratings > 30').head(10) # put all forms of queries into the brace. .head is for display
pab = df.query("region.str.contains('robles', na = False)", engine = 'python') # because string contains functions, you'll have to specify the engine

#changes to string
df['var_short'] = df['variety'].replace({'red wine': 'r', 'white wine': 'w'}) #replace red wine with r and white wine with w, store in var_short

#applying functions in pandas
def good_wine(value):
  if value > 94:
    return True
  return False

df['good'] = df['rating'].apply(good_wine) # Adds a new column called good, if ratings is greater than 94, it appends true.

"""Tuples"""   #they are faster than lists, immutable and cannot be added to or deleted from

tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)
new_tuple = tuple1 + tuple2

tuple1 = (1, 2, 3)
repeated_tuple = tuple1 * 3    # performing operations

my_tuple = (1, 2, 3, 4, 5)   
element = my_tuple[0]
subset = my_tuple[1:4]   #indexing

my_tuple = (1, 2, 2, 3, 4, 2)
count_of_2 = my_tuple.count(2)     # counting values

my_tuple = (1, 2, 3, 4, 5)
new_tuple = tuple(element for element in my_tuple if element != 3)   #creating a new tuple without some elements: alternative to deleting.

"""sets"""    # unordered and mutable, no duplicate values

my_set = {1, 2, 3}
my_set.add(4)          #adding elements

my_set = {1, 2, 3}
my_set.update([4, 5, 6])  #adding multiple elements

my_set = {1, 2, 3}
my_set.remove(2)          # deleting by value. Raises key error if not found

my_set = {1, 2, 3}
my_set.discard(2)         # deleting by value, raises no error if not found

my_set = {1, 2, 3}
popped_element = my_set.pop()    # returns an abitrary element and removes it

my_set = {1, 2, 3}
my_set.clear()            # empties set

set1 = {1, 2, 3}
set2 = {3, 4, 5}
union_set = set1.union(set2)  # others too, intersection, difference, symmetric difference.




#NB: when given a question, ask questions to clarify requirements and analysis. also use test cases. use pseudocodes too.
#NB: always look over every part of your code to see if you can reduce the code length.

# DSA commences.
# Built in data structures: Lists, TUple, Sets, Dictionary
# User Defined data structures: Stack, Queue, Linked list, Tree,Graphs

# Tuples are faster than lists, and they are used when you don't want the data to be updated

# Dictionary key must be unique. the values musn't. Dictionarys are unordered also.

# use the set constructor to create an empty set: set() or s = set([1,2]) passing a list into the set {1,2,3}. sets are on ordered.

s = set()
s.add(34) # adding values into sets, they are mutable.
# they can't be nested. because they contain only unique values.
#sets can't be indexed and don't have keys. we can check for values within usin the 'in' keyword or a loop

1 in s

for i in s:
    print(i)


'''Search Algorithms'''
# Linear Search: compares elements one after the other. complexity is O(n)
from typing import List

list = [2, 8, 3, 6, 4]

def linear_search(value: int, list: List):
    i = 0
    while i <= len(list)-1:
        if list[i] == value:
            print(f'{value} found at index {i}')
            i += 1
            return True
        else:
            print(f"number {value} is not in the list")
    return False


# Binary Search: works only on sorted lists. complexity is O (logn)

from typing import List

def binary_search(value, lst: List):
    L = 0
    U = len(lst) - 1

    while L <= U:
        mid = (L + U) // 2

        if lst[mid] == value:
            print(f"Value found at index {mid}")
            return True
        elif lst[mid] < value:
            L = mid + 1
        else:
            U = mid - 1

    print("Value not found in list")
    return False

# Example usage:
my_list = [2, 4, 6, 8, 10, 12, 14, 16]
result = binary_search(10, my_list)
print(result)




        



'''Stacks'''
# ordered collection of object from top to base. stores data using the 'last in first out' or 'first in last out' manner
# stack operations: push (adds elements), pop (removes element), Peek or top (is it full), isEmpty (is it empty)

#Uses: reversing string, forward and backward in web apps. numerous others.
# since stacks are not built in data type, we can use a list for a stack. append==push, pop==pop

stack = []
stack.append(12)
stack.append(14)
stack.pop()    # 14, last element is removed

# check if empty
stack = []
len(stack) == 0
not stack

# defining a stack using list
stack =[]
def push():
    if len(stack)==n:
        print('list is full')
    else:
        element = input("Enter the element:")
        stack.append(element)
        print(stack)

def pop_element():
    if not stack:
        print("stack is empty")
    else:
        e = stack.pop()
        print(f"removed element:{e}")
        print(stack)

n = int(input("limit of Stack:"))      # limit of stack shows before the input
while True:                            # always going to run
    print("select the operation 1.pust 2.pop, 3.quit")
    choice = int(input())
    if choice == 1:
        push()
    elif choice == 2:
        pop_element()
    elif choice == 3:
        break
    else:
        print("Enter the correct operation")

# implementing stacks using modules
#collections--deque (double ended queue)
from collections import deque
stack = deque()
stack.append(23)
stack.append(24)
stack.pop()

#check empty, 
not stack

# Using the Queue module. "Lifoqueue"
import queue
stack = queue.LifoQueue
stack.put(12)
stack.put(23)
stack.get()   #pop method

stack = queue.LifoQueue(3)   #max size is set to three.
stack.put(5, timeout=3)   # set the timeout so that it can print 'queue is full'
stack.get(timeout=3)    # sets the timeout so that it can print 'queue is empty'
#queue will keep searching if you don't use timeout


'''Queues'''
# a linear data structure where the elements are inserted from one end and removed from the other
# i.e (like a pipe, the first elements are removed first) First in First out.
# enqueue: (add element), dequeue: (remove elements), isFull, isEmpty.

# using lists as queue. append=enqueue, pop(0):dequque
queue = []
queue.append(10)
queue.append(20)
queue.pop(0) # pops the first element entered

# using insert and pop
queue = []
queue.insert(0, 10) # index and value
queue.insert(0, 20)
queue.pop()

# empty
not queue


queue = []
def enqueue():
    if len(queue) == n:
        print("List is full")
    else:
        element = input('Enter a Element:')
        queue.append(element)
        print(queue)

def dequeue():
    if not queue:
        print("queue is empty")
        return
    e = queue.pop(0)
    print(f"Removed element {e}")

n = input("Enter the limit of the queue")

while True:
    value = input("Enter a value: 1.enqueue, 2.dequeue, 3.show, 4.quit")
    if value == 1:
        enqueue()
    elif value == 2:
        dequeue()
    elif value == 3:
        print(queue)
    elif value == 4:
        break
    else:
        print("enter a valid operation")


# Implementing Queue using deque from collections (using dequeue, you can append and remove data from both sides)

# two sides: left and right side.    Methods: left: (appendleft, popleft), right: (append, pop)
from collections import deque
q = deque()
q.appendleft(10)
q.appendleft(20)

q.pop()
q.pop()

# or
q.append(10)
q.append(20)

q.popleft()

#NB: this can easily be converted to the stack method.


#Uing Queue class from queue modules to implement (this module also contains LIfoQueue, used for stacks)
# add: Queue(maxsize=) if maxsize is equal to zero then you have defined an infinite queue.
# methods: Queue.size, .empty, .full
#put(item, block = Boolean, timeout=time)  # if block is true, it will wait until a slot is available to put a value if max size already attained.
#put_nowait(item) # will print queue is full
#get(block = True, timeout = None)  $ like the put. True is default.
# get_nowait()

from queue import Queue

q = Queue()

q.put(10)
q.put(50)

q.get()



'''Priority Queues'''
# entering is first to last, removing is based on priority, each element is assigned a priority.
# setting priority: value of the element (lowest value:highest priority, or highest value:hightest priority), Tuple priority: taking tuple of value and priority

# Priority Queues are implemented using Lists or PriorityQueue from queue

# lowest:highest priority
q = []
q.append(12)
q.append(23)
q.sort
q.append(24)
q.sort

q.pop()  # based on priority

# Using Binary Heap structure (PriorityQueue)

# also use the block and timout, or put_nowait with PriorityQueues

from queue import Queue

q = Queue()

q.put(10)
q.put(45)
q.put(23)

q.get()  # 10
q.get()  # 23


# tuple

q = []
q.append((1, "alexa"))
q.append((2, "ded"))
q.sort(reverse = True)   #sorts in desending order

q.pop(0)
q.pop(0)  

"""Sliding Window"""     # method of finding subarrays. time O(n), space O(1)
#subarray: contiguous set of values from an array. {1,2, 3, 4}   sub array{1,2}, not {1,3} because the latter in not contiguous, ordering is preserved
#substring: is a subarray but with characters
#subsequence: is a subarray but without the contiguity rule  {1,3} is also a subsequence ordering is preserved i.e {4, 1} isn't a subsequence
#subset: no contiguity, no ordering

#NB: if you are not given an array to work with, create your own

#E.G1: Given a array of positive integers, find the subarrays of integers that add up to a given number. 

def get_subarrays(input_arr, desired_sum):
    # Validate input
    assert desired_sum > 0, 'Desired sum must be greater than 0.'
    
    # Current window sum and window sum start index
    sum_val = 0
    sum_start_index = 0
    solutions = []

    for index, item in enumerate(input_arr):
        sum_val += item

        while sum_val > desired_sum:
            sum_val -= input_arr[sum_start_index]
            sum_start_index += 1

        if sum_val == desired_sum:
            solutions.append(input_arr[sum_start_index:index + 1])

    return solutions


# Tests
# Test case #1
example_input1 = [1, 7, 9, 4, 3, 2, 2]
desired_sum1 = 7
solution1 = [[7], [4, 3], [3, 2, 2]]

calculated_solution1 = get_subarrays(example_input1, desired_sum1)

print(f"Example Input #1: {example_input1}, Desired Sum: {desired_sum1}, Solution: {calculated_solution1}")
assert calculated_solution1 == solution1

# Test case #2
example_input2 = [23, 1, 6, 9, 15, 8]
desired_sum2 = 24
solution2 = [[23, 1], [9, 15]]

calculated_solution2 = get_subarrays(example_input2, desired_sum2)

print(f"Example Input #2: {example_input2}, Desired Sum: {desired_sum2}, Solution: {calculated_solution2}")
assert calculated_solution2 == solution2

# Test case #3
# Sliding window technique cannot handle negative numbers in this case, so the solution will not be complete
example_input3 = [-1, -4, 0, 5, 3, 2, 1]
desired_sum3 = 5
solution3 = [[-1, -4, 0, 5, 3, 2], [5], [3, 2]]

calculated_solution3 = get_subarrays(example_input3, desired_sum3)

print(f"Example Input #3: {example_input3}, Desired Sum: {desired_sum3}, Solution (some missing): {calculated_solution3}")
assert calculated_solution3 != solution3

## E.G2: Given an array of 0's and 1's, find the maximum sequence of continuous 1's that can be formed by flipping at-most k 0's to 1's.

def get_max_sequence(input_arr, max_flips):
    # Validate input
    assert max_flips >= 0, 'Max flips cannot be negative.'

    sub_arr_start = 0
    sub_arr_end = 0
    flipped_zeroes = 0
    longest_sub_arr = {'start': 0, 'end': 0, 'len': 0}

    for index, item in enumerate(input_arr):
        # Always start by increasing window size
        sub_arr_end = index

        if item == 0:
            flipped_zeroes += 1

        sub_arr_len = 1 + sub_arr_end - sub_arr_start
        if flipped_zeroes <= max_flips and sub_arr_len > longest_sub_arr['len']:
            longest_sub_arr = {'start': sub_arr_start, 'end': sub_arr_end, 'len': sub_arr_len}

        # Decrease window size until we are less than or equal to the max flip limit
        while flipped_zeroes > max_flips:
            if input_arr[sub_arr_start] == 0:
                flipped_zeroes -= 1

            sub_arr_start += 1

    return input_arr[longest_sub_arr['start']: longest_sub_arr['end'] + 1]


# Tests
# Test case #1
example_input1 = [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0]
max_flips1 = 2
solution1 = [0, 1, 1, 0, 1, 1]

calculated_solution1 = get_max_sequence(example_input1, max_flips1)

print(f"Example Input #1: {example_input1}, Maximum Flips: {max_flips1}, Solution: {calculated_solution1} (Length: {len(calculated_solution1)})")
assert calculated_solution1 == solution1

# Test case #2
example_input2 = [0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0]
max_flips2 = 3
solution2 = [1, 0, 0, 0, 1, 1, 1, 1]

calculated_solution2 = get_max_sequence(example_input2, max_flips2)

print(f"Example Input #2: {example_input2}, Maximum Flips: {max_flips2}, Solution: {calculated_solution2} (Length: {len(calculated_solution2)})")
assert calculated_solution2 == solution2

#E.G3: Given an array of integers, find maximum sum subarray of the required size.

def get_max_subarray(input_arr, subarray_size):
    # Validate input
    assert subarray_size > 0, 'Subarray size must be positive.'

    current_sum = 0
    max_sum = 0
    max_sum_start_index = 0

    # Iterate entire array from left to right
    for index, number in enumerate(input_arr):
        # Increase the window size by one from the right
        current_sum += number

        if index < subarray_size:
            # Continue to accumulate until we reach the desired subarray size (= max window size)
            max_sum = current_sum
        else:
            # We are over the max window size, so remove one element from the left
            current_sum -= input_arr[index - subarray_size]

            if current_sum > max_sum:
                # We have a new maximum sum window, so record its starting index
                max_sum = current_sum
                max_sum_start_index = index - subarray_size + 1

    return input_arr[max_sum_start_index:max_sum_start_index + subarray_size]


# Tests
# Test case #1
example_input1 = [-1, 2, 3, 0, -3, 9]
subarray_size1 = 2
solution1 = [-3, 9]

calculated_solution1 = get_max_subarray(example_input1, subarray_size1)

print(f"Example Input #1: {example_input1}, Subarray Size: {subarray_size1}, Solution: {calculated_solution1}")
assert calculated_solution1 == solution1

# Test case #2
example_input2 = [6, 0, -1, 2, 1, -3, 4]
subarray_size2 = 3
solution2 = [6, 0, -1]

calculated_solution2 = get_max_subarray(example_input2, subarray_size2)

print(f"Example Input #2: {example_input2}, Subarray Size: {subarray_size2}, Solution: {calculated_solution2}")
assert calculated_solution2 == solution2


"""Bit Manipulation"""
# Converting base 10 to base 2: 28 = multiples of 2 are (16 + 8 + 4), yeilding 1(for 16), 1(for 8), 1(for 4), 0(for 2) and 0(for 1) == 11100.  NB: consider each power of two consecutively.

# printing binary digits
n1 = 28
n2 = 19

print(bin(n1))       #output: 0B11100
print(bin(n2)[2:])    #output: 10011

# we use bitwise operators to perform computation with binary (AND, OR, XOR)

# AND    (1 and 1 is 1, otherwise 0)
n3 = n1 & n2
print(bin(n3)[2:])

# OR     (0 or 0 is 0, otherwise 1)
n4 = n1 | n2
print(bin(n4)[2:])

# XOR    (1 XOR 0 = 1, 0 XOR 1 = 1, otherwise 0)
n5 = n1 ^ n2
print("0" + bin(n5)[2:])     # we added zero because the terminal won't display leading zeros

# NOT
print(bin(~n1))      # the not symbol doesn't invert the number as it is supposed to. we do it another way

print("0" + bin(0b111111111111 - n1)[2:]) #'0b' indicates we are writing a binary, "1's" should equal the length of the number to convert

# SHIFTS   (equivalent to adding a zero at the end)

number = 20
print(bin(number)[2:])   # 10100
number <<= 1       #  left shifting once '1'
print(number)   # 40
print(bin(number)[2:]) # 101000
number >>= 2  # right shift two places
print(number)   #10
print(bin(number)[2:])  #1010

# Flags  #(Read (R), Write (W), Execute, change policy)
# giving a user permissions
#RWEC = 0b1111, R only = 1000 ...

person1 = 0b1000
person2 = 0b1110
person3 = 0b1111
person4 = 0b1010
person5 = 0b1101

# all have to have a certain permission before something can be done
together1 = person1 & person2 & person3 & person4 & person5   # 0b1000, what all of them can do.
print(bin(together1)[2:])

# one person should have all the permission at least (use the pipe operator)
together2 = person1 | person2 | person3 | person4 | person5     # 0b1111

# permissions in practice
WRITE_PERMISSION = 0b0100
READ_PERMISSION = 0b1000

def perf(permission):
    if permission == 0b1100:
        print("do something")

perf(WRITE_PERMISSION | READ_PERMISSION)   # how permission is used in practive

# switching variables without a placeholder
a = 10
b = 20

a ^= b    # same as  a = a ^ b
b ^= a 
a ^= b

print(a)  #20
print(b) #10

#checking if a number is even or odd
somenumber = 345392
if somenumber & 1 == 0:
    print("even")
else: 
    print('odd')

"""Strings"""

'''Linked list'''
# list of nodes, a list contains data field and one or two links. 

#first node reference is called 'head' node 1 stores node 2's reference, node 2 stores node 3 reference. the last node's reference is 'Null' and called tail

# advantages: it is a dynamic data structure. elements can be added or removed easily, they can be used to implement stacks, queues and graphs.

# Types: single linked list (only foward movement, backward isn't easy), Double linked list, circular linked list

# using classes to create linked list
class Node:
    def __init__(self, data):
        self.data = data
        self.ref = None   # Not 'Null', 'empty'

class LinkedList:
    def __init__(self):
        self.head = None     # starting point
    # 3 operations add, removing elements and traversal of linked list.
    #Traversal: check if empty (print a message if none-use if head is none, linkedlist is empty)
    def print_LL(self):
        if self.head is None:
            print("Linkedlist is Empty")
        else:
            n = self.head
            while n is not None:     # n starts from head and is assigned to n.ref until the last node when n.ref is Null  
                print(n.data, '-->', end=" ")  # this make our output of form 4 --> 5
                n = n.ref        # n will be null at the last node

# self.head is the reference to the first node. self.head.data is the data in the node. self.head.ref is the reference of the next node.


#Adding elements: add can be done at the begining, middle or end of the linked list

#Adding at the beginning: create the node (Node class), new node ref = head (because previous fist node reference was stored in head) lastly, point head to new node.

    def add_begin(self, data):
        new_node = Node(data)  #create the node
        new_node.ref =self.head # point the node to head (previous self.head and self.head stores ref of previous first node)
        self.head = new_node    #point head to new node (assigned to new node) NB: the reference is a value the class object creates for that instance.
                                #self.head = new_node stores the reference of that class instance. you can try printing a class instance and see the reference as output
        
# LL1 = LinkedList()
# LL1.add_begin(10)
# LL1.add_begin(20)
# LL1.print_LL()

# adding data at the end of the linked list
# create the node, check if linked list is empty (if head is none),

    def add_end(self, data):
        new_node = Node(data)
        if self.head is None:   # if linkedlist is empty
            self.head = new_node  #NB: here self.head stores the reference to an object an can be used to access the objects methods using n.ref, if n=self.head
        else:
            n = self.head
            while n.ref is not None:  # n.ref is only None (null) at the end
                n = n.ref
            n.ref = new_node          # assign the new node reference to the previous nref value.

# LL1 = LinkedList()
# LL1.add_begin(10)
# LL!.add_end(100)
# LL1.add_begin(20)
# LL1.print_LL()     # 20 --> 10 --> 100

# Adding elements btwn nodes
# we can add after or before a certain node.

# adding after a certain node.
#steps: find the x node(the one to add after) using n.data == x

    def add_after(self, data, x):       #x is the data in the node we want to place new one after.
        n = self.head
        while n is not None:
            if x == n.data:      #finding x position using while loop and if
                break
            n = n.ref
        if n is None:
            print("node is not present in linkedlist")
        else:             # using else to create the new node
            new_node = Node(data)
            new_node.ref = n.ref                   # the one pointing to is the one we assign first.
            n.ref = new_node  # n.ref is pointing to the new node (n.ref will always store the reference to a class object)
        

# LL1 = LinkedList()
# LL1.add_end(100)
# LL1.add_end(20)
# LL1.add_begin(10)
# LL1.add_after(200, 100)
# LL1.print_LL()            10-->100-->200-->20-->
    
# Adding an element before a given node.

    def add_before(self, data, x):   # if x is the first node self.head.data will equal x.
        if self.head is None:
            print('Linked list is empty')  #this helps to prevent errors because with the print, the under code doesn't run
        if self.head.data == x:
            new_node = Node(data)
            new_node.ref = self.head
            self.head = new_node

# after confirming that the first node isn't x, we find the node and go to its previous node
# previous node is one which the value of the next node is x 'n.ref.data == x' means the value of data from previous reference since the refs are objects.
        n = self.head
        while n.ref is not None:
            if n.ref.data == x:
                break
            n = n.ref
        if n.ref is None:
            print("Value isn't within list")
        else:
            new_node = Node(data)
            new_node.ref = n.ref
            n.ref = new_node                # check the after code for clarity

 # LL1 = LinkedList()
# LL1.add_begin(10)
# LL1.add_after(20, 10)
# LL1.add_before(30, 10)
# LL1.print_LL()   20-->30-->10-->          


# inserting a node when the linked list is completely empty

    def insert_empty(self, data):     # works only if linkedlist is completely empty
        if self.head is None:
            new_node = Node(data)
            self.head = new_node
        else:
            print("Linked list is not empty")



# Deleting operations from the list. from (end, middle and begining)

#from Begining: check if its empty first. if not delete and point head to second node
    def delete_begin(self):
        if self.head is None:
            print("LL is empty so we can't delete'")
            #Return   # also ends.
        else:
            self.head = self.head.ref    # point self to the reference of the second node. by doing this we delete. our class will only return linked values

# Deleting the last node
#  check if list is empty, traverse to the last node(n.ref = None) traverse from self.head.

    def delete_end(self):
        if self.head is None:
            print("LLis empty so we cant delete node")
        elif self.head.ref is None:     # this condition is included for when list contains only one value. otherwise will give an error.
            self.head = None
        else:
            n = self.head
            while n.ref.ref is not None:       # finding the node before the last one.
                n = n.ref
            n.ref = None      


# deleting the node from any position in the list. We perform delete by value.

    def delete_by_value(self, x):
        if self.head is None:
            print("can't delete because list is empty")
            return
        if x==self.head.data:    # if the x value is the first node
            self.head = self.head.ref
            return
        n = self.head
        while n.ref is not None:
            if x == n.ref.data:
                break
            n=n.ref
        if n.ref is None:
            print("Node is not present")
        else:
            n.ref = n.ref.ref




'''Doubly Linked List'''
# each node contains the data of the next and previous nodes.
# performing: Insertion, Deletion and Traversal operations.

#NB: we need extra memory to store links in the doubly linked lists
# each node takes the previous node class ref and stores as pref and the next node's as nref
# conventions (pref: previous node ref, nref: next node ref)

#Inserting at the first node position
# steps: create a node, new_node nref =head, head points to new node


#Inserting at the end: create node, go to last node reference, last_nod nref=new_node ref.
# new_node pref = last_node

#Inserting inbetween: create node, go to previous node before where we want to add, x.nref = newnode,
# new_node.pref = nref of previous, newnode nref= pref of next.

#Deleting from the begining of the linked list: head = 2nd node, 2nd pref = none

#Deleting from the end: find 2nd last node, 2nd last nref = none

#Delete by value: go to previous node of reference, change previous nref to the next object, change pref of next object to new node

#Traversal: nref for forward and pref for backwards

class Node:
    def __init__(self, data):
        self.data = data
        self.nref = None
        self.pref = None

class doublyLL:
    def __init__(self):
        self.head = None
    def print_LL(self):        # traversing in the forward direction, same as the single linked
        if self.head is None:
            print("Linked list is empty")
        else:
            n = self.head
            while n is not None:
                print(n.data, '-->', end=" ")
                n = n.nref

    def print_LL_reverse(self):
        print()                                    # add this so that output from LL forward and LL reverse functions won't print on same line.
        if self.head is None:
            print("Linked list is empty")
        else:
            n = self.head
            while n.nref is not None:
                n = n.nref
            while n.pref is not None:                 # first node pref is None, last node nref is None too.
                print(n.data, "-->", end = ' ')
                n = n.pref



#Inserting a node

#When empty: create the node, head = new-node
    def insert_empty(self, data):
        if self.head is None:
            new_node = Node(data)
            self.head = new_node
        else:
            print("Linked List is not empty")

#Adding at the begining: check if linked list is empty, if not, add a new node at beginning
    def add_begin(self, data):
        new_node = Node(data)
        if self.head is None:    #for empty
            self.head = new_node
        else:
            new_node.nref = self.head
            self.head.pref = new_node
            self.head = new_node
    def add_end(self, data):
        new_node =Node(data)
        if self.head is None:    #for empty
            self.head = new_node
        else:
            n = self.head
            while n.nref is not None:
                n = n.nref
            n.nref = new_node
            new_node.pref = n




# inserting after and before a given node.
# check if the linked list is empty, if not, traverse to given node x


    def add_after(self, data, x):
        if self.head is None:
            print("LL is empty")
        else:
            n = self.head
            while n.ref is not None:
                if n.data == x:
                    break
                n = n.ref
            if n is None:
                print("Given Node value not present")
            else:   # check whether you are inserting after the last node because the method is different for last node.
                new_node = Node(data)
                new_node.nref = n.nref
                new_node.pref = n
                if n.nref is not None:
                    n.nref.pref = new_node
                n.nref = new_node

        def add_before(self, data, x):       #insert before
            if self.head is None:
                print("LL is empty")
            else:
                n = self.head
                while n is not None:
                    if x ==n.data:
                        break
                    n = n.nref
                if n is None:
                    print("Given node is not present in DLL")
                else:
                    new_node = Node(data)
                    new_node.nref = n
                    new_node.pref = n.pref
                    if n.pref is not None:
                        n.pref.nref = new_node
                    else:
                        self.head = new_node   # pointing previous first node pref to the newnode.
                    n.pref = new_node



# Deleting from DDL:

#From Beginning: check if empty, check if the DDL contains only one node, then we can write the code for multiple nodes

    def delete_begin(self):
        if self.head is None:
            print("DDL is empty")
            return   # we can use else or elif here
        if self.head.nref is None:  #if it contains only one node
            self.head = None
            print("DLL is empty after deleting")
        else: 
            self.head = self.head.nref
            self.head.pref = None


# Delete end: check for empty, check for one node, perform normal delete

    def delete_end(self):
        if self.head is None:
            print("there is no element in the list")
            return
        if self.head.nref is None:
            self.head = None
            print("DDL contains just one node")
        else:
            n = self.head
            while n.nref is not None:
                n = n.nref
            n.pref.nref = None


# Delete by value
# when list is empty, when DLL contains only one node, when you want to delet first or last node, normal
    def delete_by_value(self, x):
        if self.head is None:
            print("no node within the DLL")
            return
        if self.head.nref is None:
            if x == self.head.data:
                self.head = None
            else:
                print("the input value isn't in the DLL")
            return
        if self.head.data == x:    # if we are deleting the first element
            self.head = self.head.nref
            self.head.pref = None
            return
        n = self.head
        while n.nref is not None:
            n = n.nref
            if n.data == x:
                break
            if n.nref is not None:
                n.nref.pref = n.pref
                n.pref.nref = n.nref
            else:                      # if n.nref is none, at the last node
                if n.data == x:
                    n.pref.nref = None
                else:
                    print("x value isn't present in DLL")



'''Cicular LL or Circular DLL'''

# last node contains the reference of first node.
# we can start from any node since it is cycler  

#Insertion LL:
# when empty: create the node, point the reference to itself
# at begining: create a node, point the ref to the reference of the first node, point last node to new node
# at end: create node, last node stores reference of new, new node stores reference of first node
#at middle: create node, change both reference like a normal linked list.

#Deletion LL:
#Traversing
# mainly same just that nothing points to none.
####circular link program is similar to that of the others, 
'''Write the programs for the circular LL and DLL'''




# Non Linear Data Structures.


'''Trees and Graphs'''
# collection of trees called nodes. each node has edges. not all have children
# leaf nodes, or terminal nodes are those without children

# if we have n nodes, we'll have n-1 edges.
# trees are recursive. they contain sub trees.

#node degree: total number of children associated with that node
#Tree degree: highest node degree is equal to tree degree.

#Level: start from 0 and increments by one for each children level

#Hight of node: longest path from any leaf node to that node.
#Hight of Tree: longest path from any leaf node to the root node.

#Depth of node: number of edges from root node to that node.

#NB: hight of leaf node is 0, depth of root node is 0

#Depth of tree: longest path from root node to leaf node.

'''Types of trees'''
# general tree: no limit to the number of children a node can have
# binary trees: each node can have at most 2 children
#TYPES OF BINARY TREE
#--Full, complete, perfect, balanced, pathological binary trees.

# Full BT: each node has 0 or 2 children. or each node other than the leaf nodes contain 2 children
# Complete BT: all the levels are completely (have 2 children) filled with nodes. last level can be completely filled or is filled from left to right.
# Perfect BT: all internal node contains 2 children and all leaf nodes are present in the same level.
# Balanced BT: is balanced when the difference between the (hight of lef sub tree - hight of right sub tree) is less than or equal to 1 (height of left and right side of a node with no children both equal -1)
# >>>> starting from the sub tree not the main three, for balanced BT calculation. for node without children, (-1 - (-1)) = 0
# pathological or degenatate BT: every parent node can only contain one child node.

'''Binary search tree'''
# is a binary tree.
# -left subtree should only contain nodes with keys less than node's key.
# -right subtree of a node should only contain nodes with keys greater than node's key
# -lef and right subtree must also be a BST.

# when constructing a BST, start comparing from the root, and follow the rules and compare at every level
# duplicate values in BST: some books, not allowed. others left side, others right side.

'''Operations in a binary search tree'''
# Searching: (1) is the bst empty -(2) root == given value - (3) value < root , if yes, go left. continue for each level until found or not available.

# Inserting at the correct position: if empty, insert normally. go down the level using = and < and find where to place.

# Deletion operation: delete if present or print a message if tree is empty or key not found. search for node if not empty.
#>> if the value is a leaf node, deleting it is simple straightforward
#>> if the node has one child node, the child node takes its place.
#>> if the node has 2 child nodes, replace deleted node with the greatest value in left side or smallest value in right side of its children.


# Traversal a BST: Algorithms
#> pre-order Traversal: visit the root, traverse lef sub tree, traverse right sub tree (perform operation recursively)
#> In-order Traversal: visit left sub tree, visit root, visit right sub tree. (start from the left most leaf node)
#> Post-order Traversal: left s.t, right s.t, root. (start from left most leaf node)
#> level-order Traversal: by level, from left to right, starting from level 0 (root level): aka BFS (Breadth first search) travel algorithm


#IMPLEMENTATION
#Key considerations: key, left child, right child. we are using the concepts of storing references. like a DLL the references stored are those of the children references

class BST:
    def __init__(self, key,):
        self.key = key
        self.lchild = None
        self.rchild = None

#Insertion of new node: check if tree is empty or not, if empty, node will be first and stores no reference.
    def insert(self, data):
        if self.key is None:              # empty node. because initializing the class already causes the tree to have one node. except it was initialized with None.
            self.key = data
            return
        if self.key == data:              #disregarding duplicate values
            return
        if self.key > data:
            if self.lchild:              # then there is a node at the left already
                self.lchild.insert(data)   # continuously compares with the current left node, if smaller, it moves to the next level recursively
            else:
                self.lchild = BST(data)        # when greater, insert the new node.
        else:                                 # if greater than the root node key
            if self.rchild:                     # just the same for lchild, if a node exists
                self.rchild.insert(data)
            else:
                self.rchild = BST(data)

#NB, continuously assigning the references to the children is how we preserve data while updating the references.
# for inserting a list into the tree 
# root = BST(10)  # root value inserted
# list1 = [20, 3, 30, 2, 1]
# for i in list1:
#     root.insert(i)


# Search operations in trees

#compare root key with data, if equal print a message, if smaller, search left sub tree, else search right sub tree.

    def search(self, data):
        if self.key == data:
            print('Node is found')
            return
        if data < self.key:
            if self.key.lchild:
                self.lchild.search(data)
            else:
                print('Node is not present in tree')
        else:
            if self.key.rchild:
                self.rchild.search(data)
            else:
                print('Node is not present in tree')

        
            
 #Traversal Algorithm:

 #Pre-order traversal: printing the order of its traversal
 # Traverasal and printing order: root, left, right

    def preorder(self):
        print(self.key, end=" ")        # notice that print statement has other parameters
        if self.lchild:
            self.lchild.preorder()      #prints the self.key
        if self.rchild:
            self.rchild.preorder()
    

# In order traversal: sorts from ascending order
# left, root, right: from leaf node in left.

    def inorder(self):
        if self.lchild:
            self.lchild.inorder()
        print(self.key)                  # printing the leftmost
        if self.rchild:
            self.rchild.inorder()        # rightmost in current subtree.

#Post order traversal
#left, right, root

    def postorder(self):
        if self.lchild:
            self.lchild.postorder()     #recursive
        if self.rchild:
            self.rchild.postorder()
        print(self.key)                   #self.key in some way denotes the root. we print at the root, we use others to traverse.


 # Deletion operation
 # steps: check if tree is empty, print a message. find node and delete, otherwise print a message.


    def delete(self, data):
        if self.key is None:
            print("Tree is empty")
            return
        if data < self.key:
            if self.lchild:           # To avoid a case when there isn't any lchild reference
                self.lchild = self.lchid.delete(data)    # traversing downwards to find the node, like we did above. This time we assigned the traversal to use in the last else statement.
            else:
                print("Given Node is Not present in the tree")
        elif data > self.key:
            if self.rchild:
                self.rchild = self.rchild.delete(data)
            else:
                print("Given node isn't present in tree")
        else:                                                              #node is the root node since it has gone through left and right. we'll perform the delete operation here
            if self.lchild is None:                   # Deleting starts here. We assigned to lchild to avoid complexity here, self is now pointing to the node we want to delete
                temp = self.rchild                    # if its a leaf node, we want to return the none so that its parent.lchild will be none too. (something to note)
                self = None
                return temp        
            if self.rchild is None:
                temp = self.lchild
                self = None
                return temp                        # the above part will work for both one child and leaf nodes (47)
            

# if it contains 2 children, reasign the key from the children in line with the rule then delete the node
# we are replacing with the smallest value in the right sub tree. i.e self.rchild.lchild (recursively)
            node = self.rchild          # for convention
            while node.lchild:
                node = node.lchild     #find the last lchild, while node has an lchild
            self.key = node.key       #assign the self to the smallest value
            self.rchild = self.rchild.delete(node.key)    # assigning node.key to none while self.key, its smallest child, gets its key value
            return self

# finding the node with the smallest and largest key value
# leftmost: smallest, rightmost: largest.  (if leftnodes are not present, root is smallest)
    def min_node(self):
        current = self
        while current.lchild:
            current = current.lchild
        print("node with smallest key is:", current.key)

# at the onset, self will be pointing to 
    def max_node(self):
        current = self
        while current.rchild:
            current = current.rchild
        print("node with maximum key is :", current.key)

        
#DELETING THE ROOT NODE

# consider if root is a leaf node, contains only one child or two children
    #was written by me, proof check it.
    def delete_root(self):
        if self.key is None:
            print("There is no node within the tree")
            return
        if self.lchild is None:
            if self.rchild is None:
                self.key = None
                return
        if self.lchild:
            temp = self.lchild
            while temp.rchild is not None:
                temp = temp.rchild
            temp = temp.delete_root()
            self.key = temp.key
            temp.key = None
            return
        if self.rchild:
            temp = self.rchild
            while temp.lchild is not None:
                temp = temp.lchild
            temp.delete_root()
            self.key = temp.key
            temp.key = None




# define a count function to find out how many nodes are int the tree

def count(node):                     # a function to count the number of nodes in tree.
    if node is None:
        return 0
    return 1+count(node.lchild) + count(node.rchild)

root = BST(20)
print(count(root))

if count(root) > 1:
    root.delete(10)
else:
    print("can't delete when root node is a leaf node")

# the delete method doesn't work when we are deleting the root or a leaf node child to the root node, we are trying to modify for these conditions
#      def delete(self, data, curr):    #added a variable 'curr'
#         if self.key is None:
#             print("Tree is empty")
#             return
#         if data < self.key:
#             if self.lchild:           # To avoid a case when there isn't any lchild reference
#                 self.lchild = self.lchid.delete(data, curr)    # traversing downwards to find the node, like we did above. This time we assigned the traversal to use in the last else statement.
#             else:
#                 print("Given Node is Not present in the tree")
#         elif data > self.key:
#             if self.rchild:
#                 self.rchild = self.rchild.delete(data, curr)
#             else:
#                 print("Given node isn't present in tree")
#         else:                                                              #node is the root node since it has gone through left and right. we'll perform the delete operation here
#             if self.lchild is None:                   # Deleting starts here. We assigned to lchild to avoid complexity here, self is now pointing to the node we want to delete
#                 temp = self.rchild                    # if its a leaf node, we want to return the none so that its parent.lchild will be none too. (something to note)
                #   if data == curr:
                #     self.key = self.rchild.key     # if root, assign the key of the child to it
                #     self.lchild = temp.lchild      (self.rchild.lchild)   #asign the references to it as well
                #     self.rchild =  temp.rchild     (self.rchild.rchild)     #assign the references to it as well
              #       temp = None                    # deleting the child
                 #     return
#                 self = None
#                 return temp        
#             if self.rchild is None:
#                 temp = self.lchild
             #    if data == curr:
                #     self.key = self.rchild.key     # if root, assign the key of the child to it
                #     self.lchild = temp.lchild      (self.lchild.lchild)   #asign the references to it as well
                #     self.rchild =  temp.rchild     (self.lchild.rchild)     #assign the references to it as well
                #     temp = None                    # deleting the child
                #     return
#                 self = None
#                 return temp                        # the above part will work for both one child and leaf nodes (47)
            

# # if it contains 2 children, reasign the key from the children in line with the rule then delete the node
# # we are replacing with the smallest value in the right sub tree. i.e self.rchild.lchild (recursively)
#             node = self.rchild          # for convention
#             while node.lchild:
#                 node = node.lchild     #find the last lchild, while node has an lchild
#             self.key = node.key       #assign the self to the smallest value
#             self.rchild = self.rchild.delete(node.key, curr)    # assigning node.key to none while self.key, its smallest child, gets its key value
#             return self




'''Binary Heap Data structure'''

# Binary heap is a complete binary tree that satisfies heap properties.
#HEAP:Parent node needs to be less than or equal to, or greater than or equal to its children

# Min Heap: root node is less than or equal to the children. root key is smallest, and recursively true
# Max Heap: root node is greater than or equal to parent. root key is greatest, and recursively true.

#USES: implementing priority queues, used for sorting and finding largest or smallest values.

'''Operations'''
# Heapify: operation performed on binary trees to make them binary heaps (perform heapify after insertion, deletion and binary heap tree creation from an array)
# >>Heapify_up: comparison starting from leaf node to root,
# >>Heapify_down: comparison starting from root to leaf node
# if it is a max heap, it is called max_heapify

# INSERTION
# we add insert to maintain the complete binary heap property, inserting at the first open slot at the lower level
# then we perform heapify_up

# DELETION
# replace the node to delete with the last Node
# delete the last Node
# heapify the tree

# Extracting min and max is just heapifying min or max and taking the root value.

#NB: heap works by moving values in order to achieve its properties.

# Creating a binary tree.
#>> create a complete binary tree, then heapify (start lowest and last parent node in the complete BT, complete that level then upwards )

#Reresenting binary heap with list
#> write values from top to bottom, left to right within the list.i.e root is always at 0 index.
'''ith index can be found using list[i]. parent node = (i-1)/2'''
'''lchild index = (2 * i) +1,  rchild index = (2 * i) + 2'''
def max_heapify(arr, n, i):
    largest = i
    left = 2*i + 1
    right = 2*i +2
    # largest so far, compared with the left
    if left < n and arr[largest]< arr[left]:
        largest = left
    # largest so far, compared with right
    if right < n and arr[largest] < arr[right]:
        largest = right

    #change parent
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]

        #recursive call
        max_heapify(arr, n largest)   #recursively, starting from largest this time
    

arr = [2,3,54,50,12,3]

n = len(arr)

#building max heap
for i in range(n//2 - 1, -1, -1): #half length value minus 1, to -1, decrementing by 1.
    max_heapify(arr, n, i)

#display
print("max heap is ", end=" ")
for i in range(n):
    print(arr[i])




'''using the heapq module in python'''
import heapq

#heappush
# heapq.heappush(heap, item)  # inserting the element to the heap following the min_heap design

heap = []
heapq.heappush(heap, 10)
heapq.heappush(heap, 1)

#heappop: returns the minimum value and deletes it from the heap
heapq.heapop(heap)   #removes 1

#heapify: converts a list of numbers that don't follow the min heap property to a heap.
list1 = [1,2,3,4,5]
heapq.heapify(list1)

#heappushpop: pushes a new value and pops the min value
heapq.heappushpop(list1, 89)

#heapreplace: pops the smallest value and inserts the new value
heapq.heapreplace(list1, 100)

#nsmallest: return n number of smallest numbers in the heap
heapq.nsmallest(2, list1)    # can work on normal heaps as well as lists n=2

#nlargest: returns n number of largest vales
heapq.nlargest(3, list)    # n = 3

#implementing priority queue using the heapq module
list1 = [(1, "ria"), (4, "sia" ), (3, "gia")]
heapq.eapify(list1)
for i in range(len(list1)):
    print(heapq.heappop(list1))    # pops out values based on their priority

#### Watch one video on how to implement heaps from scratch.




'''Graphs'''
# graphs are none linear data structures that comprises nodes and graphs.
# a trees will always be a graph but not all graphs are trees.

# mathematically, G =(V, E)  == ordered pair of edges and vertices.
#{} : if this was used, it would represent 'unordered pair'

#TYPES OF GRAPHS
#> Directed graphs and undirected graphs (bidirectional)
#> weighted graphs and unweighted graphs
#> cyclic graphs and acyclic graphs

#CONCEPTS
#adjacent nodes: if there exists an edge btwn 2 vertex, they are adjacent
# path: sequence of vertices, each connected by an edge. length of path is the sum of all the edges from one vertic to another
# simple path is one in which no vertex is repeating, otherwise it is a complex path
# fully connected graphs: there is a path to every node.
# strongly connected graphs: in directed graphs, there is a part from any other node.
# Node degree: in undirected, degree of a node is the number of nodes connected to it
# Node degree: in-degree: number of edges coming to a node, out-degree: the number of edges leaving a node
# complete graph: there is an edge btwn every pair of nodes in the graph


'''Graph Representation'''
        
# Adjacency Matrix and Adjacency list

# Ajacency Matrix represent the connection between graph nodes in a matrix form
#>>firt create the matrix (n*n) where n is number of nodes in graph, store 1 if there is an edge otherwise 0. if matrix created, think of connection of the form row to column, in case of directed graphs

# in python we can store graphs using nested lists and store nodes in another list



#ADJACENCY LIST

# Store the adjacency list. a list containing all the nodes it is connected to.
#> (1) A:[B, C] (2) B[C, E] and so on.      For weighted graphs A: [(B,5), (C,12)]

# represent adjacency list as dictionaries. i.e {A: [B, C], B: [C, D]}


'''GRAPH OPERATION'''

# Adding a new node to a graph:
# Adding a new edge

# write a function to insert a new node to a graph using adjacency matrix representation
nodes = []   #stores the nodes list
graph = []   # for the graph matrix as nested
node_count = 0     # taking a count of the number of nodes within the graph

def add_node(v):
    global node_count          # so that we can update node_count within our function. Recall, it is a global variable
    if v in nodes:
        print(v,"is already present in the graph")
    else:
        node_count = node_count + 1
        nodes.append(v)
        for n in graph:
            n.append(0)           #append 0 after every column 
            temp = []             # adding a new list to be added as nested within the graph list, for row
            for i in range(node_count):
                temp.append(0)                # using the node count to create the length of zero
            graph.append(temp)


#adding an edge for undirected and unweighted graphs
def add_edge(v1, v2): 
    if v1 not in nodes:                  # checking if nodes are present to start with
        print(v1, 'is not present in the graph')  
    elif v2 not in nodes:
        print(v2, 'is not present in the graph')
    else: 
        index1 = nodes.index(v1)        # get the index of the vi
        index2 = nodes.index(v2)        #index is a method associated with lists
        graph[index1][index2] == 1
        graph[index2][index1] == 1


# adding edge for weighted graphs
def add_edge(v1, v2, cost): 
    if v1 not in nodes:                  # checking if nodes are present to start with
        print(v1, 'is not present in the graph')  
    elif v2 not in nodes:
        print(v2, 'is not present in the graph')
    else: 
        index1 = nodes.index(v1)        # get the index of the vi
        index2 = nodes.index(v2)        #index is a method associated with lists
        graph[index1][index2] == cost
        graph[index2][index1] == cost    # when calling the function, add the cost.

# for directed weighted graphs
def add_edge(v1, v2): 
    if v1 not in nodes:                  # checking if nodes are present to start with
        print(v1, 'is not present in the graph')  
    elif v2 not in nodes:
        print(v2, 'is not present in the graph')
    else: 
        index1 = nodes.index(v1)        # get the index of the vi
        index2 = nodes.index(v2)        #index is a method associated with lists
        graph[index1][index2] == 1     #change 1 to cost, for weigted graph, add cost in argument as well



# A function to print the graph in matrix form
def print_graph():
    for i in range(node_count):       #row loop
        for j in range(node_count):        #asymptotically column loop
            print(graph [i], [j], end=' ')
        print()

# if the values are a mixture of 2 digits and one digits, the matrix won't print well. add the format to print it properly.
def print_graph():
    for i in range(node_count):       #row loop
        for j in range(node_count):        #asymptotically column loop
            print(format(graph [i], [j]), end=' ')        
        print()



# write functions to add a new node and edge to a graph using the adjacency list representation

graph = {}

def add_node(v):
    if v in graph:
        print(v, 'is already present in the graph')
    else:
        graph[v] = []         # adding values in a dictionary


# add an edge using adjacency list (undirected, unweighted)
def add_edge(v1, v2):
    if v1 not in graph:
        print(v1, 'is not in graph')
    elif v2 not in graph:
        print(v1, 'is not present in graph')
    else:
        graph[v1].append(v2)            # indexing the key to add a value to the list it is mapped to 
        graph[v2].append(v1)


# undirected weighted graph
def add_edge(v1, v2, cost):
    if v1 not in graph:
        print(v1, 'is not in graph')
    elif v2 not in graph:
        print(v1, 'is not present in graph')
    else:
        list1 = [v2, cost]          # recall that for weighted, values are nested as (node, weight)
        list2 = [v1, cost]
        graph[v1].append(list1)            # indexing the key to add a value to the list it is mapped to 
        graph[v2].append(list2)


#directed graphs
def add_edge(v1, v2, cost):        # take out cost and list for unweighted.
    if v1 not in graph:
        print(v1, 'is not in graph')
    elif v2 not in graph:
        print(v1, 'is not present in graph')
    else:
        list1 = [v2, cost]          # recall that for weighted, values are nested as (node, weight)
        list2 = [v1, cost]
        graph[v1].append(list1)
        

##DELETION OPERATION

# deleting a node will delete the node and the connections to that node

# delete node using adjacency matrix operation
node_count = len(nodes)
def delete_node(v):
    global node_count         # because we want to make changes to 'node_count'
    if v not in nodes:
        print(v,'is not present in the graph')
    else:
        index1 = nodes.index(v)        # trying to find the index of the node we want to delete
        node_count = node_count-1
        nodes.remove(v)             #remove is a method associated with a list
        graph.pop(index1)           #take out the entire row, the column still remains
        for i in graph:
            i.pop(index1)

        
# delete an edge using the adjacency matric representation

# weighted and unweighted graphs

def delete_edge(v1, v2):
    if v1 not in nodes:
        print(v1, 'is not present in node')
    elif v2 not in nodes:
        print(v2, 'is not present in graph')
    else:
        index1 = nodes.index(v1)
        index2 = nodes.index(v2)
        graph[index1][index2] = 0
        graph[index2][index1] = 0


# for a directed graph, delete the node.
def delete_edge(v1, v2):
    if v1 not in nodes:
        print(v1, 'is not present in node')
    elif v2 not in nodes:
        print(v2, 'is not present in graph')
    else:
        index1 = nodes.index(v1)
        index2 = nodes.index(v2)
        graph[index1][index2] = 0


# Deleting using adjacency list notation.

#for undirected unweghted graphs
def delete_node(v):
    if v not in graph:
        print(v, 'is not present in graph')
    else:
        graph.pop(v)          # deleting from a dictionary
        for i in graph:
            list1 = graph[i]
            if v in list1:
                list1.remove(v)

#deleting for weighted graphs
def delete_node(v):
    if v not in graph:
        print(v, 'is not present in graph')
    else:
        graph.pop(v)          # deleting from a dictionary
        for i in graph:
            list1 = graph[i]
            for j in list1:          # remember weights are represented as nested
                if v == j[0]:         #first value signals the node, last value is weight
                    list1.remove(v)
                    break        


# delete edge from adjacency list

def delete_edge(v1, v2):
    if v1 not in graph:
        print(v1,'is not present in the graph')
    elif v2 not in graph:
        print(v2, 'is not present in graph')
    else:
        if v2 in graph[v1]:
            graph[v1].remove(v2)         #indexing using the dictionary key
            graph[v2].remove(v1)



# deleting an edge from a directed graph
def delete_edge(v1, v2):
    if v1 not in graph:
        print(v1,'is not present in the graph')
    elif v2 not in graph:
        print(v2, 'is not present in graph')
    else:
        if v2 in graph[v1]:
            graph[v1].remove(v2) 



#deleting values in a weighted graph
def delete_edge(v1, v2, cost):
    if v1 not in graph:
        print(v1,'is not present in the graph')
    elif v2 not in graph:
        print(v2, 'is not present in graph')
    else:
        temp = [v1, cost]             # because it is a nested list
        temp1 = [v2, cost]
        if v2 in graph[v1]:
            graph[v1].remove(temp1)
            graph[v2].remove(temp)       # remove this for weighted directed graph


# we can store the number of edges btwn vertices instead of storing 1


'''Graph Traversal algorithms'''

#Depth first search: starting from the starting node. (any node can be the strting node)
#> start from a starting node, visit the starting node, then visit the adjacent node of a, any order. recursively.
#> DFS sticks to one path. when it finishes, it will back track(through its former paths) and begin checking other nodes that are adjacent to the ones it passed

# we can implement dfs algorithm recursively and iteratively performed using stacks

#HOW: push all adjacent nodes into a stack, then pop each and confirm if visited. if visited, push its own adjacent matrix to stack, even if the previous still has some not compared


# implement DFS in an adjacency list using recursion.

# considering that nodes and edges have been added using the adjacency list add_node and add_edge functions.
 
visited = set()       # we defined this outside the function because we want the recursion to call it multiple times.
graph  = {}
add_node('a')
add_node('b')
add_node('c')     
add_edge('a','b')   # this is a graph


#DFS for weighted undirected graphs

def DFS(node, visited, graph):       # asking user to select the starting node
    if node not in graph:
        print("Node is not present in the graph")
        return
    if node not in visited:
        print(node)
        visited.add(node)
        for i in graph[node]:
            DFS(i, visited, graph)           #graph contains the graph, recursively prints the values visited and adds them to the list



# implementing DFS using iterative approach. (using the stack data structure)

def DFSiterative(node, graph):
    visited = set()
    if node not in graph:
        print("Node is not present in the graph")
    stack = []
    stack.append(node)         #push
    while stack:                               # this was added afterwards, so that we can iterate the process until all the elements in the stack are finished. 
        current = stack.pop()                #pop
        if current not in visited:
            print(current)
            visited.add(current)
            for i in graph(current):          # get the adjacent nodes of current
                stack.append(i)
    


'''BREADTH FIRST SEARCH '''
# visiting in level order. a level is defined as the path length from the source node.
# start from level 0 (root node level) and proceed till the final level.
# implemented using a queue. to leverage the first in first out concept to add the children of the node

adj_list = {
    "A": ["B", "D"],
    "B": ["A", "V"],
    "C": ["A", "E", "F"],
    "D": ["A", "E", "F"]
}

from queue import Queue

visited = {}           # to keep track of all visited node
level = {}            # to keep track of the levels
parent = {}           # to keep track of the parents of the nodes
bfs_traversal_output = [] 
queue = Queue()

for node in adj_list.keys():
    visited[node] = False      # initializing the default values for each node
    parent[node]  = None        # initializing the default values for each node
    level[node]  = -1       # initializing the default values for each node, this could be infinity

# at this point all the nodes are set to false, i.e they haven't been visited, we also haven't assigned levels hence the -1
# defining our source node
s = "A"
visited[s] = True
level[s] = 0
queue.put(s)

#for others
while not queue.empty():
    u = queue.get()        #pops the first element in queue
    bfs_traversal_output.append(u)

    for v in adj_list[u]:
        if not visited[v]:
            visited[v] = True           #changing its value to true
            parent[v] = u               #assigning it a parent
            level[v] = level[u] + 1     #assiging it a level
            queue.put(v)                # using a queue to process the adjacent nodes

print(bfs_traversal_output)


# find the shortest distance btwn nodes using the leve

print(level['D'])

# find the shortest path to any node from the source node
v = "G"
path = []
while v is not None:
    path.append(v)
    v = parent[v]
path.reverse()          # reverses the list from last to first. (inbuilt to the list method.)
print(path)




"""HASHING"""   # they are also known as dictionaries

#converting a data of any length to a fix length array.
#hash requires, input data, hash function to produce the hash value.
# the hash function can be any function. most important considerationis collistion
# collision handling methods are: Separate chaining, Open Addressing (Linear probing, Quadratic probine, Double hashing)

'''Methods'''
#separate chaining: using linked list to link colliding values from our hash table.
#Open adressing: Linear probing: if there is a collision, add 1 to the value, and recalculate, map to h1. (h0=number, h1=number +1, ...)
#Open adressing: Quadratic probing: instead of h1 being (number + 1) the added number is powered.
# Double hashing uses 2 hash functions, for calculating h1, we add to just 1 of the

# hash values should be immutable. use tuples instead of lists. 

city_map = {}
cities = ['calgary', 'Vancouver', 'Toronto']
city_map['Canada'] = []   # this is done because we want to pass a list as values, initialize first
city_map["Canada"] += cities
# working with hashmaps, they are plainly dictionaries
# .keys(), .values() and .items()

#E.g. Given an array of strings, group the anagrams together, anagrams are words containing the same letters.

## Method1
from collections import defaultdict
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagram_map = defaultdict(list)
        result = []

        for s in strs:
            sorted_s = tuple(sorted(s))    # sorted returns a list, keys must be immutable
            anagram_map[sorted_s].append(s) # we are appending to a list

        for value in anagram_map.values():
            result.append(value)

        return value
    
#using a normal dictionary
from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagram = {}
        result = []

        for s in strs:
            sorted_s = tuple(sorted(s))
            if sorted_s in anagram:
                anagram[sorted_s].append(s)
            else:
                anagram[sorted_s] = [s]

        for a in anagram.values():
            result.append(a)

        return result




'''Big Notation time complexity'''

# O of 1: the time complexity doesn't grow with data size. eg adding to the end of a row, indexing
# O of n: time complexity is proportional to size. eg, searching, looping
# O of n2: time complexity increase by squared. eg nested loops (2). (bubblesort, insertionsorts)
# O of n *m: time complexity when array isn't squared for nested loop of amount = 2.
# O of logn: binary search. or heap operations. logn is much more efficient than n.
# O of nlogn: sorting algorithms, mergesort, quick sort etc.

'''RECURSION'''

# Iterative function
def walk(steps):
    for step in range(1, steps + 1):
        print(f"you take steps #{step}")
walk = 100
#Recursive version
def walk(steps):
    if steps == 0:                # if not it goes into negative numbers
        return
    walk(steps - 1)
    print(f'You take steps #{steps}')

walk = 100

# recursion walks like stacking multiple function calls like the stack module. there is a max it can go tho.
# recursive functions are slower but useful in DSA

# eg. defining a factorial function recursively and iteratively.
def factorial(x):
    result = 1
    if x > 0:
        for y in range(1, x+1):
            result = result * y  #result *= y      is the same thing
        return result
    

# Recursive approach
def factorial(x):
    if x == 1:
        return 1
    else: 
        return x * factorial(x-1)


'''SORTING ALGORITHMS'''

# Insertion sort
# take each values and sort one after the other by comparing it with others before it until a perfect position is found.
# it works with nested loops and is O(n2) in complexity
A = [1,3,5,2,3,6,1]
def insertion_sort(A):
    for i in range(1, len(A)): # looping through the elements in the list
        for j in range(i-1, 0, -1):     #loops from the element before i to the zeroth element (useful for comparing i with other elements before it, to find where to place i)
            if A[j] > A[j + 1]:         # iteratively comparing the element with the one before it, if bigger, they swap positions
                A[j], A[j+1] = A[j+1], A[j]
            else:
                break

# using a while loop
def insertion_sort(A):
    for i in range(1, len(A)):
        j = i-1
        while A[j] > A[j+1]:
            A[j], A[j+1] = A[j+1], A[j]
            j -= 1                       # Decrement

# same thing but a faster way to implement
def insertion_sort(A):
    for i in range(1, len(A)):
        curNum = A[i]
        for j in range(i-1, 0, -1):
            if A[j] > curNum:
                A[j+1] = A[j]
            else:
                A[j + 1] = curNum
                break



# Selection Sort
# finds the min value in the list and exchange with the first element. find the next min and exchanges with the second value
def selection_sort(A):
    for i in range(0, len(A)-1):         # length of list. this way because we want to start count from 0
        minIndex = i
        for j in range(i+1, len(A)-1):
            if A[j] < A[minIndex]:
                minIndex = j
        if minIndex != i:
            A[i], A[minIndex] = A[minIndex], A[i]


#Bubble Sort
# compares first two values and swaps if pre is greater than post, incrementally and iteratively. after going through the list, it starts again and again until all is sorted.
def bubbleSort(A):
    for i in range(0, len(A)-1-i):     # -i because based on the algorithm, the last value will always be sorted.
      for j in range(len(A)-1-i):     # if you're taking two values, range is -1 and the last is already sorted, hence -i. Also since we are comparing 2, j shouldn't reach the end
        if A[j] > A[j+1]:
            A[j], A[j+1] = A[j+1], A[j]    
    return A

#Merge Sort
# break list into two, then break the half in two continuously until we have only one element in each break, then compare elements in first break with those in second.
#  append the smaller to a sub main list and compare. creat bigger submain until you have compared all the values.
# it is O(nlogn)

def merge_sort(A):
    merge_sort2(A, 0, len(A)-1)

def merge_sort2(A, first, last):
    if first < last:               #first is 0, last is len(A)-1, basically saying if there are more than one element in list break further
        middle = (first + last) // 2
        merge_sort2(A, first, middle) # first half
        merge_sort2(A, middle + 1, last)
        merge(A, first, middle, last)

def merge(A, first, middle, last):
    L = A[first:middle]
    R = A[middle:last + 1]
    L.append(9999999)             # large value to denote end of halved list
    R.append(9999999)             
    i = j = 0                   # initializing the indexes
    for k in range(first, last + 1):    # full length range of list
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1





# QuickSort
#pick a value and compare other values with it. all smaller values are sent to the left while all bigger to the right. this is performed recursively on both left and right until complete sort is achieved.

def quick_sort(A):
    quick_sort2(A, 0, len(A)-1)

def quick_sort2(A, low, hi):
    if low < hi:
        p = partition(A, low, hi)
        quick_sort2(A, low, hi)
        quick_sort2(A, p + 1, hi)

def get_pivot(A, low, hi):     # selected 3 values, hi, mid, and low. we want to find the most median of them by comparing them
    mid = (hi + low) // 2
    pivot = hi
    if A[low] < A[mid]:
        if A[mid] < A[hi]:
            pivot = mid
    elif A[low] < A[hi]:
        pivot = low
    return pivot

def partition(A, low, hi):
    pivotIndex = get_pivot(A, low, hi)
    pivotValue = A[pivotIndex]
    A[pivotIndex], A[low] = A[low], A[pivotIndex]
    border = low

    for i in range(low, hi + 1):
        if A[i] < pivotValue:
            border += 1             # pushes the pivot value up the index
            A[i], A[border] = A[border], A[i]
    A[low], A[border] = A[border], A[low]
    return (border)



'''Trie Data Structure'''
# is a prefix tree used to store strings. used for autocomplete.
# words are inserted as nodes.build one adjacent nodes for each until the word is formed.
# apple and ape. we can use the apple trie to create the ape trie, just add another node after 'ap' for node 'e' to make
# we also mark the end of words with True.

class TrieNode:
    def __init__(self):
        self.children = {}                # root is a word identifier, children are the letters that make up the word
        self.endofWord = False

class Trie:
    def __init__(self):
        self.root = TrieNode()    

    def insert(self, word: str) -> None:
        cur = self.root
        for c in word:
            if c not in cur.children:
                cur.children[c] = TrieNode()   # create a node for child
            cur = cur.children[c]             # store value in cur
        cur.endofWord= True

    def search(self, word: str) -> bool:
        cur =  self.root
        for c in word:
            if c not in cur.children:
                return False
            cur = cur.children[c]        # if letter in word is available in our trie, we point curr to it, we keep going down until the end of word
        return cur.endofWord            # end of word is true of false. if true, there is consecutive node connection for every letter in the word, and the end is marked as end.
    
    def startswith(self, prefix:str) -> bool:
        cur = self.root
        for c in prefix:
            if c not in cur.children:           # goes through the word and returns true if there is consecutive node connection for it from start. even if it isn't registered as end of word.
                return False
            cur = cur.children[c]
        return True
    

'''Memoization or Top-Down dynamic programming'''

# for recursive functions, store the values for previous calls so that future calls won't have to repeat the work.
    
# simple recursive fibonacci fuction
def fibonacci(n):
    if n == 1:
            return 1
    elif n==2:
            return 1
    elif n>2:
            return fibonacci(n-1) + fibonacci(n)
    
#usage
# for n in range(1, 101):
#     print(n, ':', fibonacci(n))

# to slow because it calls itself, which calls itself, which calls itself, continuously.

# we can use memoization to speed up its implementation.
# memoization implementation
fibonacci_cache = {}
def fibonacci(n):
    # if we have cached the value, then return it
    if n in fibonacci_cache[n]:
        return fibonacci_cache[n]
    
    #compute the nth term
    if n == 1:
        value == 1
    elif n==2:
        value == 1
    elif n>2:
        value == fibonacci(n-1) + fibonacci(n)
    #cache the value and return it
    fibonacci_cache[n] = value
    return value

#usage
# for n in range(1, 101):
#     print(n, ':', fibonacci(n))

# method 2: implementing memoization
def fib_memoized(n):
    def fib(n):
        if n <= 1:
            return n
        else:
            return fib_memoized(n-1) + fib_memoized(n-2)
    cache = {}
    if n not in cache:
        cache[n] = fib(n)
    return cache[n]



#Using python built in lru_cache module for memoization
from functools import lru_cache

@lru_cache(maxsize=1000)
def fibonacci(n):
    if n == 1:
            return 1
    elif n==2:
            return 1
    elif n>2:
            return fibonacci(n-1) + fibonacci(n)
    
#usage
# for n in range(1, 101):
#     print(n, ':', fibonacci(n))


'''Tabulation or Bottom-up dynamic programming'''

# using tables to store previously processed values

# code
def fibonacci_tabulation(n):
    if n <= 1:
        return n

    # Initialize a table to store Fibonacci numbers
    fib_table = [0] * (n + 1)         # creates a list of n+1 values, each initialized as zero
    fib_table[1] = 1                       # initialize the first value to 1

    # Fill up the table iteratively
    for i in range(2, n + 1):                   # to avoid first two values.
        # this is tabulation. the stored value within the list, are -1 and -2, they have been calculated and they will be used to calculate the next values.
        fib_table[i] = fib_table[i - 1] + fib_table[i - 2]   # we use minus 1 and 2 because we want to start our sum from the first elements.

    return fib_table[n]




# Example usage:
n = 10
result = fibonacci_tabulation(n)
print(f"The {n}-th Fibonacci number is: {result}")


# Example: finding the minimum number of coins to make a change using Tabulation.

def min_coins_dynamic_programming(coins, amount):
    # Create a table to store the minimum number of coins for each amount
    dp = [float('inf')] * (amount + 1)                                       # list should store infinity equals to the amount + 1 value
    dp[0] = 0  # Base case: 0 coins needed to make change for amount 0

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1

# Example usage:
coin_denominations = [25, 10, 5, 1]
change_amount = 63

result = min_coins_dynamic_programming(coin_denominations, change_amount)
if result != -1:
    print(f"Minimum number of coins to make change: {result}")
else:
    print("Change cannot be made with the given coin denominations.")


# bottom up approach, dynamic programming


"""Greedy algorithm implementation"""       # complexity -- if unsorted: O(nlogn), if sorted:O(n)

#When to use greedy algorithms. 
#> when a global optimum can be arrived at by selecting local optimums, 
#> when the optimal solution can be composed of optimal solutions of subproblems.

#Problem: given n activities with their start and finish time, select the max number of activites a person can perform.
#> constraints: Only one activity can be performed per time.

#greedy solution:
 #> 1, sort the activities according to finish time, select the first activity and print, (next: if the start time of the other activity is 
 #> greater than or equal to the finish time of the current activity, print activity)

 def activity_selection(start_times, finish_times):
    n = len(start_times)

    # Create a list of tuples (start_time, finish_time, activity_index)
    activities = [(start_times[i], finish_times[i], i) for i in range(n)]

    # Sort activities based on finish times
    activities.sort(key=lambda x: x[1])

    selected_activities = []
    selected_activities.append(activities[0])

    # Iterate through the sorted activities and select non-overlapping ones
    for i in range(1, n):
        current_activity = activities[i]
        last_selected_activity = selected_activities[-1]

        if current_activity[0] >= last_selected_activity[1]:
            selected_activities.append(current_activity)

    # Extract the indices of selected activities
    selected_indices = [activity[2] for activity in selected_activities]

    return selected_indices

# Example usage:
start_times = [1, 3, 0, 5, 8, 5]
finish_times = [2, 4, 6, 7, 9, 9]

result = activity_selection(start_times, finish_times)
print("Maximum number of activities:", len(result))
print("Selected activity indices:", result)



# Greedy algorithm solution to find the minimum number of coins

def min_coins(coins, amount):
    coins.sort(reverse=True)  # Sort the coins in descending order

    num_coins = 0
    i = 0

    while amount > 0 and i < len(coins):
        if coins[i] <= amount:
            # Take as many coins of the current denomination as possible
            num_coins += amount // coins[i]   # same as num_coins = num_coins + (amount // coins[i] )
            amount %= coins[i]                # same as amount = amount % coins[i]
        i += 1

    if amount == 0:
        return num_coins
    else:
        # If amount is not zero, it means it cannot be represented with the given coins
        return -1

# Example usage:
coin_denominations = [25, 10, 5, 1]
change_amount = 63

result = min_coins(coin_denominations, change_amount)
if result != -1:
    print(f"Minimum number of coins to make change: {result}")
else:
    print("Change cannot be made with the given coin denominations.")



"""BackTracking"""

# it is used when we want to find all the possible solutions to a particular problem.
#> it represents the information as a tree using DFS method. eg in how many ways can 2 boys and 
#> one girl seat on tree chairs such that the girl cannot be in the middle. create a tree of all possible ways and cancel those with a girl at middle.

#solution to the 2 boys, 1 girl problem (this generates all possible permutuations, solve the one for when girl must be in the middle)
def print_solution(perm):
    print(" ".join(perm))

def is_valid(perm):
    # In this example, any arrangement is considered valid
    return True

def arrange_boys_and_girl(perm, choices):
    if len(perm) == len(choices):
        # All positions are filled, print the solution
        print_solution(perm)
        return

    for person in choices:
        if person not in perm:
            # Add the person to the current arrangement
            perm.append(person)

            # Check if the current arrangement is valid
            if is_valid(perm):
                # Recur to fill the next position
                arrange_boys_and_girl(perm, choices)

            # Backtrack: Remove the person and try other possibilities
            perm.pop()

# Example usage:
boys_and_girl = ['Boy1', 'Boy2', 'Girl']
arrange_boys_and_girl([], boys_and_girl)


#NB: if we want the most optimal solution, we'll use dynamic programming. Greedy method is also used to find optimal solutions


#EG: we have a board with 4 rows and 4 columns, we want to place 4 queens to avoid them being in same row, same column or same diagonal
#> we want to find out all possible solutions: we can draw the tree and use bonding function (while drawing the tree) to cancel any path that breaks the rule

# Solution n-queens (for diagonal from left to right, row index - col index = -1) (for diagonal from right to left, col index + row index = 2)

class Nqueens:
    def totalNQueens(self, n: int) -> int:
        column = set()
        positiveDiagonal = set()    # (row + column) is constant
        negativeDiagonal = set()    # (row - column) is constant

        result  = 0
        def backtrack(r):
            if r == n:
                nonlocal result       # non local is the opposite of 'Global' we want to make a variable global within a function
                result += 1
                return
            for c in range(n):
                if c in column or (r + c) in positiveDiagonal or (r - c) in negativeDiagonal:
                    continue
                column.add(c)
                positiveDiagonal.add(r + c)
                negativeDiagonal.add(r - c)
                backtrack(r + 1)
                column.remove(c)
                positiveDiagonal.remove(r + c)
                negativeDiagonal.remove(r - c)
            backtrack(0)
            return result
"""Dijkstra's Algorithm"""

# Used to find the shortest path length in a graph.

# In a case where links are costed, when there is no direct path from our start node, we those other nodes to infinity
# Dijkstra's algorithm doesn't consider negative costed links

class Solution:
    def shortestPath(self, n: int, edges: List[List[int]], src: int) -> Dict[int, int]:
        adj = {}
        for i in range(n):   # number of nodes
            adj[i] = []

        for s, d, weight in edges:      #source, destination and weight
            adj[s].append([d, weight])

        shortest = {}    #Map vertex -> distance of shortest path
        minHeap = [[0, src]]    #src is starting node
        while minHeap:
            w1, n1 = heapq.heapop(minHeap)
            if n1 in shortest:
                continue
            shortest[n1] = w1

            for n2, w2 in adj[n1]:
                if n2 not in shortest:
                    heapq.heappush(minHeap, [w1 + w2, n2])

        for i in range(n):
            if i not in shortest:
                shortest[i] = -1
        return shortest
