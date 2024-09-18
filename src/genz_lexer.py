import ply.lex as lex

# List of token names
tokens = (
    # Operators and punctuation
    "PLUS",
    "MINUS",
    "TIMES",
    "OVER",
    "EQUALS",  # Only defined once
    "LPAREN",
    "RPAREN",
    "COMMA",
    "COLON",
    # Structural tokens
    "NEWLINE",
    "INDENT",
    "DEDENT",
    # Literals
    "NUMBER",
    "STRING",
    # Identifiers and keywords
    "IDENTIFIER",
    "VIBE",
    "FLEX",
    "MAIN_CHARACTER",
    "WHILE",
    "COOK",
    "SPILL",
    "IS",
    "SUS",
    "AND",
    "OR",
    "LESS_THAN",
    "GREATER_THAN",
    "NOT_EQUALS",
    "TRUE",
    "FALSE",
    "ELSE",
    "FOR",
    "IN",
)

# Reserved keywords and their corresponding tokens
reserved = {
    "vibe": "VIBE",
    "flex": "FLEX",
    "main_character": "MAIN_CHARACTER",
    "while": "WHILE",
    "cook": "COOK",  # 'if' in your language
    "spill": "SPILL",  # 'print' in your language
    "is": "IS",  # 'is' in Python for comparison
    "sus": "SUS",  # 'None' or empty array in your language
    "and": "AND",  # Logical AND
    "or": "OR",  # Logical OR
    "true": "TRUE",  # Boolean True
    "false": "FALSE",  # Boolean False
    "else": "ELSE",
    "for": "FOR",
    "in": "IN",
}

# Regular expression rules for simple tokens
t_PLUS = r"plus"
t_MINUS = r"minus"
t_TIMES = r"times"
t_OVER = r"over"
t_EQUALS = r"got"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_COMMA = r","
t_COLON = r":"
t_LESS_THAN = r"<"
t_GREATER_THAN = r">"
t_NOT_EQUALS = r"!="

# States for handling indentation
states = (("INDENT", "exclusive"),)


# Function to handle special keywords and identifiers
def t_IDENTIFIER(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    t.type = reserved.get(t.value, "IDENTIFIER")  # Check for reserved words
    return t


# Function to handle strings
def t_STRING(t):
    r'"([^\\\n]|(\\.))*?"'
    t.value = t.value[1:-1]  # Strip the quotes
    return t


# Function to handle numbers
def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    return t


def t_INDENT(t):
    r"[ \t]+"
    pass  # Ignore indentation, handled by parser or as spaces


# Error rule for handling unknown characters in INDENT state
def t_INDENT_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)


def t_INDENT_INITIAL(t):
    r"[ \t]+"
    # Ignore whitespace at beginning of lines if same indentation
    pass


# Function to handle comments
def t_COMMENT(t):
    r"\#.*"
    pass


# Function to handle illegal characters
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)


# Override the token method to handle DEDENT tokens
def lexer_token():
    if hasattr(lexer, "dedent_tokens") and lexer.dedent_tokens:
        return lexer.dedent_tokens.pop()
    else:
        tok = lexer.token_original()
        return tok


# Build the lexer
lexer = lex.lex()
# Initialize indentation stack
lexer.indents = [0]
lexer.dedent_tokens = []

# Save the original token method
lexer.token_original = lexer.token
lexer.token = lexer_token
