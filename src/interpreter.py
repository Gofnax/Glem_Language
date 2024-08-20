from parser import parser
from parser import GlemParser


class Interpreter:
    def __init__(self):
        # Initialize a stack to track function calls and their respective environments
        self.call_stack = []

    def eval(self, node, env={}):
        """
        Evaluates an AST node in the given environment.

        Args:
            node (tuple): The AST node to evaluate.
            env (dict): The current environment mapping variable names to values.

        Returns:
                The result of evaluating the node, which could be a value, function, or lambda expression.
        """
        if isinstance(node, tuple):
            try:
                if node[0] == 'program':
                    # Evaluate a list of statements in a program
                    self.call_stack.append(('program', env))  # Push a new frame for the program
                    result = None
                    for stmt in node[1]:  # Iterate over each statement in the program
                        result = self.eval(stmt, env)  # Evaluate each statement
                        if not callable(result):  # Only print the result if it's not a lambda function
                            eval_string = str(result)
                            print(eval_string)
                    self.call_stack.pop()  # Pop the program frame after execution
                    return result  # Return the last evaluated result
                elif node[0] == 'number':
                    # Return a number literal
                    return node[1]
                elif node[0] == 'boolean':
                    # Return a boolean literal
                    return node[1]
                elif node[0] == 'identifier':
                    # Evaluate an identifier (variable or function name)
                    if node[1] in env:
                        return env[node[1]]
                    elif node[1] in GlemParser.functions:
                        return node[1]  # Return the function name if it exists in the global function list
                    else:
                        raise RuntimeError(f"Undefined identifier '{node[1]}'")
                elif node[0] == 'binop':
                    # Evaluate a binary operation
                    left = self.eval(node[2], env)  # Evaluate the left operand
                    if left is True and node[1] == '||':
                        return True
                    elif left is False and node[1] == '&&':
                        return False
                    right = self.eval(node[3], env)  # Evaluate the right operand
                    return self.apply_binop(node[1], left, right)  # Apply the binary operation
                elif node[0] == 'not':
                    # Evaluate a unary 'not' operation
                    expr = self.eval(node[1], env)
                    if not isinstance(expr, bool):
                        raise TypeError(f"Expected boolean in 'not' operation, got {type(expr).__name__}")
                    return not expr
                elif node[0] == 'lambda':
                    # Define a lambda expression (anonymous function)
                    res = lambda x: self.eval(node[2], {**env, node[1]: x})
                    return res
                elif node[0] == 'function':
                    # Function declaration, simply acknowledge the function definition
                    return f"Function '{node[1]}' defined."
                elif node[0] == 'call':
                    # Evaluate a function call
                    func_name = env.get(node[1], node[1])  # Get the function name
                    if func_name not in GlemParser.functions:
                        raise NameError(f"Undefined function '{func_name}'")
                    func = GlemParser.functions[func_name]
                    return self.call_function(func, node[2], env, func_name)

            except Exception as e:
                print(f"Runtime error: {e}")
                return None  # Return None on error

        # If the node is not a tuple (e.g., it's a raw value), return it as is
        return node

    def apply_binop(self, op, left, right):
        """
        Apply a binary operation to two operands.

        Args:
            op (str): The binary operator as a string.
            left: The left operand.
            right: The right operand.

        Returns:
            The result of applying the binary operation.

        Raises:
            TypeError: If the operands are of incompatible types for the operation.
            ZeroDivisionError: If division by zero is attempted.
        """
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
                return left // right  # Use integer division
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
        """
        Handle the execution of a function call.

        Args:
            func (tuple): The function body and arguments as a tuple.
            args (list): The arguments passed to the function during the call.
            env (dict): The current environment.
            func_name (str): The name of the function being called.

        Returns:
            The result of executing the function.

        Raises:
            Exception: If there is an error during function execution.
        """
        try:
            func_body, func_args = func[1], func[0]
            # Create a new local environment for the function execution
            local_env = {arg: self.eval(arg_val, env) for arg, arg_val in zip(func_args, args)}
            tot_env = {**env, **local_env}  # Merge local environment with the current environment
            self.call_stack.append((func_name, tot_env))  # Push a stack frame before executing the function
            for stmt in func_body[:-1]:  # Execute all statements except the last one
                print(self.eval(stmt, tot_env))
            return_value = self.eval(func_body[-1], tot_env)  # Return the result of the last statement
            self.call_stack.pop()  # Pop the stack frame after execution
            return return_value
        except Exception as e:
            print(f"Runtime error in function '{func_name}': {e}")
            return None  # Return None on error
