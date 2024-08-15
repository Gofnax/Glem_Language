from parser import parser


class Interpreter:
    def __init__(self):
        self.call_stack = []

    def eval(self, node, env={}):
        if isinstance(node, tuple):
            if node[0] == 'program':
                for stmt in node[1]:
                    eval_string = str(self.eval(stmt, env))
                    if not eval_string:
                        print(eval_string)
                return
            elif node[0] == 'number':
                return node[1]
            elif node[0] == 'boolean':
                return node[1]
            elif node[0] == 'identifier':
                return env.get(node[1], node[1])
            elif node[0] == 'binop':
                left = self.eval(node[2], env)
                right = self.eval(node[3], env)
                return self.apply_binop(node[1], left, right)
            elif node[0] == 'not':
                return not self.eval(node[1], env)
            elif node[0] == 'lambda':
                return lambda x: self.eval(node[2], {**env, node[1]: x})
            elif node[0] == 'function':
                return node[1] + " defined."
            elif node[0] == 'call':
                func_name = node[1]
                args = node[2]
                func = node[3]  # parser.functions[func_name]
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
        func_body, func_args = func[1], func[0]
        local_env = {arg: self.eval(arg_val, env) for arg, arg_val in zip(func_args, args)}
        for stmt in func_body:
            print(self.eval(stmt, {**env, **local_env}))
        return


# Test the interpreter
interpreter = Interpreter()
# ast = parser.parse('!true;')
# ast = parser.parse('-3 + (3 + 5) * 2; !true; true; 3 > 5 || 5 == 3;')
# '''function_definition : MEY LCURLY IDENTIFIER COMMA LPAREN arg_list RPAREN RCURLY LCURLY expression SEMICOLON RCURLY SEMICOLON'''
# ast = parser.parse('mey {factorial, (n)} (n == 0) || (n * factorial(n - 1)); true; factorial(5);')
ast = parser.parse('mey {addOne, (n)} {n * 2; n + 3; !true; n - 2 * 3;}; addOne(9 + 1);')
# ast = parser.parse('Lambda x.(x+1);')
result = interpreter.eval(ast)
# print(result)
