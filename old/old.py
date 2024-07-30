def create_basic_ast(pgm):
    pgm_arr = pgm.split(TAB)
    # Creation of AST
    line_no = 1
    prev = None
    root = None
    for n in pgm_arr:
        node = Node(n, line_no)
        if prev != None:
            prev.next = node
        else:
            root = node
        prev = node
        line_no += 1
    return root


def root_check(root):
    # Root check
    ptr = root
    while True:
        print(ptr.line_no, ":", ptr.text)
        if ptr.next == None:
            break
        ptr = ptr.next
