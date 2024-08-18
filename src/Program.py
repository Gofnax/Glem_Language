import sys
import os
from parser import parser
from interpreter import Interpreter
def run_lambda_program(program):
    interpreter = Interpreter()
    ast = parser.parse(program)

    if ast[0] == 'program':
        temp = ast[1]
        i = 0
        while i < len(temp):
            result = interpreter.eval(temp[i])
            while callable(result):
                i += 1
                l_value = interpreter.eval(temp[i])
                result = result(l_value)
            i += 1
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
                user_input = input('> Insert value for lambda:\n> ')
                t_ast = parser.parse(user_input)
                temp = interpreter.eval(t_ast)
                result = result(temp)
                if result is not None and not callable(result):
                    print(result)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if file_path.endswith('.lambda'):
            try:
                with open(file_path, 'r') as file:
                    program = file.read()
                    run_lambda_program(program)
            except FileNotFoundError:
                print("File not found")
        else:
            print(f"Error: {file_path} is not a valid .lambda file.")
    else:
        run_interactive_mode()