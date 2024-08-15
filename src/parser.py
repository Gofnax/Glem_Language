import ply.yacc as yacc
from lexer import tokens

# Precedence rules for arithmetic operators
precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'EQUAL', 'NOTEQUAL', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MODULO'),
    ('right', 'NOT'),
)

# Dictionary to store function definitions
functions = {}

# Dictionary to store the AST
names = {}

# Define the start rule
# start = 'program'


# Grammar rules
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])


def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_statement(p):
    '''statement : expression SEMICOLON
                 | function_definition'''
    p[0] = p[1]


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
        p[0] = ('binop', p[2], p[1], p[3])


def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = ('not', p[2])


def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]


def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = ('number', p[1])


def p_expression_boolean(p):
    '''expression : BOOLEAN'''
    p[0] = ('boolean', p[1])


def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    p[0] = ('identifier', names[p[1]])


def p_expression_function_call(p):
    '''expression : IDENTIFIER LPAREN param_list RPAREN'''
    p[0] = ('call', p[1], p[3], functions[p[1]])


def p_expression_lambda(p):
    '''expression : LAMBDA IDENTIFIER DOT LPAREN expression RPAREN'''
    names[p[2]] = p[2]
    p[0] = ('lambda', p[2], p[5])


def p_function_definition(p):
    # '''function_definition : MEY LCURLY IDENTIFIER COMMA LPAREN arg_list RPAREN RCURLY expression SEMICOLON'''
    '''function_definition : MEY LCURLY IDENTIFIER COMMA LPAREN arg_list RPAREN RCURLY LCURLY statement_list RCURLY SEMICOLON'''
    func_name = p[3]
    args = p[6]
    body = p[10]
    functions[func_name] = (args, body)
    p[0] = ('function', func_name)


def p_arg_list(p):
    '''arg_list : IDENTIFIER
                | IDENTIFIER COMMA arg_list'''
    names[p[1]] = p[1]
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_param_list(p):
    '''param_list : expression
                  | expression COMMA param_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_error(p):
    print(f"Syntax error at '{p.value}'")


# Build the parser
parser = yacc.yacc()
