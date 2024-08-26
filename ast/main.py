from reader import read
from ast_parser import parse


def sum(a, b):
    c = a+b
    return c

def minus(a, b):
    c = a-b
    return c

def mul(a, b):
    c = a * b
    return c

def div(a, b):
    c = a / b
    return c

def mod(a, b):
    c = a * b
    return c

def ifs(a, b):
    c = 0
    if a == b:
        return 
    return c



def printRoot(root):
    print(str(root.text) + ", line_no: " + str(root.line_no))

    j = 0
    while (j < len(root.children)):
        printRoot(root.children[j])
        j += 1


if __name__ == '__main__':
    (pgm, func, *args) = read(__file__, minus, int, int)
    root = parse(pgm, func, *args)
    printRoot(root)
