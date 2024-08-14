from parser import parser
class Interpreter:
    def __init__(self):
        self.call_stack = []

    def eval(self, node, env={}):
        if isinstance(node, tuple):
            if node[0] == 'number':
                return node[1]
            elif node[0] == 'boolean':
                return node[1]
            elif node[0] == 'identifier':
                return env.get(node[1], parser.names.get(node[1]))
            elif node[0] == 'binop':
                left = self.eval(node[2], env)
                right = self.eval(node[3], env)
                return self.apply_binop(node[1], left, right)
            elif node[0] == 'not':
                return not self.eval(node[1], env)
            elif node[0] == 'lambda':
                return lambda x: self.eval(node[2], {**env, node[1]: x})
            elif node[0] == 'call':
                func_name = node[1]
                args = node[2]
                func = parser.functions[func_name]
                return self.call_function(func, args, env)
        return node

    def apply_binop(self, op, left, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left // right
        elif op == '%':
            return left % right
        elif op == '&&':
            return left and right
        elif op == '||':
            return left or right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '>':
            return left > right
        elif op == '<':
            return left < right
        elif op == '>=':
            return left >= right
        elif op == '<=':
            return left <= right

    def call_function(self, func, args, env):
        func_type, func_args, func_body = func
        local_env = {arg: self.eval(arg_val, env) for arg, arg_val in zip(func_args, args)}
        return self.eval(func_body, {**env, **local_env})


# Test the interpreter
interpreter = Interpreter()
# ast = parser.parse('3 + 5;')
# '''function_definition : MEY LCURLY IDENTIFIER COMMA LPAREN arg_list RPAREN RCURLY expression SEMICOLON'''
ast = parser.parse('mey {factorial, (n,)} (n == 0) || (n * factorial(n - 1)); factorial(5);')
result = interpreter.eval(ast)
print(result)
