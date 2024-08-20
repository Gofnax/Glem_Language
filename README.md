# Glem_Language
**Making a simple arithmetic programming language named Glem.<br/><br/>**
**Authors:<br/>**
**Gilad Faibish - @giladf424<br/>**
**Emil Glater - @Gofnax<br/>**
<br/>

Based on code written in Python, using the PLY module, we implemented 
a lexer, a parser, and an interpreter that allow us define a new 
(small) programming language we call Glem.<br>

The interpreter can be used in two methods:
1. Interactive mode (REPL): the user can execute commands one line 
at a time and see the result of each line immediately after execution.
2. Full program mode: code files in Glem have the .lambda suffix. The 
user can provide the path to a file they wrote a Glem program in, and 
our program reads the code line by line and executes it.<br>

----

<details>
<summary> Documentation </summary>
<br>

### Data Types:
In Glem we support the usage of integers and boolean values, 
where all the values are immutable, and there are no variable assignments.<br>
<br>
With this, you can use basic arithmetic operations:
* Addition (+)
* Subtraction (-)
* Multiplication (*)
* Division (integer division) (/)
* Modulo (%)
  
and boolean and comparison operations:
* AND (&&)
* OR (||)
* NOT (!)
* Equality to (==)
* Not queal to (!=)
* Greater than (>)
* Less than (<)
* Greater than or equal to (>=)
* Less than or equal to (<=)
<br>

### Basic Usage:
The basic way to make use of Glem is to write one-line expressions, 
for which the interpreter will print the result. In addition, you can 
write an expression inside an expression, as shown below. At the end 
of each line, there has to be a ```;``` for the language to recognize 
the expression written as a statement it can execute.<br>
For example:
```
>>> 3 + 5;
8
>>> 12 >= 4;
true
>>> 4 * (5 + 2);
28
```
<br>

### Comments:
Glem allows you to add comments to your code to elevate its readability just like 
many other languages. To insert a comment in the code you simply need to wrap it 
with ```#```'s.<br>
For example:
```
...
3 + 5;  # Example code #
addThree(13);  # Works like addOne but increase value by 3 #
5 * 2 # You can even put a comment in the middle of a statement # + true;
...
```
A comment can only include the letters a-z and A-Z, digits 0-9, spcaes ```' '```,
dots ```.```, and commas ```,```, and colon ```:```.
<br>

### Functions:
In Glem, you can define functions using the keyword ```mey``` and call them 
anywhere in the code from the point of their definition onwards. 
As Glem doesn't support variable assignment, writing a function that 
executes multiple statement won't affect that function's returned value, 
and only the result of the last statement will be returned for further calculations.<br>

The format of a function definition is:
```
mey {function_name, (arg1, arg2, ...)}
{statement; statement; ...; statement;};
```

For example, let's look at the definition of the function ```addOne``` that 
receives an integer and returns its value increased by 1:
```
>>> mey {addOne, (n)} {n + 1;};
addOne defined.
```

The format of calling a function is:
```
function_name(arg1, arg2, arg3, ...);
```

Continuing with our example, assuming we defined ```addOne``` earlier in our 
code, to call it we simply need to write its name, followed by brackets with 
values that correspond to its expected values in them:
```
>>> addOne(3);
4
```
<br>

### Lambda Functions:
In addition to regular functions, Glem supports the usage of anonymous 
functions (lambda function/expressions). These allow you to write code with a higher 
level of complexity than a regular statement, but without the need to define 
a function beforehand. For Glem to recognize a lamda function, it has to be defined 
using the ```lambda``` keyword.<br>

The format of a lambda function, as recognized by Glem is:
```
Lambda param.(expression); arg;
```
Where ```param``` can be switched with any other identifier for the parameter 
the lambda function expects to receive, and any expression can be written inside 
the brackets. To immediately invoke the lambda function, an argument has to be sent 
to it in the following statement. If you run the program in the REPL mode, you will 
see a prompt urging you to insert the argument.<br>
<br>

### Calling Functions from other Functions:
In case you want to maintain code readability or avoid duplicating code, Glem allows 
you to use a function (or several functions) as an expression executed within 
another function. With that, you can also define recursive functions.<br>

For example, here's a function call inside another function definition:
```
mey {addOne, (n)} {n + 1;};
mey {addTwo, (n)} {addOne(n) + 1;};
```
First, we have to define the innermost function, the last one to be actually 
called, but the first one to be executed fully. After that, we can call it from 
another function. Thanks to Glem's parsing rules, there is an inherent 'call stack' 
that is responsible for executing each expression in its appropriate scope.<br>
<br>

### Recursion:
As for recursive functions, defining them can be a bit more challenging. Because 
Glem doesn't support if-statements, you have to utilize boolean operations to define 
your stop condition (base case).<br>

For example, here we define a recursive function that calculates the factorial of 
a given number:
```
mey {factorial, (n)} {(n == 0) || (n * factorial(n - 1));};
```
For this function to be able to stop when it receives ```n = 0```, we had to define that in 
case of the OR operation, if the left expression (which is evaluated first) is ```True```, 
then the right expression won't be evaluated, and the statement returns ```True```. This way, 
when we get to ```n = 0```, the functions returns ```True``` to its caller, where ```n = 1```, 
and doesn't continue to try and evaluate the second expression with negative values. When we 
calculate ```1 * True```, it convert the value ```True``` to ```1``` so we get the result 
```1 * True = 1 * 1 = 1```. From this point on, only integers get returned by the fucntion 
which ends up calculating the factorial of the value received by the user.
<br>
</details>

----

<details>
<summary> BNF and Language Limitations </summary>
<br>
  
### Language Syntax:
```
program ::= statement_list

statement_list ::= statement_list statement
                 | statement

statement ::= expression ";"
            | function_definition
            | expression_lambda

expression ::= expression "+" expression
             | expression "-" expression
             | expression "*" expression
             | expression "/" expression
             | expression "%" expression
             | expression "&&" expression
             | expression "||" expression
             | expression "!=" expression
             | expression "==" expression
             | expression ">" expression
             | expression "<" expression
             | expression ">=" expression
             | expression "<=" expression
             | "!" expression
             | "(" expression ")"
             | NUMBER
             | BOOLEAN
             | IDENTIFIER
             | IDENTIFIER "(" param_list ")"
             | "lambda" IDENTIFIER "." "(" expression ")"

function_definition ::= "mey" "{" IDENTIFIER "," "(" arg_list ")" "}" "{" statement_list "}" ";"

arg_list ::= IDENTIFIER
           | IDENTIFIER "," arg_list

param_list ::= expression
             | expression "," param_list
```

### Language Limitations:
Glem is designed in such a way that there are a few concepts that are not supported by the 
language. Among them are:
* Variable assignment
* Conditional statements
* Shortage of data types
* Only sinle-line comments

The trade-off of these concepts not being supported, is keeping the language simple. There 
aren't many keywords and grammar rules the user needs to get to know and remember to be able 
to write working code in Glem.
<br>
</details>

----

<details>
<summary> User Guide for Running the Interpreter </summary>
<br>

Welcome to the Glem Language Interpreter User Guide. This guide provides instructions on how to 
run the interpreter in both interactive mode (REPL) and file reading mode.

### System Requirements:
To run the Glem Language Interpreter, you will need:
* Python 3.6 or higher and pip (Python's package installer) installed on your machine
* Our repository cloned to your machine
<br>

### Installing PLY Module:
Our project is based on the PLY module, so to run it correctly using the command prompt or the 
terminal, you need to install it using the next command:
```
pip install ply
```
<br>

### Interactive Mode (REPL):
Interactive mode allows you to enter and execute Glem language commands one at a time. This mode 
is useful for testing snippets of code quickly.

To start the interpreter in interactive mode:
1. Open a terminal or command prompt.
2. Navigate to the directory where the program.py file is located.
3. Type the following command and press 'Enter':
```
python Program.py
```
4. You will see a prompt that says "Welcome to the Glem Language Interpreter. Type 'exit' to quit."
Enter your commands after the > prompt.
5. To exit the interactive mode, type exit and press Enter.

**Sample session:**
```
> mey {addOne, (n)} {n + 1;};
Function 'addOne' defined.
> addOne(5);
6
> exit
```
<br>

### File Reading Mode:
File reading mode allows you to execute a script written in the Glem language saved in a file with a 
.lambda suffix.

To run a .lambda file:
1. Ensure your file has a .lambda suffix and contains valid Glem language code.
2. Open a terminal or command prompt.
3. Navigate to the directory where both your .lambda file and program.py are located.
4. Run the following command, replacing your_script.lambda with the name of your file:
```
python Program.py your_script.lambda
```
5. The interpreter will execute the contents of the file and display the outputs sequentially.

**Sample Session:**<br>
example.lambda file contains:
```
mey {factorial, (n)} {(n == 0) || (n * factorial(n - 1));};
factorial(5);
```

Command to run:
```
python Program.py example.lambda
```

Expected output:
```
120
```
<br>

### Error Handling
If there are any errors in your Glem language code, whether syntax or runtime, the interpreter will 
display an error message detailing the issue. For instance, using an undefined function or variable 
will prompt an error indicating that the identifier is undefined.
<br>

### Notes
* Ensure that all Glem language commands and functions in your scripts adhere to the syntax rules as 
specified by the language's grammar.
* The interpreter can handle basic arithmetic, logical operations, function definitions, and lambda 
expressions as outlined in the Glem language specifications.

For more information or support, refer to the official documentation.
<br>
</details>

----

<details>
<summary> Design Choices </summary>
<br>

### Lexer:
The lexer is responsible for tokenizing the user input so that we can create a string that 
the language understands and can evaluate.

**Design Considerations:**
* To describe what string gets translated to each token we chose to work with regular expressions 
(or REGEX). This way we cover all the strings that the user can input without having to 
actually write down each and every one of them.
* Whitespaces and single-line comments are ignored. This makes the source code more readable 
without affecting the functionality.
* The lexer includes a mechanism for identifying and reporting illegal characters.

**Assumptions:**
* It is assumed that keywords such as ```lambda``` and ```mey``` are always written in lowercase 
and cannot be used as identifiers.
* We assume all numbers are integers, and booleans are either ```true``` or ```false```. No 
support for other types like strings or floating-point numbers.
<br>

### Parser:
The parser is responsible for building the AST from the token the lexer provided it, 
allowing the interpreter to evaluate the user input and return the user the result they 
were expecting to get from their program.

**Design Considerations:**
* The parser follows a clear set of grammar rules that align with the language's specifications. 
Each grammar rule corresponds to a particular construct in the language, like expressions, function 
definitions, and statements. The parser's main goal is to produce an Abstract Syntax Tree (AST) 
that represents the structure of the source code.
* Precedence rules for operators are defined by the parser to ensure correct evaluation order by 
the interpreter. These rules are crucial for handling expressions with multiple operators, such 
as arithmetic and logical operations.
* It is able to recognize and store function definitions, and differentiate between function 
definition and function call based on the syntax. Functions are stored in a dictionary within the 
GlemParser class, where each key is the function name, and its value is a tuple that holds the 
arguments the function expects to get, and all the statements that it expects to execute upon 
call. It also handles function calls, ensuring that parameters are passed correctly according 
to the language's rules and the function's expectations.

**Assumptions:**
* The parser assumes a fixed grammar structure, meaning that function definitions, expressions, 
and other constructs follow a strict format. For instance, function definitions must always use 
the ```mey``` keyword followed by the correct syntax, and expressions must adhere to the defined 
operator precedence.
* The parser assumes that once an identifier is defined within a function or lambda expression, 
its value is immutable. This is consistent with the language's functional nature and is enforced 
during parsing by ensuring identifiers are correctly mapped and not reassigned.
<br>

### Interpreter:
The interpreter is responsible for evaluating an input string or a program received from the user 
and returning them the final value that that input come sdown to.

**Design Considerations:**
* Managing an environment (a dictionary) to map identifiers to their corresponding values or functions, 
to resemble memory storage. A call stack is implemented by the grammar of the language, and simulated 
using a stack to manage function calls and recursion.
* AST nodes are evaluated by the interpreter based on their types, such as binary operations, function 
calls, literals, etc.. It recursively processes the tree, applying operations and managing scopes, and
at the end returning the final value of each statement.
* The design includes support for higher-order functions, allowing functions to be passed as arguments 
to other functions.

**Assumptions:**
* There is a determined sequence in which the expressions in each statement need to be evaluated 
for the interpreter to return the correct final value.
* The environment is assumed to be immutable, meaning that once a value is bound to an identifier, 
it cannot be changed.
* Each function definition ends with a single return value, which is the result of the evaluation of 
the last statement in the function body.
<br>

### Challenges and Solutions:
This is our first try at writing an interpreter of any kind, and our first actual project implemented 
using Python. As a result, we faced quite a few challenges with building this project.
* Unfamiliar syntax and conventions: being inexperienced with a language poses many challenges in its 
own. You have to learn the syntax anew for features you're familiar with from other languages, and 
the languages nuances may differ (such as memory management, data types implementation, object methods, 
etc.).
* No prior knowledge of the interpreter's way of work: we had to create an interpreter for a language 
without being taught the intricacies of how the interpreter works, what parts it's composed of, or how
each part communicates with the other.

Regardless, we had to make the project work, so obviously we had a lot of learning and experimenting 
to do in order to familiarize ourselves with Python and the operation process of the interpreter. We 
mainly relied on many different forums and on ChatGPT as knowledge sources and reference points when 
we had to find out how certain things are done, or if they are possible to implement in the way we 
know from other languages.
<br>
</details>
