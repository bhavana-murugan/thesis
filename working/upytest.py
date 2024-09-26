import ast
from reader import read
import c0
import c1
import smt
import astgraph

executed_lines = {}


def track_execution(line_number):
    executed_lines[line_number] = True


def instrument_code(code, transformer):
    tree = ast.parse(code)
    modified_tree = transformer.visit(tree)
    ast.fix_missing_locations(modified_tree)
    return ast.unparse(modified_tree)


def utest(file, func):
    (pgm, func) = read(file, func)
    astgraph.graph(pgm)
    cases = smt.generate_constraints(pgm, func)
    pgm_and_cases = pgm + "\n"
    for i, case in enumerate(cases):
        pgm_and_cases += case
        if i < len(cases) - 1:
            pgm_and_cases += "\n"

    t0 = c0.c0()
    instrumented_code1 = instrument_code(pgm_and_cases, t0)
    # print("Instrumented code:")
    # print(instrumented_code1)
    exec(instrumented_code1)
    print("===================================")
    t0.analyze_coverage(pgm, executed_lines)

    executed_lines.clear()

    t1 = c1.c1()
    instrumented_code2 = instrument_code(pgm_and_cases, t1)
    # print("Instrumented code:")
    # print(instrumented_code2)
    print("Output:")
    exec(instrumented_code2)
    t1.analyze_coverage(pgm, executed_lines)
