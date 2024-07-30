class Node:
    # text = ""
    # line_no = 0
    # is_used = False
    # proceed_to_next = False
    # type = ""
    # result = ""
    # children = []

    def __init__(self, text, line_no):
        self.text = text
        self.line_no = line_no
        self.children = []

    def show(self):
        print(self.text)

    def append(self, n):
        self.children.append(n)
