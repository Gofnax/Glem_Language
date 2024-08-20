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
            # if not user_input.endswith(';'):
            #     ast = parser.parse(user_input + ';')
            else:
                ast = parser.parse(user_input)
            result = interpreter.eval(ast)
            while callable(result):
                user_input = input('> Insert value for lambda:\n> ')
                if not user_input.endswith(';'):
                    t_ast = parser.parse(user_input + ';')
                else:
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
                    Gilad = program.split(';')
                    print(Gilad)
                    addToList = False
                    func_def = []
                    lambda_def = []
                    count = 0
                    for stmt in Gilad:
                        try:
                            if stmt == '' or stmt == '\n':
                                continue
                            stmt += ';'
                            if "mey" in stmt[0:5] or addToList:
                                addToList = True
                                func_def.append(stmt)
                                if stmt[0] == '}':
                                    addToList = False
                                    stmtToRun = " ".join(func_def)
                                    func_def = []
                                    run_lambda_program(stmtToRun)
                            elif "lambda" in stmt:
                                count = stmt.count("lambda")
                                lambda_def.append(stmt)
                            elif count > 0:
                                lambda_def.append(stmt)
                                count -= 1
                                if count == 0:
                                    lambdaToRun = " ".join(lambda_def)
                                    lambda_def = []
                                    run_lambda_program(lambdaToRun)
                            else:
                                run_lambda_program(stmt)
                        except Exception as e:
                            print(f"Error processing statement: {stmt}.")
            except FileNotFoundError:
                print("File not found")
            except Exception as e:
                print(f"Error opening file: {e}")

        else:
            print(f"Error: {file_path} is not a valid .lambda file.")
    else:
        run_interactive_mode()