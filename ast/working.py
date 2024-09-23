import ast

# Global dictionary to track executed lines
executed_lines = {}

# { 1: true, 2: true }
# { b1: true, b2: true }


def track_execution(line_number):
    executed_lines[line_number] = True


class C0_transformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # Instrument function entry
        track_call = ast.Expr(
            ast.Call(
                func=ast.Name(id='track_execution', ctx=ast.Load()),
                args=[ast.Constant(n=node.lineno)],
                keywords=[]
            )
        )
        node.body.insert(0, track_call)
        return self.generic_visit(node)

    def visit_Assign(self, node):
        # Instrument assignments
        track_call = ast.Expr(
            ast.Call(
                func=ast.Name(id='track_execution', ctx=ast.Load()),
                args=[ast.Constant(n=node.lineno)],
                keywords=[]
            )
        )
        return [track_call, node]

    def visit_If(self, node):
        # Instrument if statements
        if_track_call = ast.Expr(
            ast.Call(
                func=ast.Name(id='track_execution', ctx=ast.Load()),
                args=[ast.Constant(n=node.lineno)],
                keywords=[]
            )
        )
        node.body.insert(0, if_track_call)

        if node.orelse:
            # If there's an else block, instrument it
            else_lineno = node.orelse[0].lineno if isinstance(
                node.orelse[0], ast.If) else node.body[-1].lineno + 1
            else_track_call = ast.Expr(
                ast.Call(
                    func=ast.Name(id='track_execution', ctx=ast.Load()),
                    args=[ast.Constant(n=else_lineno)],
                    keywords=[]
                )
            )
            node.orelse.insert(0, else_track_call)

        return self.generic_visit(node)

class C1_transformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # Instrument function entry
        track_call = ast.Expr(
            ast.Call(
                func=ast.Name(id='track_execution', ctx=ast.Load()),
                args=[ast.Constant(n=node.lineno)],
                keywords=[]
            )
        )
        node.body.insert(0, track_call)
        return self.generic_visit(node)

    def visit_Assign(self, node):
        # Instrument assignments
        track_call = ast.Expr(
            ast.Call(
                func=ast.Name(id='track_execution', ctx=ast.Load()),
                args=[ast.Constant(n=node.lineno)],
                keywords=[]
            )
        )
        return [track_call, node]

    def visit_If(self, node):
        # Instrument if statements
        if_track_call = ast.Expr(
            ast.Call(
                func=ast.Name(id='track_execution', ctx=ast.Load()),
                args=[ast.Constant(n=node.lineno)],
                keywords=[]
            )
        )
        node.body.insert(0, if_track_call)

        if node.orelse:
            # If there's an else block, instrument it
            else_lineno = node.orelse[0].lineno if isinstance(
                node.orelse[0], ast.If) else node.body[-1].lineno + 1
            else_track_call = ast.Expr(
                ast.Call(
                    func=ast.Name(id='track_execution', ctx=ast.Load()),
                    args=[ast.Constant(n=else_lineno)],
                    keywords=[]
                )
            )
            node.orelse.insert(0, else_track_call)

        return self.generic_visit(node)


def instrument_code(code):
    tree = ast.parse(code)
    transformer = C0_transformer()
    modified_tree = transformer.visit(tree)
    ast.fix_missing_locations(modified_tree)
    return ast.unparse(modified_tree)


def analyze_coverage(original_code):
    total_lines = len(original_code.split('\n')) - 3
    covered_lines = len(executed_lines)
    coverage_percentage = (covered_lines / total_lines) * 100

    print("\nCoverage Analysis:")
    print(f"Total lines: {total_lines}")
    print(f"Covered lines: {covered_lines}")
    print(f"C0 Coverage percentage: {coverage_percentage:.2f}%")

    print("\nLine by line coverage:")
    for line_num, line in enumerate(original_code.split('\n'), 1):
        status = "Covered" if line_num in executed_lines else "Not covered"
        print(f"Line {line_num}: {line.strip()} : {status}")


pgm = """def sum(a, b):
    c = a + b
    if c > 10:
        c = 10
    else:
        c = 30
sum(0, 0)
sum(20, 0)
sum(1, 1)"""

instrumented_code = instrument_code(pgm)

print("Instrumented code:")
print(instrumented_code)

exec(instrumented_code)
analyze_coverage(pgm)
