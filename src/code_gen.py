from ast_builder import (
    BinOpNode,
    FunctionCallNode,
    IdentifierNode,
    NumberNode,
    StringNode,
    IfNode,
    WhileNode,
)


class CodeGenerator:
    def __init__(self):
        self.code = []
        self.indent_level = 0

    def get_code(self):
        return "".join(self.code)

    def generate(self, nodes):
        for node in nodes:
            self.generate_node(node)

    def generate_node(self, node):
        if node is None:
            return
        method_name = f"gen_{type(node).__name__}"
        method = getattr(self, method_name, self.gen_generic)
        return method(node)

    def gen_generic(self, node):
        raise NotImplementedError(
            f"Code generation not implemented for node type: {type(node).__name__}"
        )

    def gen_NumberNode(self, node):
        return str(node.value)

    def gen_StringNode(self, node):
        return f'"{node.value}"'  # Ensure strings are enclosed in quotes

    def gen_IdentifierNode(self, node):
        if node.name == "sus":
            return "None"  # Use 'None' for 'sus'
        return node.name

    def map_operator(self, op):
        operators = {
            "PLUS": "+",
            "MINUS": "-",
            "TIMES": "*",
            "OVER": "/",
            "EQUALS": "==",
            "LESS_THAN": "<",
            "GREATER_THAN": ">",
        }
        return operators.get(op, f"<unknown operator: {op}>")

    def map_function_name(self, name):
        return {"spill": "print"}.get(name, name)

    def gen_BinOpNode(self, node):
        left = self.gen_expression(node.left)
        right = self.gen_expression(node.right)
        op = self.map_operator(node.op)
        return f"({left} {op} {right})"

    def gen_VarDeclNode(self, node):
        value = self.gen_expression(node.value)
        self.write_line(f"{node.name} = {value}")

    def gen_FunctionCallNode(self, node):
        args = ", ".join([self.gen_expression(arg) for arg in node.args])
        func_name = self.map_function_name(node.name)
        self.write_line(f"{func_name}({args})")

    def gen_FunctionDefNode(self, node):
        params = ", ".join(node.params)
        self.write_line(f"def {node.name}({params}):")
        self.indent_level += 1
        for stmt in node.body:
            self.generate_node(stmt)
        self.indent_level -= 1

        # Make sure the 'main_character' function is defined properly
        if node.name == "main_character":
            self.write_line(f"{node.name}()")

    def gen_IfNode(self, node):
        condition = self.gen_expression(node.condition)
        self.write_line(f"if {condition}:")
        self.indent_level += 1
        for stmt in node.then_body:
            self.generate_node(stmt)
        self.indent_level -= 1
        if node.else_body:
            self.write_line("else:")
            self.indent_level += 1
            for stmt in node.else_body:
                self.generate_node(stmt)
            self.indent_level -= 1

    def gen_WhileNode(self, node):
        condition = self.gen_expression(node.condition)
        self.write_line(f"while {condition}:")
        self.indent_level += 1
        for stmt in node.body:
            self.generate_node(stmt)
        self.indent_level -= 1

    def gen_expression(self, expr):
        if isinstance(
            expr, (NumberNode, StringNode, IdentifierNode, BinOpNode, FunctionCallNode)
        ):
            method_name = f"gen_{type(expr).__name__}"
            method = getattr(self, method_name, self.gen_generic)
            return method(expr)
        elif isinstance(expr, str):
            return f'"{expr}"'
        else:
            raise ValueError(f"Unhandled expression type: {type(expr)}")

    def write_line(self, line):
        indent = "    " * self.indent_level
        self.code.append(f"{indent}{line}\n")
