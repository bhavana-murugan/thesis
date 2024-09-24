import ast
from graphviz import Digraph

# Function to analyse AST and identify statements and branches


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

    # Highlights statements and branches
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
    if a + b > 10:
        print("Yes")
    else:
        print("No")"""

tree = ast.parse(pgm)

# Analyse the AST
statements, branches = analyze_ast(tree)
# Flatten the branches list to count individual branches
flattened_branches = [item for sublist in branches for item in (sublist if isinstance(sublist, list) else [sublist])]
# Count the total number of statements
total_statements = len(statements) + len(flattened_branches)
print(f"Number of statements: {total_statements}")
print(f"Number of branches: {len(flattened_branches)}")
# Create a Graphviz Digraph object
dot = Digraph(comment='AST')
# Add nodes starting from the root
add_nodes(tree)
# Render the graph to a file and open it
dot.render('ast_tree', format='pdf', view=True)
