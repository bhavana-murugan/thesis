import ast


class c0(ast.NodeTransformer):

    def create_track_call(self, lineno):
        return ast.Expr(
            ast.Call(
                func=ast.Name(id='track_execution', ctx=ast.Load()),
                args=[ast.Constant(n=lineno)],
                keywords=[]
            )
        )

    def visit_FunctionDef(self, node):
        # Instrument function entry
        track_call = self.create_track_call(node.lineno)
        node.body.insert(0, track_call)
        return self.generic_visit(node)

    def visit_Assign(self, node):
        # Instrument assignments
        track_call = self.create_track_call(node.lineno)
        return [track_call, node]

    def visit_If(self, node):
        # Instrument if statements
        if_track_call = self.create_track_call(node.lineno)
        node.body.insert(0, if_track_call)
        if node.orelse:
            # If there's an else block, instrument it
            else_lineno = node.orelse[0].lineno if isinstance(
                node.orelse[0], ast.If) else node.body[-1].lineno + 1
            else_track_call = self.create_track_call(else_lineno)
            node.orelse.insert(0, else_track_call)
        return self.generic_visit(node)

    def visit_For(self, node):
        # Instrument for loops
        for_track_call = self.create_track_call(node.lineno)
        node.body.insert(0, for_track_call)
        return self.generic_visit(node)

    def visit_While(self, node):
        # Instrument while loops
        while_track_call = self.create_track_call(node.lineno)
        node.body.insert(0, while_track_call)
        return self.generic_visit(node)

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == 'print':
            # Track print statements
            track_call = self.create_track_call(node.lineno)
            return [track_call, node]
        elif isinstance(node.value, ast.BinOp):
            # Track arithmetic operations
            track_call = self.create_track_call(node.lineno)
            return [track_call, node]
        return self.generic_visit(node)

    def analyze_coverage(self, original_code, executed_lines):
        total_lines = len(original_code.split('\n'))
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
