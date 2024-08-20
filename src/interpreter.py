from parser import parser
from parser import GlemParser


class Interpreter:
    def __init__(self):
        self.call_stack = []  # Stack frame format: (<function_name>, <environment>)

    def eval(self, node, env={}):
        if isinstance(node, tuple):
            try:
                if node[0] == 'program':
                    self.call_stack.append(('program', env))  # Pushing a starting stack frame
                    result = None
                    for stmt in node[1]:
                        result = self.eval(stmt, env)
                        if not callable(result):  # Only print the result if it's not a lambda function
                            eval_string = str(result)
                            print(eval_string)
                    self.call_stack.pop()  # After the program finishes, we pop the first stack frame
                    return result  # Return the result of the last evaluated statement
                elif node[0] == 'number':
                    return node[1]
                elif node[0] == 'boolean':
                    return node[1]
                elif node[0] == 'identifier':
                    if node[1] in env:
                        return env[node[1]]
                    elif node[1] in GlemParser.functions:
                        return node[1]
                    else:
                        raise RuntimeError(f"Undefined identifier '{node[1]}'")
                    # return env.get(node[1], node[1])
                elif node[0] == 'binop':
                    left = self.eval(node[2], env)
                    if left is True and node[1] == '||':
                        return True
                    elif left is False and node[1] == '&&':
                        return False
                    right = self.eval(node[3], env)
                    return self.apply_binop(node[1], left, right)
                elif node[0] == 'not':
                    expr = self.eval(node[1], env)
                    if not isinstance(expr, bool):
                        raise TypeError(f"Expected boolean in 'not' operation, got {type(expr).__name__}")
                    return not expr
                    # return not self.eval(node[1], env)
                elif node[0] == 'lambda':
                    res = lambda x: self.eval(node[2], {**env, node[1]: x})
                    return res
                elif node[0] == 'function':
                    return f"Function '{node[1]}' defined."
                    # return node[1] + " defined."
                elif node[0] == 'call':
                    func_name = env.get(node[1], node[1])
                    if func_name not in GlemParser.functions:
                        raise NameError(f"Undefined function '{func_name}'")
                    func = GlemParser.functions[func_name]
                    return self.call_function(func, node[2], env, func_name)
                    # args = node[2]
                    # func = GlemParser.functions[func_name]
                    # return self.call_function(func, args, env, func_name)

            except Exception as e:
                print(f"Runtime error: {e}")
                return None

        return node

    def apply_binop(self, op, left, right):
        try:
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
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
            else:
                raise ValueError(f"Unknown binary operator '{op}'")
        except TypeError:
            raise TypeError(
                f"Type error: Unsupported operand type(s) for '{op}': '{type(left).__name__}' and '{type(right).__name__}'")

    def call_function(self, func, args, env, func_name):
        try:
            func_body, func_args = func[1], func[0]
            local_env = {arg: self.eval(arg_val, env) for arg, arg_val in zip(func_args, args)}
            tot_env = {**env, **local_env}
            self.call_stack.append((func_name, tot_env))  # Pushing a stack frame before executing the function
            for stmt in func_body[:-1]:
                print(self.eval(stmt, tot_env))
            return_value = self.eval(func_body[-1], tot_env)
            self.call_stack.pop()  # Popping the stack frame after finishing the execution of the function
            return return_value
        except Exception as e:
            print(f"Runtime error in function '{func_name}': {e}")
            return None


# Test the interpreter
interpreter = Interpreter()
# ast = parser.parse('!true;')
# ast = parser.parse('-3 + (3 + 5) * 2; !true; true; 3 > 5 || 5 == 3;')
# ast = parser.parse('mey {factorial, (n)} {(n == 0) || (n * factorial(n - 1));}; true; factorial(5);')
# ast = parser.parse('mey {addOne, (n)} {n + 1;}; mey {loop, (count, total, cond)} {(cond && loop(count - 1, addOne(total), count - 1 > 0)) || ((1 - cond) && total);}; loop(5, 10, true);')
# ast = parser.parse('mey {addOne, (n, m)} {n * 2; m + 3; !true; n - 2 * 3;}; addOne(9 + 1, 200);')
# ast = parser.parse('mey {addOne, (n)} {n + 1;}; mey {addTwo, (n)} {addOne(n) + 1;}; addTwo(3);')
# ast = parser.parse('lambda x.(lambda y.(y+1));')
# ast = parser.parse('(1 == 0) || (2 + 3 + true);')
ast = parser.parse('mey {addOne, (n)} {n + 1;}; mey {doLambda, (action, arg)} {action(arg);}; doLambda(lambda x.(x+1), 3);')
result = interpreter.eval(ast)
# while callable(result):
#     result = result(10)
print(result)
# test_cases = [
#     ('Missing semicolon', 'lambda x.(x+1)', 'Syntax error'),
#     ('Unclosed parenthesis', '1 + (2 * 3', 'Syntax error'),
#     ('Invalid character', '1 + @ 2;', 'Illegal character')
# ]
# test_cases.extend([
#     ('Adding boolean to number', '1 + true;', 'Type error'),
#     ('Boolean as function', 'true(2);', 'Type error'),
#     ('Number as function', '3(4);', 'Type error')
# ])
# test_cases.extend([
#     ('Division by zero', '10 / 0;', 'Runtime error: division by zero'),
#     ('Undefined variable', 'x + 1;', 'Runtime error: undefined variable')
# ])
# for description, code, expected_error in test_cases:
#     try:
#         ast = parser.parse(code)
#         result = interpreter.eval(ast)
#         print(f"Expected: {expected_error}")
#         # print(f"1) Test failed: {description}. Expected {expected_error}, got {result}.")
#     except Exception as e:
#         if expected_error in str(e):
#             print(f"2) Test passed: {description}.")
#         else:
#             print(f"3) Test failed: {description}. Expected {expected_error}, got {str(e)}.")
