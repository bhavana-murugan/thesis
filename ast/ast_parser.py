from Node import Node

# types
DEF = "def"
ARGS = "args"
ASSIGN = "="
ADD = "+"
SUBTRACT = "-"
RETURN = "return"
VARIABLE = "variable"

# chars
TAB = "\t"
BREAK_LINE = "\n"
BRACKET_START = "("
SPACE = " "

# precedings in decending order
# add more in future
PRECEDING = {DEF: DEF, ASSIGN: ASSIGN, ADD: ADD, SUBTRACT: SUBTRACT}


def isLeaf(line):
    return (
        line.find(DEF) == -1 and
        line.find(ASSIGN) == -1 and
        line.find(ADD) == -1 and 
        line.find(SUBTRACT) == -1 and
        line.find(RETURN) == -1
    )


def ast(pgm_arr, i, root, prev, parent_prev, current):
    current = str.strip(current)
    if current == "":
        if (i < len(pgm_arr)):
            current = pgm_arr[i]
        else:
            return root
    current = str.strip(current)

    # only for 1st line def sum():
    if i == 0 and current[0:3] == DEF:
        args = current[0:-2].split(BRACKET_START)
        node = Node(args[0], i)
        node.type = DEF
        left_node = Node(args[1].split(','), i)
        left_node.type = ARGS
        node.append(left_node)
        root = node
        prev = node
        parent_prev = node
        current = ""
        i += 1
        ast(pgm_arr, i, root, prev, parent_prev, current)

    # for other nodes   
    else:
        # atomic
        if (isLeaf(current)):
            node = Node(current.strip(), i)
            node.type = VARIABLE
            prev.append(node)
            return

        # 1. =
        elif (-1 != current.find(ASSIGN)):
            node = Node(ASSIGN, i)
            node.type = ASSIGN
            current = current.split(ASSIGN)
            prev.append(node)
            prev = node
            ast(pgm_arr, i, root,  prev, parent_prev, current[0])
            ast(pgm_arr, i, root,  prev, parent_prev, current[1])
            return

        # 2. +
        elif (-1 != current.find(ADD)):
            node = Node(ADD, i)
            node.type = ADD
            current = current.split(ADD)
            prev.append(node)
            prev = node
            ast(pgm_arr, i, root,  prev, parent_prev, current[0])
            ast(pgm_arr, i, root,  prev, parent_prev, current[1])
            return
        # 3. - 
        elif (-1 != current.find(SUBTRACT)):
            node = Node(SUBTRACT, i)
            node.type = SUBTRACT
            current = current.split(SUBTRACT)
            prev.append(node)
            prev = node
            ast(pgm_arr, i, root,  prev, parent_prev, current[0])
            ast(pgm_arr, i, root,  prev, parent_prev, current[1])
            return

        
        # 4. return
        elif (-1 != current.find(RETURN)):
            node = Node(RETURN, i)
            node.type = RETURN
            current = current.split(RETURN)
            parent_prev.append(node)
            prev = node
            ast(pgm_arr, i, root,  prev, parent_prev, current[1])
            return root
    i += 1
    return ast(pgm_arr, i, root,  prev, parent_prev, "")


def parse(pgm, func, *args):
    pgm_arr = pgm.split(BREAK_LINE)
    root = None
    prev = None
    parent_prev = None
    current = ""
    root = ast(pgm_arr, 0, root, prev, parent_prev, current)
    return root
