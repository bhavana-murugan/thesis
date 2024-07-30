from reader import read
from ast_parser import parse


def sum(a, b):
    c = a+b
    return c


def root_check(root):
    print(root.text)

    j = 0
    while (j < len(root.children)):
        root_check(root.children[j])
        j += 1


if __name__ == '__main__':
    (pgm, func, *args) = read(__file__, sum, int, int)
    #print(pgm)
    root = parse(pgm, func, *args)
    # print(sum(1,2))
    root_check(root)
