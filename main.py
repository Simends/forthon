#!/usr/bin/env python
from collections import deque
import sys, tty, termios

dict = deque()
stack = deque()
variables = {"base": 10}

def push(arg):
    stack.appendleft(arg)

def pop():
    return stack.popleft()

def ipop():
    return int(pop(), base=variables['base'])

def spop():
    return str(pop())

def addword(name, type, code):
    dict.appendleft({'name': name, 'type': type, 'code': code})

def key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        c = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return c

addword("key", "code", ("push(key())"))

def emit():
    sys.stdout.write(spop())
    sys.stdout.flush()

addword("emit", "code", ("emit()"))
addword(".", "word", ("emit", "lit", "\n", "emit"))

def dup():
    word = pop()
    push(word)
    push(word)

addword("dup", "code", ("dup()"))

def add():
    first = ipop()
    second = ipop()
    push(first + second)

addword("+", "code", ("add()"))

def subtract():
    first = ipop()
    second = ipop()
    push(second - first)
 
addword("-", "code", ("subtract()"))

def multiply():
    first = ipop()
    second = ipop()
    push(first * second)

addword("*", "code", ("multiply()"))

def drop():
    pop()

addword("drop", "code", ("drop()"))

def swap():
    first = pop()
    second = pop()
    push(first)
    push(second)

addword("swap", "code", ("swap()"))

def over():
    stack.rotate(-1)
    second = pop()
    stack.rotate(1)
    push(second)

addword("over", "code", ("over()"))

def rot():
    first = pop()
    second = pop()
    third = pop()
    push(second)
    push(first)
    push(third)

addword("rot", "code", ("rot()"))

def nrot():
    first = pop()
    second = pop()
    third = pop()
    push(first)
    push(third)
    push(second)

addword("-rot", "code", ("nrot()"))

def twodrop():
    pop()
    pop()

addword("2drop", "code", ("twodrop()"))

def twodup():
    first = pop()
    second = pop()
    push(second)
    push(second)
    push(first)
    push(first)

addword("2dup", "code", ("twodup()"))

def incr():
    first = ipop()
    first += 1
    push(first)

addword("1+", "code", "incr()")

def equ():
    first = pop()
    second = pop()
    push(first == second)

addword("=", "code", "equ()")

def nequ():
    first = pop()
    second = pop()
    push(first != second)

addword("<>", "code", "nequ()")

def lt():
    first = pop()
    second = pop()
    push(first < second)

addword("<", "code", "lt()")

def gt():
    first = pop()
    second = pop()
    push(first > second)

addword(">", "code", "gt()")

def le():
    first = pop()
    second = pop()
    push(first <= second)

addword("<=", "code", "le()")

def ge():
    first = pop()
    second = pop()
    push(first >= second)

addword(">=", "code", "ge()")

def store():
    global variables
    variable = pop()
    data = pop()
    variables[variable] = data

addword("!", "code", "store()")

def fetch():
    variable = pop()
    push(variables[variable])

addword("@", "code", "fetch()")

def word():
    input = key()
    if input == "\\":
        # TODO: Comment
        print("Comment!")
    if input.isspace():
        # TODO: Space
        print("Space!")

addword("print4", "word", ("lit", "base", "@", "."))

def find_and_execute(word, starti):
    while starti <= len(dict):
        i = starti
        starti += 1
        if dict[i]['name'] != word:
            continue
        if dict[i]['type'] == "code":
            eval(dict[i]['code'])
            break
        islit = 0
        for subword in dict[i]['code']:
            if islit  != 0:
                push(subword)
                islit = 0
                continue
            if subword == "lit":
                islit = 1
                continue
            find_and_execute(subword, i)
        break

find_and_execute("print4", 0)
