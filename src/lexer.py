# Lexer definition
import ply.lex as lex

# Token definitions for the lexical analysis
# These tokens represent the basic components of the Glem language
tokens = (
    'MEY', 'NUMBER', 'BOOLEAN', 'IDENTIFIER',
    'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULO',
    'AND', 'OR', 'NOT',
    'EQUAL', 'NOTEQUAL', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL',
    'LCURLY', 'RCURLY', 'LPAREN', 'RPAREN', 'LAMBDA', 'SEMICOLON',
    'COMMA', 'DOT'
)

# Regular expression rules for simple tokens
# Each token corresponds to a specific symbol or keyword in the language
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
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'.'


# Define function for matching 'MEY' keyword
# 'MEY' is a keyword used for function definitions in the Glem language
def t_MEY(t):
    r'mey'
    return t


# Define function for matching numbers, converts string to integer
# This handles both positive and negative integers
def t_NUMBER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


# Define function for matching 'lambda' keyword
# 'lambda' introduces anonymous functions in the Glem language
def t_LAMBDA(t):
    r'lambda'
    return t


# Define function for matching boolean values, converts string to boolean
# Handles the boolean literals 'true' and 'false'
def t_BOOLEAN(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t


# Define function for matching identifiers (variable names)
# Identifiers start with a letter or underscore and can include numbers
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t


# Handle newlines and increment line counter
# This is essential for tracking line numbers for error reporting
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)  # Increment line number based on the number of new lines found


# Ignored characters (spaces, tabs, and comments)
# Comments are enclosed in '#' and ignored by the lexer
t_ignore = ' \t '
t_ignore_COMMENT = r'\#[a-zA-Z0-9.:\-\, ]*\#'


# Error handling rule for illegal characters
# If an illegal character is found, raise an exception with its position
def t_error(t):
    raise Exception(f"Illegal character '{t.value[0]}' at line {t.lineno}, position {t.lexpos}")
    t.lexer.skip(1)  # Skip the illegal character


# Build the lexer
# This compiles the lexer from the token rules defined above
lexer = lex.lex()
