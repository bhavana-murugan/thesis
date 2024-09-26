import ast


class c1(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.branch_count = 0

    def get_branch_count(self):
        return self.branch_count

    def create_track_call(self, lineno):
        return ast.Expr(
            ast.Call(
                func=ast.Name(id='track_execution', ctx=ast.Load()),
                args=[ast.Constant(n=lineno)],
                keywords=[]
            )
        )

    def visit_If(self, node):
        # Instrument if statements
        self.branch_count += 1  # Count the 'if' branch
        if_track_call = self.create_track_call(node.lineno)
        node.body.insert(0, if_track_call)
        if node.orelse:
            self.branch_count += 1  # Count the 'if' branch
            # If there's an else block, instrument it
            else_lineno = node.orelse[0].lineno if isinstance(
                node.orelse[0], ast.If) else node.body[-1].lineno + 1
            else_track_call = self.create_track_call(else_lineno)
            node.orelse.insert(0, else_track_call)
        return self.generic_visit(node)

    def visit_For(self, node):
        self.branch_count += 1  # Count the 'if' branch
        # Instrument for loops
        for_track_call = self.create_track_call(node.lineno)
        node.body.insert(0, for_track_call)
        return self.generic_visit(node)

    def visit_While(self, node):
        self.branch_count += 1  # Count the 'if' branch
        # Instrument while loops
        while_track_call = self.create_track_call(node.lineno)
        node.body.insert(0, while_track_call)
        return self.generic_visit(node)

    def analyze_coverage(self, original_code, executed_lines):
        total_lines = self.get_branch_count()
        covered_lines = len(executed_lines)
        coverage_percentage = (covered_lines / total_lines) * 100

        print("\nCoverage Analysis:")
        print(f"Total branches: {total_lines}")
        print(f"Covered branches: {covered_lines}")
        print(f"C1 Coverage percentage: {coverage_percentage:.2f}%")
        if coverage_percentage>=65:
            print("\033[92mC1 - PASS\033[0m")
        else:
            print("\033[91mC1 - FAIL\033[0m")

        # print("\nLine by line coverage:")
        # for line_num, line in enumerate(original_code.split('\n'), 1):
        #     status = "Covered" if line_num in executed_lines else "Not covered"
        #     print(f"Line {line_num}: {line.strip()} : {status}")
