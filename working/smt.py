import ast
from z3 import *
# pip install z3-solver


class ConstraintExtractor(ast.NodeVisitor):
    def __init__(self):
        self.constraints = []
        self.variables = set()

    def visit_If(self, node):
        self.if_condition = self.expr_to_z3(node.test)
        self.constraints.append(self.if_condition)
        self.has_else = node.orelse != []
        self.generic_visit(node)

    def visit_Compare(self, node):
        left = self.expr_to_z3(node.left)
        for op, right in zip(node.ops, node.comparators):
            right = self.expr_to_z3(right)
            if isinstance(op, ast.Gt):
                self.constraints.append(left > right)
            elif isinstance(op, ast.Lt):
                self.constraints.append(left < right)
            elif isinstance(op, ast.Eq):
                self.constraints.append(left == right)
            elif isinstance(op, ast.GtE):
                self.constraints.append(left >= right)
            elif isinstance(op, ast.LtE):
                self.constraints.append(left <= right)
            elif isinstance(op, ast.NotEq):
                self.constraints.append(left != right)

    def visit_BoolOp(self, node):
        if isinstance(node.op, ast.And):
            self.constraints.append(
                And(*[self.expr_to_z3(value) for value in node.values]))
        elif isinstance(node.op, ast.Or):
            self.constraints.append(
                Or(*[self.expr_to_z3(value) for value in node.values]))

    def visit_BinOp(self, node):
        left = self.expr_to_z3(node.left)
        right = self.expr_to_z3(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            return left / right

    def expr_to_z3(self, node):
        if isinstance(node, ast.Name):
            self.variables.add(node.id)
            return Int(node.id)
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            return self.visit_BinOp(node)
        elif isinstance(node, ast.Compare):
            self.visit_Compare(node)
            return self.constraints[-1]
        elif isinstance(node, ast.BoolOp):
            self.visit_BoolOp(node)
            return self.constraints[-1]


def generate_constraints(code):
    tree = ast.parse(code)
    extractor = ConstraintExtractor()
    extractor.visit(tree)

    print("Variables:", extractor.variables)
    print("If Condition:", extractor.if_condition)
    print("Has Else:", extractor.has_else)

    # Create Z3 solver
    solver_if = Solver()
    solver_if.add(extractor.if_condition)

    print("\nSolving for 'if' branch:")
    if solver_if.check() == sat:
        model = solver_if.model()
        print("Satisfiable. Model:")
        for var in extractor.variables:
            print(f"{var} = {model[Int(var)]}")
    else:
        print("Unsatisfiable")

    # Solve for 'else' branch (if it exists)
    if extractor.has_else:
        solver_else = Solver()
        solver_else.add(Not(extractor.if_condition))
        
        print("\nSolving for 'else' branch:")
        if solver_else.check() == sat:
            model = solver_else.model()
            print("Satisfiable. Model:")
            for var in extractor.variables:
                print(f"{var} = {model[Int(var)]}")
        else:
            print("Unsatisfiable")
