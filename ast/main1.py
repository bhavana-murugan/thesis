import ast
from graphviz import Digraph

# Function to analyze AST and identify statements and branches


def analyze_ast(node):
    statements = []
    branches = []

    class Analyzer(ast.NodeVisitor):
        def visit(self, node):
            # Count function definitions as statements
            if isinstance(node, ast.FunctionDef):
                statements.append(node)
            # Count assignments, expressions, and return statements as statements
            elif isinstance(node, (ast.Assign, ast.Expr, ast.Return)):
                statements.append(node)
            # Count if statements as branches and also consider the else part
            elif isinstance(node, ast.If):
                branches.append(node)  # Count the 'if' branch
                if node.orelse:  # Check if there is an 'else' or 'elif'
                    branches.append(node.orelse)  # Count the 'else' branch
            self.generic_visit(node)

    Analyzer().visit(node)
    return statements, branches

# Function to add nodes to the graph


def add_nodes(node, parent_id=None):
    node_id = str(id(node))

    # Create a label based on the node type and relevant attributes
    if isinstance(node, ast.FunctionDef):
        label = f"FunctionDef\\nname: {node.name}"
    elif isinstance(node, ast.arg):
        label = f"arg\\nname: {node.arg}"
    elif isinstance(node, ast.Assign):
        label = "Assign"
    elif isinstance(node, ast.BinOp):
        label = "BinOp"
    elif isinstance(node, ast.Return):
        label = "Return"
    elif isinstance(node, ast.Name):
        label = f"Name\\nid: {node.id}"
    elif isinstance(node, ast.Constant):
        label = f"Constant\\nvalue: {node.value}"
    elif isinstance(node, ast.If):
        label = "If"
    elif isinstance(node, ast.Compare):
        label = "Compare"
    elif isinstance(node, ast.Call):
        label = f"Call\\nfunc: {node.func.id if isinstance(
            node.func, ast.Name) else type(node.func).__name__}"
    else:
        label = type(node).__name__

    # Highlight statements and branches
    if node in statements:
        dot.node(node_id, label, style='filled', fillcolor='lightblue')
    elif node in branches:
        dot.node(node_id, label, style='filled', fillcolor='lightgreen')
    else:
        dot.node(node_id, label)

    if parent_id:
        dot.edge(parent_id, node_id)

    for child in ast.iter_child_nodes(node):
        add_nodes(child, node_id)


pgm = """def sum(a, b):
    c = a + b
    if c > 10:
       c = 10
    elif c == 0:
        c = 20
    else:
        c = 30
sum(0, 0)
sum(20, 0)
sum(1, 1)"""

# Global dictionary to track executed lines
executed_lines = {}


def track_execution(line_number):
    executed_lines[line_number] = True


class InstrumentationTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # Instrument function entry
        track_call = ast.Expr(
            ast.Call(
                func=ast.Name(id='track_execution', ctx=ast.Load()),
                args=[ast.Num(n=node.lineno)],
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
                args=[ast.Num(n=node.lineno)],
                keywords=[]
            )
        )
        return [track_call, node]

    def visit_If(self, node):
        # Instrument if statements
        if_track_call = ast.Expr(
            ast.Call(
                func=ast.Name(id='track_execution', ctx=ast.Load()),
                args=[ast.Num(n=node.lineno)],
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
                    args=[ast.Num(n=else_lineno)],
                    keywords=[]
                )
            )
            node.orelse.insert(0, else_track_call)

        return self.generic_visit(node)


def instrument_code(code):
    tree = ast.parse(code)
    transformer = InstrumentationTransformer()
    modified_tree = transformer.visit(tree)
    ast.fix_missing_locations(modified_tree)
    return ast.unparse(modified_tree)


def analyze_coverage(original_code):
    total_lines = len(original_code.split('\n'))
    covered_lines = len(executed_lines)
    coverage_percentage = (covered_lines / (total_lines - 3)) * 100

    print("\nCoverage Analysis:")
    print(f"Total lines: {total_lines}")
    print(f"Covered lines: {covered_lines}")
    print(f"Coverage percentage: {coverage_percentage:.2f}%")

    print("\nLine by line coverage:")
    for line_num, line in enumerate(original_code.split('\n'), 1):
        status = "Covered" if line_num in executed_lines else "Not covered"
        print(f"Line {line_num}: {status}")
        print(f"  {line.strip()}")


instrumented_code = instrument_code(pgm)
print("Instrumented code:")
print(instrumented_code)
exec(instrumented_code)
analyze_coverage(pgm)

# # Analyze the AST
# statements, branches = analyze_ast(tree)
# # Flatten the branches list to count individual branches
# flattened_branches = [item for sublist in branches for item in (sublist if isinstance(sublist, list) else [sublist])]
# # Count the total number of statements
# total_statements = len(statements) + len(flattened_branches)  # Include branches in total statements if needed
# print(f"Number of statements: {total_statements}")
# print(f"Number of branches: {len(flattened_branches)}")
# # Create a Graphviz Digraph object
# dot = Digraph(comment='AST')
# # Add nodes starting from the root
# add_nodes(tree)
# # Render the graph to a file and open it
# dot.render('ast_tree', format='pdf', view=True)
