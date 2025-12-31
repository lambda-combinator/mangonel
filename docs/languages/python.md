# Python: The Language for Tools and Scripts

Python is used throughout Centurion for scripting, data processing, and tools like the RISC-V assembler and linker. This guide covers Python fundamentals and then focuses on its use in Centurion.

## Table of Contents
1. [Language Fundamentals](#language-fundamentals)
2. [Basic Data Types](#basic-data-types)
3. [Control Flow](#control-flow)
4. [Functions](#functions)
5. [Classes and Objects](#classes-and-objects)
6. [File I/O and Data Processing](#file-io-and-data-processing)
7. [Modules and Packages](#modules-and-packages)
8. [Advanced Features](#advanced-features)
9. [Centurion Tools: Assembler, Linker, and Testbenches](#centurion-tools-assembler-linker-and-testbenches)

---

## Language Fundamentals

### What is Python?

Python is a high-level, interpreted language designed for readability and productivity. It's widely used for:
- **Scripting**: Automating tasks
- **Data processing**: Reading, parsing, transforming data
- **Tools**: Building compilers, assemblers, linkers
- **Testing**: Hardware testbenches with cocotb

### Running Python

```bash
# Interactive shell
python3

# Run a script
python3 script.py

# Run code directly
python3 -c "print('Hello, World!')"

# Check version
python3 --version
```

### Comments and Style

```python
# This is a single-line comment

# Multiple lines can have comments
# stacked like this

"""
This is a multi-line string or docstring.
Used for module/function documentation.
"""

def my_function():
    """Docstring: explains what this function does."""
    pass

# Python style: snake_case for variables/functions, UPPER_CASE for constants
my_variable = 42
MY_CONSTANT = 255
def process_data(input_file):
    pass
```

---

## Basic Data Types

### Numbers

```python
# Integers (no size limit in Python 3)
a = 42
b = -100
c = 0

# Hexadecimal, binary, octal
hex_val = 0xFF        # 255
bin_val = 0b1010_1100 # 172 (binary)
oct_val = 0o777       # 511 (octal)

# Floating point
pi = 3.14159
e = 2.71828e0
tiny = 1e-10

# Common operations
sum_val = 10 + 20
diff = 100 - 30
prod = 5 * 6
quotient = 20 / 3      # 6.666... (float division)
int_quotient = 20 // 3 # 6 (integer division)
remainder = 20 % 3     # 2 (modulo)
power = 2 ** 10        # 1024 (exponentiation)

# Bit operations
a = 0b1100
b = 0b1010
a_and_b = a & b        # 0b1000 (8)
a_or_b = a | b         # 0b1110 (14)
a_xor_b = a ^ b        # 0b0110 (6)
not_a = ~a             # Bitwise NOT (inverts all bits)
shift_left = a << 2    # 0b110000 (48)
shift_right = a >> 1   # 0b0110 (6)
```

### Strings

```python
# String literals (single or double quotes)
msg1 = 'Hello'
msg2 = "World"
msg3 = """Multi-line
string literal"""

# Escape sequences
newline = "Line 1\nLine 2"
tab = "Col1\tCol2"
backslash = "Path: C\\Users\\Documents"

# String operations
greeting = "Hello" + " " + "World"  # Concatenation
repeated = "Ha" * 3                 # "HaHaHa"
length = len("Python")              # 6
char = "Python"[0]                  # 'P' (indexing)
substring = "Python"[1:4]           # 'yth' (slicing)

# Formatting strings (multiple ways)
name = "Alice"
age = 30

# f-string (modern, recommended)
msg = f"Name: {name}, Age: {age}"
hex_formatted = f"Hex: {255:08x}"   # "Hex: 000000ff"
bin_formatted = f"Binary: {12:08b}" # "Binary: 00001100"

# .format() method
msg = "Name: {}, Age: {}".format(name, age)

# % operator (older, still used sometimes)
msg = "Name: %s, Age: %d" % (name, age)

# String methods
"HELLO".lower()        # "hello"
"hello".upper()        # "HELLO"
"a,b,c".split(",")     # ["a", "b", "c"]
["a", "b", "c"].join(", ")  # "a, b, c"
"  text  ".strip()     # "text" (remove whitespace)
"hello".startswith("he")     # True
"hello".endswith("lo")       # True
"hello".replace("l", "L")    # "heLLo"
```

### Lists

```python
# Creating lists
numbers = [1, 2, 3, 4, 5]
mixed = [42, "hello", 3.14, True]
empty = []

# Indexing and slicing
numbers[0]              # 1 (first element)
numbers[-1]             # 5 (last element)
numbers[1:3]            # [2, 3] (slice from index 1 to 2)
numbers[:3]             # [1, 2, 3] (first 3)
numbers[2:]             # [3, 4, 5] (from index 2 to end)
numbers[::2]            # [1, 3, 5] (every 2nd element)
numbers[::-1]           # [5, 4, 3, 2, 1] (reversed)

# Adding and removing
numbers.append(6)       # [1, 2, 3, 4, 5, 6]
numbers.insert(0, 0)    # [0, 1, 2, 3, 4, 5, 6]
numbers.extend([7, 8])  # [0, 1, 2, 3, 4, 5, 6, 7, 8]
numbers.remove(3)       # Removes first occurrence of 3
popped = numbers.pop()  # Returns and removes last element

# Length and membership
len(numbers)            # Number of elements
2 in numbers            # True (membership test)
10 not in numbers       # True

# Sorting and reversing
sorted([3, 1, 4, 1, 5])  # [1, 1, 3, 4, 5] (returns new list)
[3, 1, 4].sort()         # Sorts in place
[1, 2, 3].reverse()      # Reverses in place

# List comprehensions (powerful!)
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]
hex_list = [hex(x) for x in [1, 16, 255]]     # ['0x1', '0x10', '0xff']
```

### Dictionaries (Hash Maps)

```python
# Creating dictionaries
student = {
    "name": "Alice",
    "age": 20,
    "gpa": 3.8
}
empty = {}

# Accessing values
student["name"]         # "Alice"
student.get("age")      # 20
student.get("missing", "N/A")  # "N/A" (default value)

# Adding and modifying
student["major"] = "Computer Science"
student["age"] = 21

# Removing
del student["major"]
student.pop("age")      # Removes and returns value

# Iteration
for key in student:
    print(key, student[key])

for key, value in student.items():
    print(f"{key}: {value}")

# Membership test
"name" in student       # True
"email" not in student  # True

# Keys, values, items
list(student.keys())    # ["name", "age", "gpa"]
list(student.values())  # ["Alice", 20, 3.8]
list(student.items())   # [("name", "Alice"), ("age", 20), ("gpa", 3.8)]

# Dictionary comprehension
hex_dict = {i: hex(i) for i in range(5)}
# {0: '0x0', 1: '0x1', 2: '0x2', 3: '0x3', 4: '0x4'}
```

### Tuples (Immutable Sequences)

```python
# Creating tuples
coords = (10, 20)
point_3d = (1, 2, 3)
single = (42,)  # Single element needs comma

# Accessing (like lists)
coords[0]               # 10
coords[1]               # 20

# Cannot modify (immutable)
# coords[0] = 5  # ERROR!

# Useful for multiple return values
def divide(a, b):
    return a // b, a % b

quotient, remainder = divide(17, 5)  # Unpacking tuple

# Named tuples (more readable)
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
p.x                     # 10
p.y                     # 20
```

### Sets (Unique, Unordered)

```python
# Creating sets
numbers = {1, 2, 3, 4, 5}
unique = set([1, 1, 2, 2, 3])  # {1, 2, 3}
empty = set()  # {} is dict, use set()

# Set operations
numbers.add(6)
numbers.remove(3)       # Error if not present
numbers.discard(10)     # No error if not present
numbers.clear()

# Set math
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
a & b               # {3, 4} (intersection)
a | b               # {1, 2, 3, 4, 5, 6} (union)
a - b               # {1, 2} (difference)
a ^ b               # {1, 2, 5, 6} (symmetric difference)

# Membership and size
3 in a              # True
len(a)              # 4
```

---

## Control Flow

### if, elif, else

```python
age = 25

if age < 13:
    print("Child")
elif age < 18:
    print("Teenager")
elif age < 65:
    print("Adult")
else:
    print("Senior")

# One-line if (ternary operator)
status = "Adult" if age >= 18 else "Minor"

# Multiple conditions
if age > 18 and age < 65:
    print("Working age")

if x < 0 or x > 100:
    print("Out of range")

if not (x % 2 == 0):  # Equivalent to: if x % 2 != 0:
    print("Odd number")
```

### for Loops

```python
# Loop over a list
for item in [1, 2, 3, 4]:
    print(item)

# Loop with index
for i in range(5):      # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 8):   # 2, 3, 4, 5, 6, 7
    print(i)

for i in range(0, 10, 2):  # 0, 2, 4, 6, 8 (step by 2)
    print(i)

# Enumerate (get index and value)
for idx, val in enumerate(['a', 'b', 'c']):
    print(f"Index {idx}: {val}")

# Dictionary iteration
data = {"name": "Bob", "age": 30}
for key, value in data.items():
    print(f"{key} = {value}")

# Nested loops
for i in range(3):
    for j in range(3):
        print(f"({i}, {j})", end=" ")

# break and continue
for i in range(10):
    if i == 3:
        continue  # Skip rest of iteration
    if i == 7:
        break     # Exit loop
    print(i)
```

### while Loops

```python
count = 0
while count < 5:
    print(count)
    count += 1

# Loop until condition
while True:
    user_input = input("Enter 'quit' to exit: ")
    if user_input == 'quit':
        break
    print(f"You entered: {user_input}")

# While with else (runs if no break)
i = 0
while i < 5:
    if i == 10:
        break
    i += 1
else:
    print("Loop completed without break")
```

---

## Functions

### Function Definition

```python
def greet(name):
    """Greet someone by name."""
    print(f"Hello, {name}!")

greet("Alice")

# Return values
def add(a, b):
    """Return the sum of two numbers."""
    return a + b

result = add(5, 3)  # 8

# Multiple return values
def divide_and_remainder(a, b):
    return a // b, a % b

quotient, remainder = divide_and_remainder(17, 5)
```

### Default Arguments

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Bob")                          # "Hello, Bob!"
greet("Alice", greeting="Hi")         # "Hi, Alice!"

# Mutable defaults are dangerous!
def append_to_list(item, lst=[]):
    lst.append(item)
    return lst

append_to_list(1)           # [1]
append_to_list(2)           # [1, 2] -- oops!

# Better:
def append_to_list(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### Variable Arguments

```python
# *args: variable positional arguments
def sum_all(*args):
    total = 0
    for num in args:
        total += num
    return total

sum_all(1, 2, 3, 4, 5)  # 15

# **kwargs: variable keyword arguments
def print_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(f"{key} = {value}")

print_kwargs(name="Alice", age=30, city="NYC")

# Combining
def flexible(*args, **kwargs):
    print("Positional:", args)
    print("Keyword:", kwargs)

flexible(1, 2, 3, name="Bob", count=5)
```

### Lambda Functions (Anonymous)

```python
# Simple one-liner functions
square = lambda x: x ** 2
square(5)  # 25

# Often used with map, filter, sorted
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))  # [1, 4, 9, 16, 25]
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]
sorted([3, 1, 4], key=lambda x: -x)  # [4, 3, 1] (descending)
```

### Documentation and Type Hints

```python
def process_data(filename: str, verbose: bool = False) -> dict:
    """
    Process a data file and return results.
    
    Args:
        filename: Path to the input file
        verbose: Whether to print progress
    
    Returns:
        Dictionary with processed results
    """
    data = {}
    if verbose:
        print(f"Processing {filename}")
    return data

# Type hints help with IDE autocomplete and static analysis
def add(a: int, b: int) -> int:
    return a + b
```

---

## Classes and Objects

### Basic Class Definition

```python
class Counter:
    """A simple counter."""
    
    def __init__(self, start=0):
        """Initialize the counter."""
        self.value = start
    
    def increment(self):
        """Increase counter by 1."""
        self.value += 1
    
    def get(self):
        """Return current value."""
        return self.value

# Usage
counter = Counter(10)
counter.increment()
print(counter.get())  # 11
```

### Methods and Properties

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        """Calculate area."""
        return self.width * self.height
    
    def perimeter(self):
        """Calculate perimeter."""
        return 2 * (self.width + self.height)
    
    @property
    def is_square(self):
        """Check if rectangle is a square."""
        return self.width == self.height
    
    def __str__(self):
        """String representation."""
        return f"Rectangle({self.width}x{self.height})"

rect = Rectangle(10, 20)
print(rect.area())      # 200
print(rect.perimeter()) # 60
print(rect.is_square)   # False
print(rect)             # Rectangle(10x20)
```

### Inheritance

```python
class Shape:
    def __init__(self, color):
        self.color = color
    
    def describe(self):
        return f"A {self.color} shape"

class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)  # Call parent __init__
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def describe(self):
        parent_desc = super().describe()  # Call parent method
        return f"{parent_desc} with radius {self.radius}"

circle = Circle("red", 5)
print(circle.describe())  # A red shape with radius 5
print(circle.area())      # 78.54975
```

---

## File I/O and Data Processing

### Reading Files

```python
# Read entire file into string
with open('file.txt', 'r') as f:
    content = f.read()

# Read line by line
with open('file.txt', 'r') as f:
    for line in f:
        line = line.strip()  # Remove newline
        process(line)

# Read into list of lines
with open('file.txt', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    print(f"Line {i}: {line}")
```

### Writing Files

```python
# Write to file (overwrites)
with open('output.txt', 'w') as f:
    f.write("Hello, World!\n")
    f.write("Line 2\n")

# Append to file
with open('output.txt', 'a') as f:
    f.write("Line 3\n")

# Write multiple lines
lines = ["line 1", "line 2", "line 3"]
with open('output.txt', 'w') as f:
    f.writelines([line + '\n' for line in lines])
```

### Binary Files

```python
# Read binary
with open('data.bin', 'rb') as f:
    bytes_data = f.read()

# Write binary
with open('output.bin', 'wb') as f:
    f.write(b'\x00\x01\x02\x03')
    f.write(bytes([0xFF, 0xFE, 0xFD]))

# Convert bytes to int
data = b'\x12\x34\x56\x78'
value = int.from_bytes(data, byteorder='big')     # 0x12345678
value = int.from_bytes(data, byteorder='little')  # 0x78563412

# Convert int to bytes
value = 0x12345678
data = value.to_bytes(4, byteorder='big')     # b'\x12\x34\x56\x78'
data = value.to_bytes(4, byteorder='little')  # b'\x78\x56\x34\x12'
```

### JSON (Common Data Format)

```python
import json

# Parse JSON string
json_str = '{"name": "Alice", "age": 30, "items": [1, 2, 3]}'
data = json.loads(json_str)
print(data["name"])  # "Alice"

# Create JSON string
data = {"name": "Bob", "age": 25}
json_str = json.dumps(data)
json_pretty = json.dumps(data, indent=2)

# Read/write JSON files
with open('data.json', 'r') as f:
    data = json.load(f)

with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)
```

---

## Modules and Packages

### Importing

```python
# Import entire module
import math
print(math.pi)
print(math.sqrt(16))

# Import specific functions
from math import pi, sqrt
print(pi)
print(sqrt(16))

# Import with alias
import numpy as np
from matplotlib.pyplot import plot as plt_plot

# Import all (generally avoid)
from os import *

# Relative imports (in packages)
from . import sibling_module
from .. import parent_module
```

### Useful Standard Modules

```python
# os: operating system operations
import os
os.getcwd()              # Current directory
os.listdir('.')          # List files
os.path.exists('file')   # Check if file exists
os.makedirs('dir', exist_ok=True)  # Create directories
os.path.join('dir', 'file')        # OS-independent path joining

# sys: system-specific parameters and functions
import sys
sys.argv                 # Command line arguments
sys.exit(1)              # Exit program with code 1
sys.path                 # Module search paths

# subprocess: run external programs
import subprocess
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
print(result.stdout)
print(result.returncode)

# re: regular expressions
import re
pattern = r'[0-9]+'
text = "There are 123 apples"
match = re.search(pattern, text)
if match:
    print(match.group())  # "123"

numbers = re.findall(r'[0-9]+', "I have 3 cats and 5 dogs")
# ["3", "5"]

# csv: comma-separated values
import csv
with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)  # Each row is a dict

# collections: specialized containers
from collections import defaultdict, Counter
freq = Counter("aabbbc")  # {'a': 2, 'b': 3, 'c': 1}

# itertools: iteration tools
from itertools import combinations, permutations
list(combinations([1, 2, 3], 2))  # [(1,2), (1,3), (2,3)]
```

---

## Advanced Features

### Exception Handling

```python
# Try-except
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"Unexpected error: {e}")

# Try-except-else
try:
    num = int(input("Enter a number: "))
except ValueError:
    print("That's not a number!")
else:
    print(f"You entered {num}")

# Try-except-finally
try:
    f = open('file.txt', 'r')
    content = f.read()
except FileNotFoundError:
    print("File not found")
finally:
    f.close()  # Always executes

# Raising exceptions
def validate_age(age):
    if age < 0 or age > 150:
        raise ValueError("Invalid age")
    return age

# Custom exceptions
class CustomError(Exception):
    pass

try:
    raise CustomError("Something went wrong")
except CustomError as e:
    print(f"Caught: {e}")
```

### Context Managers

```python
# with statement handles setup and cleanup
with open('file.txt', 'r') as f:
    content = f.read()
# File is automatically closed

# Create custom context manager
from contextlib import contextmanager

@contextmanager
def managed_resource():
    print("Setup")
    try:
        yield "resource"
    finally:
        print("Cleanup")

with managed_resource() as res:
    print(f"Using {res}")
```

### Decorators

```python
# Simple decorator (function that wraps another function)
def timing_decorator(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def slow_function():
    import time
    time.sleep(1)

slow_function()  # Prints timing information
```

---

## Centurion Tools: Assembler, Linker, and Testbenches

### RISC-V Assembler

The assembler converts human-readable RISC-V assembly into machine code.

```python
# assembler.py structure

class Instruction:
    """Represents a RISC-V instruction."""
    def __init__(self, opcode, rd=None, rs1=None, rs2=None, imm=None):
        self.opcode = opcode
        self.rd = rd    # Destination register
        self.rs1 = rs1  # Source register 1
        self.rs2 = rs2  # Source register 2
        self.imm = imm  # Immediate value

class Lexer:
    """Tokenize assembly source code."""
    def __init__(self, source):
        self.source = source
        self.tokens = []
    
    def tokenize(self):
        for line in self.source.split('\n'):
            line = line.split('#')[0].strip()  # Remove comments
            if not line:
                continue
            tokens = line.split()
            self.tokens.append(tokens)
        return self.tokens

class Parser:
    """Parse tokens into instruction objects."""
    REGISTER_MAP = {
        'x0': 0, 'zero': 0,
        'x1': 1, 'ra': 1,
        'x2': 2, 'sp': 2,
        # ... more registers
    }
    
    INSTRUCTION_MAP = {
        'add': {'opcode': 0x33, 'funct3': 0, 'funct7': 0, 'type': 'R'},
        'addi': {'opcode': 0x13, 'funct3': 0, 'type': 'I'},
        'lw': {'opcode': 0x03, 'funct3': 2, 'type': 'I'},
        'sw': {'opcode': 0x23, 'funct3': 2, 'type': 'S'},
        'beq': {'opcode': 0x63, 'funct3': 0, 'type': 'B'},
        'jal': {'opcode': 0x6f, 'type': 'J'},
    }
    
    def parse_instruction(self, tokens):
        """Parse a single instruction."""
        mnemonic = tokens[0]
        if mnemonic not in self.INSTRUCTION_MAP:
            raise ValueError(f"Unknown instruction: {mnemonic}")
        
        spec = self.INSTRUCTION_MAP[mnemonic]
        instr = Instruction(spec['opcode'])
        
        # Parse operands based on instruction type
        if spec['type'] == 'R':  # add rd, rs1, rs2
            instr.rd = self.REGISTER_MAP[tokens[1].rstrip(',')]
            instr.rs1 = self.REGISTER_MAP[tokens[2].rstrip(',')]
            instr.rs2 = self.REGISTER_MAP[tokens[3].rstrip(',')]
        elif spec['type'] == 'I':  # addi rd, rs1, imm
            instr.rd = self.REGISTER_MAP[tokens[1].rstrip(',')]
            instr.rs1 = self.REGISTER_MAP[tokens[2].rstrip(',')]
            instr.imm = int(tokens[3], 0)
        # ... handle other types
        
        return instr

class Encoder:
    """Encode instructions into 32-bit machine code."""
    def encode_r_type(self, instr):
        """R-type: opcode[6:0] | rd[11:7] | funct3[14:12] | 
                            rs1[19:15] | rs2[24:20] | funct7[31:25]"""
        code = instr.opcode & 0x7F
        code |= (instr.rd & 0x1F) << 7
        code |= (instr.funct3 & 0x7) << 12
        code |= (instr.rs1 & 0x1F) << 15
        code |= (instr.rs2 & 0x1F) << 20
        code |= (instr.funct7 & 0x7F) << 25
        return code
    
    def encode_i_type(self, instr):
        """I-type: opcode[6:0] | rd[11:7] | funct3[14:12] | 
                            rs1[19:15] | imm[31:20]"""
        code = instr.opcode & 0x7F
        code |= (instr.rd & 0x1F) << 7
        code |= (instr.funct3 & 0x7) << 12
        code |= (instr.rs1 & 0x1F) << 15
        imm = instr.imm & 0xFFF
        code |= imm << 20
        return code

# Usage
source = """
    addi x1, x0, 100    # Load 100 into x1
    addi x2, x0, 200    # Load 200 into x2
    add x3, x1, x2      # x3 = x1 + x2
"""

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser()
instructions = []
for token_list in tokens:
    instr = parser.parse_instruction(token_list)
    instructions.append(instr)

encoder = Encoder()
machine_code = []
for instr in instructions:
    code = encoder.encode_r_type(instr) if instr.type == 'R' else encoder.encode_i_type(instr)
    machine_code.append(code)

# Write to binary file
with open('program.bin', 'wb') as f:
    for code in machine_code:
        f.write(code.to_bytes(4, byteorder='little'))
```

### Linker

The linker combines object files and resolves symbols.

```python
# linker.py

class ObjectFile:
    """Represents a compiled object file."""
    def __init__(self, filename):
        self.filename = filename
        self.code = []
        self.symbols = {}
        self.relocations = []
    
    def read(self):
        """Read object file format (simplified)."""
        with open(self.filename, 'rb') as f:
            # Parse header
            header = f.read(16)
            num_sections = int.from_bytes(header[0:4], 'little')
            
            # Parse code sections
            for _ in range(num_sections):
                size = int.from_bytes(f.read(4), 'little')
                code = f.read(size)
                self.code.extend(code)

class Linker:
    """Links multiple object files."""
    BASE_ADDRESS = 0x80000000  # RISC-V typical base
    
    def __init__(self, object_files):
        self.object_files = [ObjectFile(f) for f in object_files]
        self.executable = bytearray()
        self.symbol_table = {}
    
    def link(self):
        """Link all object files."""
        # Read all object files
        for obj in self.object_files:
            obj.read()
        
        # Assign addresses and collect symbols
        current_address = self.BASE_ADDRESS
        for obj in self.object_files:
            for symbol, info in obj.symbols.items():
                self.symbol_table[symbol] = current_address + info['offset']
            current_address += len(obj.code)
        
        # Concatenate code
        for obj in self.object_files:
            self.executable.extend(obj.code)
    
    def write_elf(self, filename):
        """Write linked executable as ELF."""
        with open(filename, 'wb') as f:
            # ELF header (simplified)
            f.write(b'\x7fELF')  # Magic number
            f.write(b'\x01')      # 32-bit
            f.write(b'\x01')      # Little-endian
            f.write(b'\x01')      # ELF version
            # ... more header fields
            
            f.write(self.executable)

# Usage
linker = Linker(['main.o', 'lib.o'])
linker.link()
linker.write_elf('program.elf')
```

### Testbench Structure with cocotb

While testbenches are covered in detail in misc.md, here's the Python structure:

```python
# tb_uart.py - Testbench for UART

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
import random

@cocotb.test()
async def test_uart_loopback(dut):
    """Test UART transmitter and receiver."""
    
    # Create clock
    clock_task = cocotb.start_soon(Clock(dut.clk, 10, units="us").start())
    
    # Reset
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    
    # Send 0xAB via UART
    dut.data_in.value = 0xAB
    dut.data_valid.value = 1
    await RisingEdge(dut.clk)
    dut.data_valid.value = 0
    
    # Wait for transmission (10 bits at 115200 baud)
    # This takes approximately 10 * (50MHz / 115200) = 4340 clock cycles
    for _ in range(5000):
        await RisingEdge(dut.clk)
    
    # Check output
    print(f"Transmitted: 0xAB")
    print(f"UART TX line: {dut.tx.value}")
```

---

## Summary

Python is essential for Centurion because it:
- **Assembler (~500 lines)**: Lexes, parses, and encodes RISC-V assembly
- **Linker (~300 lines)**: Combines object files and resolves symbols
- **Testbenches (with cocotb)**: Simulate hardware with Python test code
- **Utilities**: File processing, data conversion, scripting

Key takeaways:
- Use dictionaries and lists for data structures
- Leverage list comprehensions for concise, readable code
- Classes organize related data and functions
- Context managers (`with` statements) handle resource cleanup
- Exceptions handle errors gracefully
- Standard library provides powerful tools for file I/O, text processing, and more

Next: Learn how the assembler and linker work together to transform your code into executable binaries.
