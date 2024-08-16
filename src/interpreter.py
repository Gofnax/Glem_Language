from parser import parser
from parser import GlemParser


class Interpreter:
    def __init__(self):
        self.call_stack = []    # Stack frame format: (<function_name>, <environment>)

    def eval(self, node, env={}):
        if isinstance(node, tuple):
            if node[0] == 'program':
                self.call_stack.append(('program', env))    # Pushing a starting stack frame
                for stmt in node[1]:
                    eval_string = str(self.eval(stmt, env))
                    print(eval_string)
                self.call_stack.pop()   # After the program finishes, we pop the first stack frame
                return
            elif node[0] == 'number':
                return node[1]
            elif node[0] == 'boolean':
                return node[1]
            elif node[0] == 'identifier':
                return env.get(node[1], node[1])
            elif node[0] == 'binop':
                left = self.eval(node[2], env)
                if left is True and node[1] == '||':
                    return True
                elif left is False and node[1] == '&&':
                    return False
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
                func = GlemParser.functions[func_name]
                return self.call_function(func, args, env, func_name)
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

    def call_function(self, func, args, env, func_name):
        func_body, func_args = func[1], func[0]
        local_env = {arg: self.eval(arg_val, env) for arg, arg_val in zip(func_args, args)}
        tot_env = {**env, **local_env}
        self.call_stack.append((func_name, tot_env))    # Pushing a stack frame before executing the function
        for stmt in func_body[:-1]:
            print(self.eval(stmt, tot_env))
        return_value = self.eval(func_body[-1], tot_env)
        self.call_stack.pop()   # Popping the stack frame after finishing the execution of the function
        return return_value


# Test the interpreter
interpreter = Interpreter()
# ast = parser.parse('!true;')
# ast = parser.parse('-3 + (3 + 5) * 2; !true; true; 3 > 5 || 5 == 3;')
# ast = parser.parse('mey {factorial, (n)} {(n == 0) || (n * factorial(n - 1));}; true; factorial(5);')
# ast = parser.parse('mey {addOne, (n)} {n + 1;}; mey {loop, (n, m)} {(n == 0) || (addOne(m) && loop(n - 1, m));}; loop(5, 3);')
# ast = parser.parse('mey {addOne, (n, m)} {n * 2; m + 3; !true; n - 2 * 3;}; addOne(9 + 1, 200);')
# ast = parser.parse('mey {addOne, (n)} {n + 1;}; mey {addTwo, (n)} {addOne(n) + 1;}; addTwo(3);')
# ast = parser.parse('Lambda x.(x+1);')
ast = parser.parse('(1 == 0) || (2 + 3 + true);')
result = interpreter.eval(ast)
# print(result)
