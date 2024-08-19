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

<details>
<summary> Documentation </summary>

***Data Types:***<br>
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

***Basic Usage:***<br>
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

***Comments:***<br>
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
<br>

***Functions:***<br>
In Glem, you can define functions using the keyword ```mey``` and call them 
anywhere in the code from the point of their definition onwards. 
As Glem doesn't support variable assignment, writing a function that 
executes multiple statement won't affect that function's returned value, 
and only the result of the last statement will be returned.<br>

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

***Lambda Functions:***<br>
In addition to regular functions, Glem supports the usage of anonymous 
functions (lambda function/expressions). These allow you to write code with a higher 
level of complexity than a regular statement, but without the need to define 
a function beforehand. For Glem to recognize a lamda function, it has to be defined 
using the ```lambda``` keyword.<br>

The format of a lambda function, as recognized by Glem is:
```
Lambda param.(expression)
```
Where ```param``` can be switched with any other identifier for the parameter 
the lambda function expects to receive, and any expression can be written inside 
the brackets.<br>
<br>

***Calling Functions from other Functions and Recursion:***<br>
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

As for recursive functions, defining them can be a bit more challenging. Because 
Glem doesn't support if-statements, you have to utilize boolean operations to define 
your stop condition (base case).<br>

For example, here we define a recursive function that calculates the factorial of 
a given number:
```
mey {factorial, (n)} {(n == 0) || (n * factorial(n - 1));};
```
For this function to be able to stop when it receives ```n``` with the value ```0```, 
we had to define that in case of the OR operation, if the left expression (which is evaluated 
first) is ```True```, then the right expression won't be evaluated, and the statement returns 
the value ```True```. This way, when we get to ```n = 0```, the functions returns ```True``` 
to its caller, where ```n = 1```, and when we calculate ```1 * True```, it convert the value 
```True``` to ```1``` so we get the result ```1 * True = 1 * 1 = 1```.<br>
<br>


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
