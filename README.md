# Glem_Language
**Making a simple arithmetic programming language named Glem.<br/><br/>**
**Authors:<br/>**
**Gilad Faibish - @giladf424<br/>**
**Emil Glater - @Gofnax<br/>**
<br/>

<details>
<summary> Documentation </summary>

**Data Types:**<br>
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

**Basic Usage:**<br>
The basic way to make use of Glem is to write one-line expressions,<br>
for which the interpreter will print the result.
For example:
```
>>> 3 + 5;
8
>>> 12 >= 4;
true
>>> 4 * (5 + 2);
28
```

**Functions and Lambda Functions:**<br>
In Glem, you can declare functions using the keyword ```mey``` and call them<br>
anywhere in the code from the point of their declaration onwards.<br>
As Glem doesn't support variable assignment, writing a function that<br>
executes multiple statement won't affect that function's returned value,<br>
and only the result of the last statement will be returned.<br>
<br>
The format of a function declaration is:<br>
```
mey {function_name, (arg1, arg2, ...)}
{statement; statement; ...; statement;};
```

For example, let's look at the definition of the function ```addOne``` that<br>
receives an integer and returned its value increased by 1:<br>
```
mey {addOne, (n)}
{n + 1;};
```

</details>
