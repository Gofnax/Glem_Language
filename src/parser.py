import ply.yacc as yacc
from lexer import tokens  # Import tokens from the lexer

# Define precedence rules to resolve ambiguity in grammar
# Higher precedence operators are listed first
precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'EQUAL', 'NOTEQUAL', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MODULO'),
    ('right', 'NOT'),
)


class GlemParser:
    """
    A class to hold global parser state, such as function definitions and names.
    """
    functions = {}  # Dictionary to store function definitions
    names = {}  # Dictionary to store identifiers (variables)


# Define grammar rules for the language
def p_program(p):
    '''program : statement_list'''
    # The 'program' rule represents the entire program, consisting of a list of statements
    p[0] = ('program', p[1])


def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    # A statement list is either a single statement or a sequence of statements
    if len(p) == 3:
        p[0] = p[1] + [p[2]]  # Concatenate the current statement with the list
    else:
        p[0] = [p[1]]  # Start a new list with the single statement


def p_statement(p):
    '''statement : expression SEMICOLON
                 | function_definition'''
    # A statement can be either an expression followed by a semicolon or a function definition
    p[0] = p[1]


# Define grammar for binary operations
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression
                  | expression MODULO expression
                  | expression AND expression
                  | expression OR expression
                  | expression NOTEQUAL expression
                  | expression EQUAL expression
                  | expression GREATER expression
                  | expression LESS expression
                  | expression GREATEREQUAL expression
                  | expression LESSEQUAL expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        # Binary operations combine two expressions with an operator
        p[0] = ('binop', p[2], p[1], p[3])


def p_expression_not(p):
    '''expression : NOT expression'''
    # Unary 'not' operation negates the truth value of an expression
    p[0] = ('not', p[2])


def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    # Parentheses group expressions to enforce precedence
    p[0] = p[2]


def p_expression_number(p):
    '''expression : NUMBER'''
    # A number is an integer literal
    p[0] = ('number', p[1])


def p_expression_boolean(p):
    '''expression : BOOLEAN'''
    # A boolean is a literal 'true' or 'false'
    p[0] = ('boolean', p[1])


def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    # An identifier is a variable name; it may not be defined initially
    if p[1] not in GlemParser.names:
        GlemParser.names[p[1]] = None
    p[0] = ('identifier', p[1])


def p_expression_function_call(p):
    '''expression : IDENTIFIER LPAREN param_list RPAREN'''
    # Function call with parameters, where IDENTIFIER is the function name
    p[0] = ('call', p[1], p[3])


def p_expression_lambda(p):
    '''expression : LAMBDA IDENTIFIER DOT LPAREN expression RPAREN'''
    # Lambda function with one argument and an expression body
    GlemParser.names[p[2]] = None
    p[0] = ('lambda', p[2], p[5])


def p_function_definition(p):
    '''function_definition : MEY LCURLY IDENTIFIER COMMA LPAREN arg_list RPAREN RCURLY LCURLY statement_list RCURLY SEMICOLON'''
    # Function definition with a name, parameters, and a body of statements
    func_name = p[3]
    args = p[6]
    body = p[10]
    GlemParser.functions[func_name] = (args, body)  # Store the function definition
    p[0] = ('function', func_name)


def p_arg_list(p):
    '''arg_list : IDENTIFIER
                | IDENTIFIER COMMA arg_list'''
    # A list of arguments for functions
    GlemParser.names[p[1]] = p[1]
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_param_list(p):
    '''param_list : expression
                  | expression COMMA param_list'''
    # A list of parameters passed to a function during a call
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


# Error handling for syntax errors in the parser
def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' (line {p.lineno}, position {p.lexpos})")
    else:
        print("Syntax error at end of input")


# Build the parser
parser = yacc.yacc()
