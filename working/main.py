import ast
import c0
import c1

cases = ["sum(0, 0)", "sum(5, 6)"]
total_cases = len(cases)
pgm = """def sum(a, b):
    c = a + b
    if c > 10:
        print("Yes")
    else:
        print("No")"""

pgm_and_cases = pgm + "\n"
for i, case in enumerate(cases):
    pgm_and_cases += case
    if i < len(cases) - 1:
        pgm_and_cases += "\n"


executed_lines = {}


def track_execution(line_number):
    executed_lines[line_number] = True


def instrument_code(code, transformer):
    tree = ast.parse(code)
    modified_tree = transformer.visit(tree)
    ast.fix_missing_locations(modified_tree)
    return ast.unparse(modified_tree)


t0 = c0.c0()
instrumented_code1 = instrument_code(pgm_and_cases, t0)
print("Instrumented code:")
print(instrumented_code1)
exec(instrumented_code1)
t0.analyze_coverage(pgm, executed_lines)

executed_lines.clear()

t1 = c1.c1()
instrumented_code2 = instrument_code(pgm_and_cases, t1)
print("Instrumented code:")
print(instrumented_code2)
exec(instrumented_code2)
t1.analyze_coverage(pgm, executed_lines)
