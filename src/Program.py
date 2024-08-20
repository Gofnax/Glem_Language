import sys
import os
from parser import parser
from interpreter import Interpreter


def run_lambda_program(program):
    """
    Parses and executes a lambda program from a string.

    Args:
        program (str): The source code of the program to execute.
    """
    interpreter = Interpreter()  # Create an instance of the Interpreter
    ast = parser.parse(program)  # Parse the program to generate an Abstract Syntax Tree (AST)

    if ast[0] == 'program':  # Check if the AST is correctly structured
        temp = ast[1]
        i = 0
        while i < len(temp):  # Iterate over each statement in the program
            result = interpreter.eval(temp[i])  # Evaluate the current statement
            while callable(result):  # Handle lambda expressions that require additional input
                i += 1
                l_value = interpreter.eval(temp[i])  # Evaluate the next expression as input for the lambda
                result = result(l_value)
            i += 1
            print(result)  # Output the result of the evaluated statement
    else:
        print("Invalid program structure")  # Handle cases where the program structure is incorrect


def run_interactive_mode():
    """
    Runs the interpreter in interactive mode, allowing users to enter commands one at a time.
    """
    interpreter = Interpreter()  # Create an instance of the Interpreter
    print("Welcome to the Glem Language Interpreter. Type 'exit' to quit.")
    while True:
        try:
            user_input = input('> ')  # Get input from the user
            if user_input.strip().lower() == 'exit':  # Exit interactive mode if the user types 'exit'
                break
            if user_input.strip() == '':  # Skip empty input
                continue
            else:
                ast = parser.parse(user_input)  # Parse the user input to generate an AST
            result = interpreter.eval(ast)  # Evaluate the parsed AST
            while callable(result):  # Handle lambda expressions that require additional input
                user_input = input('Insert value for lambda:\n> ')
                temp_ast = parser.parse(user_input)
                temp = interpreter.eval(temp_ast)
                result = result(temp)
                if result is not None and not callable(result):
                    print(result)  # Output the result
        except Exception as e:
            print(f"Error: {e}")  # Print any errors that occur during parsing or evaluation


if __name__ == '__main__':
    """
    Determines the mode to run the interpreter based on command line arguments:
    - If a .lambda file is provided, it runs in file reading mode.
    - If no file is provided, it runs in interactive mode.
    """
    if len(sys.argv) > 1:  # Check if there are command line arguments provided
        file_path = sys.argv[1]  # Get the file path from the command line arguments
        if file_path.endswith('.lambda'):  # Ensure the file has the correct .lambda suffix
            try:
                with open(file_path, 'r') as file:  # Open and read the file
                    program = file.read()
                    stmtList = program.split(';')  # Split the program into individual statements
                    addToList = False
                    func_def = []  # List to accumulate function definitions
                    lambda_def = []  # List to accumulate lambda definitions
                    count = 0  # Counter to track nested lambdas
                    for stmt in stmtList:
                        try:
                            if stmt == '' or stmt == '\n':  # Skip empty or newline-only statements
                                continue
                            stmt += ';'
                            if "mey" in stmt or addToList:  # Detect function definition start
                                addToList = True
                                func_def.append(stmt)
                                if stmt[0] == '}':  # Detect function definition end
                                    addToList = False
                                    stmtToRun = " ".join(func_def)
                                    func_def = []
                                    run_lambda_program(stmtToRun)  # Run the complete function definition
                            elif "lambda" in stmt:  # Detect lambda expression start
                                count = stmt.count("lambda")
                                lambda_def.append(stmt)
                            elif count > 0:  # Match argument input to number of lambda functions
                                lambda_def.append(stmt)
                                count -= 1
                                if count == 0:  # Lambda expression complete (all arguments matched)
                                    lambdaToRun = " ".join(lambda_def)
                                    lambda_def = []
                                    run_lambda_program(lambdaToRun)  # Run the complete lambda expression
                            else:
                                run_lambda_program(stmt)  # Run regular statements
                        except Exception as e:
                            print(f"Error processing statement: {stmt}.")  # Handle errors in statement processing
            except FileNotFoundError:
                print("File not found")  # Handle file not found error
            except Exception as e:
                print(f"Error opening file: {e}")  # Handle any other errors during file reading

        else:
            print(f"Error: {file_path} is not a valid .lambda file.")  # Handle invalid file extension
    else:
        run_interactive_mode()  # Start interactive mode if no file is provided
