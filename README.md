# Glem_Language
**Making a simple arithmetic programming language named Glem.<br/><br/>**
**Authors:<br/>**
**Gilad Faibish - @giladf424<br/>**
**Emil Glater - @Gofnax<br/>**
<br/>

Based on code written in Python, using the PLY module, we implemented<br>
a lexer, a parser, and an interpreter that allow us define a new<br>
(small) programming language we call Glem.<br>

The interpreter can be used in two methods:
1. Interactive mode (REPL): the user can execute commands one line<br>
at a time and see the result of each line immediately after execution.<br>
2. Full program mode: code files in Glem have the .lambda suffix. The<br>
user can provide the path to a file they wrote a Glem program in, and<br>
our program reads the code line by line and executes it.<br>

<details>
<summary> Documentation </summary>

***Data Types:***<br>
In Glem we support the usage of integers and boolean values,<br>
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

***Basic Usage:***<br>
The basic way to make use of Glem is to write one-line expressions,<br>
for which the interpreter will print the result. In addition, you can<br>
write an expression inside an expression, as shown below. At the end<br>
of each line, there has to be a ```;``` for the language to recognize<br>
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

***Functions:***<br>
In Glem, you can define functions using the keyword ```mey``` and call them<br>
anywhere in the code from the point of their definition onwards.<br>
As Glem doesn't support variable assignment, writing a function that<br>
executes multiple statement won't affect that function's returned value,<br>
and only the result of the last statement will be returned.<br>
<br>
The format of a function definition is:<br>
```
mey {function_name, (arg1, arg2, ...)}
{statement; statement; ...; statement;};
```

For example, let's look at the definition of the function ```addOne``` that<br>
receives an integer and returns its value increased by 1:<br>
```
>>> mey {addOne, (n)} {n + 1;};
addOne defined.
```

The format of calling a function is:
```
function_name(arg1, arg2, arg3, ...);
```

Continuing with our example, assuming we defined ```addOne``` earlier in our<br>
code, to call it we simply need to write its name, followed by brackets with<br>
values that correspond to its expected values in them:
```
>>> addOne(3);
4
```

In addition to regular functions, Glem supports the usage of anonymous<br>
functions (lambda function/expressions). These allow you to write code with a higher<br>
level of complexity than a regular statement, but without the need to define<br>
a function beforehand. For Glem to recognize a lamda function, it has to be defined<br>
using the ```lambda``` keyword.<br>
<br>
The format of a lambda function, as recognized by Glem is:
```
Lambda param.(expression)
```
Where ```param``` can be switched with any other identifier for the parameter<br>
the lambda function expects to receive, and any expression can be written inside<br>
the brackets.<br>

***Comments:***<br>
Glem allows you to add comments to your code to elevate its readability just like<br>
many other languages. To insert a comment in the code you simply need to wrap it<br>
with ```#```'s.<br>
For example:
```
...
3 + 5;  # Example code #
addThree(13);  # Works like addOne but increase value by 3 #
5 * 2 + true;
...
```

</details>

<details>
<summary>BNF</summary>
<br>
The syntax of Glem is as follows:<br>
  
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
             | number
             | boolean
             | identifier
             | identifier "(" param_list ")"
             | "lambda" identifier "." "(" expression ")"

function_definition ::= "mey" "{" identifier "," "(" arg_list ")" "}" "{" statement_list "}" ";"

arg_list ::= identifier
           | identifier "," arg_list

param_list ::= expression
             | expression "," param_list
```
</details>
