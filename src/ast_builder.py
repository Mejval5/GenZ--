# ast_builder.py


class NumberNode:
    def __init__(self, value, lineno=None):
        self.value = value
        self.lineno = lineno


class StringNode:
    def __init__(self, value, lineno=None):
        self.value = value
        self.lineno = lineno


class IdentifierNode:
    def __init__(self, name, lineno=None):
        self.name = name
        self.lineno = lineno


class BinOpNode:
    def __init__(self, left, op, right, lineno=None):
        self.left = left
        self.op = op
        self.right = right
        self.lineno = lineno


class VarDeclNode:
    def __init__(self, name, value, lineno=None):
        self.name = name
        self.value = value
        self.lineno = lineno


class FunctionCallNode:
    def __init__(self, name, args, lineno=None):
        self.name = name
        self.args = args
        self.lineno = lineno


class FunctionDefNode:
    def __init__(self, name, params, body, lineno=None):
        self.name = name
        self.params = params
        self.body = body
        self.lineno = lineno


class IfNode:
    def __init__(self, condition, then_body, else_body=None, lineno=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body
        self.lineno = lineno


class WhileNode:
    def __init__(self, condition, body, lineno=None):
        self.condition = condition
        self.body = body
        self.lineno = lineno


class ForEachNode:
    def __init__(self, iterator, iterable, body, lineno=None):
        self.iterator = iterator
        self.iterable = iterable
        self.body = body
        self.lineno = lineno


class BooleanNode:
    def __init__(self, value, lineno=None):
        self.value = value
        self.lineno = lineno


class ReturnNode:
    def __init__(self, value, lineno=None):
        self.value = value
        self.lineno = lineno
