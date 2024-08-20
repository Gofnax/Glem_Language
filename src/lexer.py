import ply.lex as lex

# List of token names
tokens = (
    'MEY', 'NUMBER', 'BOOLEAN', 'IDENTIFIER',
    'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULO',
    'AND', 'OR', 'NOT',
    'EQUAL', 'NOTEQUAL', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL',
    'LCURLY', 'RCURLY', 'LPAREN', 'RPAREN', 'LAMBDA', 'SEMICOLON',
    'COMMA', 'DOT'
)

# Regular expressions for tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_GREATER = r'>'
t_LESS = r'<'
t_GREATEREQUAL = r'>='
t_LESSEQUAL = r'<='
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
# t_LAMBDA = r'Lambda'
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'.'

# Regular expressions with some action
def t_MEY(t):
    r'mey'
    return t
def t_NUMBER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_LAMBDA(t):
    r'lambda'
    return t

def t_BOOLEAN(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t


# Ignore whitespace, new line and comments
t_ignore = ' \t \n'
t_ignore_COMMENT = r'\#[a-zA-Z0-9 ]*\#'


# Error handling rule
def t_error(t):
    raise Exception(f"Illegal character '{t.value[0]}' at line {t.lineno}, position {t.lexpos}")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
