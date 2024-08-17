import sys
import os
from parser import parser
from interpreter import Interpreter
def run_lambda_program(file_path):
    interpreter = Interpreter()
    with open(file_path, 'r') as file:
        program = file.read()

    ast = parser.parse(program)

    if ast[0] == 'program':
        for expr in ast[1]:
            result = interpreter.eval(expr)
            if callable(result):
                # If the result is a lambda function, you could choose to evaluate it here or just print that a function is created
                print("<lambda function>")
            else:
                print(result)
    else:
        print("Invalid program structure")


def run_interactive_mode():
    interpreter = Interpreter()
    print("Welcome to the Glem Language Interpreter. Type 'exit' to quit.")
    while True:
        try:
            user_input = input('> ')
            if user_input.strip().lower() == 'exit':
                break
            if user_input.strip() == '':
                continue
            ast = parser.parse(user_input)
            result = interpreter.eval(ast)
            while callable(result):
                user_input = input('> ')
                t_ast = parser.parse(user_input)
                result = result(t_ast)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_lambda_program(sys.argv[1])
    else:
        run_interactive_mode()