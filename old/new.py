import ast

program = open("sum.py", "r")
program_string = program.read()
# print(program_string)
root = ast.parse(program_string)
print(ast.dump(root, indent=4))
