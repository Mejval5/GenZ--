# fmt: off
import ply.yacc as yacc
from genz_lexer import tokens
from ast_builder import (
    NumberNode,
    StringNode,
    BinOpNode,
    VarDeclNode,
    IdentifierNode,
    FunctionCallNode,
    FunctionDefNode,
    IfNode,
    WhileNode,
    ForEachNode,
    BooleanNode,
)

# Precedence rules with logical and comparison operators
precedence = (
    ("left", "OR"),
    ("left", "AND"),
    ("left", "LESS_THAN", "GREATER_THAN", "EQUALS", "NOT_EQUALS"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "OVER"),
)


# Starting rule
def p_program(p):
    "program : statement_list"
    p[0] = p[1]


def p_expression_statement(p):
    "expression_statement : expression"
    p[0] = p[1]


def p_statement_list(p):
    """statement_list : statement_list NEWLINE statement
    | statement_list NEWLINE
    | statement"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_statement(p):
    """statement : variable_declaration
    | expression_statement
    | function_definition
    | if_statement
    | while_statement
    | for_statement"""
    p[0] = p[1]


def p_function_definition(p):
    """function_definition : VIBE IDENTIFIER LPAREN parameter_list RPAREN COLON suite
    | MAIN_CHARACTER LPAREN RPAREN COLON suite"""
    if p[1] == "vibe":
        p[0] = FunctionDefNode(p[2], p[4], p[7], p.lineno(1))
    else:
        p[0] = FunctionDefNode("main_character", [], p[5], p.lineno(1))


def p_suite(p):
    """suite : NEWLINE INDENT statement_list DEDENT
    | NEWLINE INDENT DEDENT"""
    if len(p) == 5:
        p[0] = p[3]  # Non-empty block
    else:
        p[0] = []  # Empty block


def p_parameter_list(p):
    """parameter_list : parameter_list COMMA IDENTIFIER
    | IDENTIFIER
    | empty"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif p[1]:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_variable_declaration(p):
    "variable_declaration : FLEX IDENTIFIER EQUALS expression"
    p[0] = VarDeclNode(p[2], p[4], p.lineno(1))


def p_expression(p):
    """expression : expression PLUS term
                  | expression MINUS term
                  | expression AND term
                  | expression OR term
                  | expression LESS_THAN term
                  | expression GREATER_THAN term
                  | expression EQUALS term
                  | expression NOT_EQUALS term
                  | term"""
    if len(p) == 4:
        p[0] = BinOpNode(p[1], p[2], p[3], p.lineno(2))
    else:
        p[0] = p[1]


def p_term(p):
    """term : term TIMES factor
    | term OVER factor
    | factor"""
    if len(p) == 4:
        p[0] = BinOpNode(p[1], p[2], p[3], p.lineno(2))
    else:
        p[0] = p[1]


def p_factor(p):
    """factor : NUMBER
    | STRING
    | IDENTIFIER
    | TRUE
    | FALSE
    | SPILL LPAREN expression RPAREN
    | SUS
    | function_call"""
    if p.slice[1].type == "NUMBER":
        p[0] = NumberNode(p[1])
    elif p.slice[1].type == "STRING":
        p[0] = StringNode(p[1])
    elif p.slice[1].type == "IDENTIFIER":
        p[0] = IdentifierNode(p[1])
    elif p.slice[1].type == "SPILL":
        p[0] = FunctionCallNode("print", [p[3]], p.lineno(1))  # Spill maps to print
    elif p.slice[1].type == "SUS":
        p[0] = IdentifierNode("None")  # Map SUS to None
    elif p.slice[1].type == "TRUE":
        p[0] = BooleanNode(True, p.lineno(1))
    elif p.slice[1].type == "FALSE":
        p[0] = BooleanNode(False, p.lineno(1))
    elif p.slice[1].type == "function_call":
        p[0] = p[1]  # Function call already created its node


def p_function_call(p):
    "function_call : IDENTIFIER LPAREN argument_list RPAREN"
    p[0] = FunctionCallNode(p[1], p[3], p.lineno(1))


def p_argument_list(p):
    """argument_list : argument_list COMMA expression
    | expression
    | empty"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif p[1]:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_if_statement(p):
    """if_statement : COOK expression COLON suite
    | COOK expression COLON suite ELSE COLON suite"""
    if len(p) == 5:
        p[0] = IfNode(p[2], p[4], lineno=p.lineno(1))
    else:
        p[0] = IfNode(p[2], p[4], p[7], p.lineno(1))


def p_while_statement(p):
    "while_statement : WHILE expression COLON suite"
    p[0] = WhileNode(p[2], p[4], p.lineno(1))


def p_for_statement(p):
    "for_statement : FOR IDENTIFIER IN expression COLON suite"
    p[0] = ForEachNode(p[2], p[4], p[6], p.lineno(1))


def p_empty(p):
    "empty :"
    p[0] = None


def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, value '{p.value}' at line {p.lineno}")
    else:
        print("Syntax error at EOF")


# Build the parser
parser = yacc.yacc(debug=False, write_tables=False)
# fmt: on
