::: {#navbar .navbar .navbar-default .navbar-fixed-top role="navigation"}
::: {.container}
::: {.navbar-header}
[]{.icon-bar} []{.icon-bar} []{.icon-bar}

<div>

[![](../_static/img/RAIcon.png)](/runestone/default/user/login){.brand-logo}
[fopp](../index.html){#rs-book-toc-link .navbar-brand}

</div>
:::

::: {.navbar-collapse .collapse .navbar-ex1-collapse}
-   
-   []{#ad_warning}
-   []{#browsing_warning}
-   
-   [*[Search]{.visuallyhidden
    aria-label="Search"}*](#){.dropdown-toggle}
    -   [Table of Contents](../index.html)

    -   [Book Index](../genindex.html)

    -   

    -   ::: {.input-group}
        :::
-   
-   [*[User]{.visuallyhidden aria-label="User"}*](#){.dropdown-toggle}
    -   []{.loggedinuser}

    -   

    -   [Course Home](/ns/course/index)

    -   [Assignments](/assignment/student/chooseAssignment)

    -   [Practice](/runestone/assignments/practice)

    -   [[Peer Instruction
        (Instructor)](/runestone/peer/instructor.html)]{#inst_peer_link}

    -   [Peer Instruction (Student)](/runestone/peer/student.html)

    -   

    -   [Change Course](/runestone/default/courses)

    -   

    -   [[Instructor\'s
        Page](/runestone/admin/index)]{#ip_dropdown_link}

    -   [Progress Page](/runestone/dashboard/studentreport)

    -   

    -   [Edit Profile](/runestone/default/user/profile){#profilelink}

    -   [Change
        Password](/runestone/default/user/change_password){#passwordlink}

    -   [Register](/runestone/default/user/register){#registerlink}

    -   [Login](#)

    -   ::: {.slider .round}
        :::

        Dark Mode
-   
-   [[*[Scratch Activecode]{.visuallyhidden
    aria-label="Scratch Activecode"}*](javascript:runestoneComponents.popupScratchAC())]{#scratch_ac_link}
-   
-   [*[Help]{.visuallyhidden aria-label="Help"}*](#){.dropdown-toggle}
    -   [FAQ](http://runestoneinteractive.org/pages/faq.html)
    -   [Instructors Guide](https://guide.runestone.academy)
    -   
    -   [About Runestone](http://runestoneinteractive.org)
    -   [Report A
        Problem](/runestone/default/reportabug?course=fopp&page=StatementsandExpressions)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [2.1
        Introduction](intro-VariablesExpressionsandStatements.html){.reference
        .internal}
    -   [2.2 Values and Data Types](Values.html){.reference .internal}
    -   [2.3 Operators and Operands](Operators.html){.reference
        .internal}
    -   [2.4 Function Calls](FunctionCalls.html){.reference .internal}
    -   [2.5 Data Types](DataTypes.html){.reference .internal}
    -   [2.6 Type conversion
        functions](ConvertTypeFunctions.html){.reference .internal}
    -   [2.7 Variables](Variables.html){.reference .internal}
    -   [2.8 Variable Names and
        Keywords](VariableNamesandKeywords.html){.reference .internal}
    -   [2.9 👩‍💻 Choosing the Right Variable
        Name](WPChoosingtheRightVariableName.html){.reference .internal}
    -   [2.10 Statements and
        Expressions](StatementsandExpressions.html){.reference
        .internal}
    -   [2.11 Order of Operations](OrderofOperations.html){.reference
        .internal}
    -   [2.12 Reassignment](Reassignment.html){.reference .internal}
    -   [2.13 Updating Variables](UpdatingVariables.html){.reference
        .internal}
    -   [2.14 👩‍💻 Hard-Coding](HardCoding.html){.reference .internal}
    -   [2.15 Input](Input.html){.reference .internal}
    -   [2.16 Glossary](Glossary.html){.reference .internal}
    -   [2.17 Exercises](Exercises.html){.reference .internal}
    -   [2.18 Chapter Assessment](week1a2.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#statements-and-expressions .section}
[]{#index-0}

[2.10. ]{.section-number}Statements and Expressions[¶](#statements-and-expressions "Permalink to this heading"){.headerlink}
============================================================================================================================

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#expression_vid .align-left .youtube-video component="youtube" video-height="315" question_label="2.10.1" video-width="560" video-videoid="3WgmLIsXFkI" video-divid="expression_vid" video-start="0" video-end="-1"}
:::
:::

A **statement** is an instruction that the Python interpreter can
execute. You have only seen the assignment statement so far. Some other
kinds of statements that you'll see in future chapters are
`while`{.docutils .literal .notranslate} statements, `for`{.docutils
.literal .notranslate} statements, `if`{.docutils .literal .notranslate}
statements, and `import`{.docutils .literal .notranslate} statements.
(There are other kinds too!)

An **expression** is a combination of literals, variable names,
operators, and calls to functions. Expressions need to be evaluated. The
result of evaluating an expression is a *value* or *object*.

![table that shows expressions and their value, and
type.](../_images/expression_value_type.png)

If you ask Python to `print`{.docutils .literal .notranslate} an
expression, the interpreter **evaluates** the expression and displays
the result.

::: {.runestone .explainer .ac_section}
::: {#ac2_10_1 component="activecode" question_label="2.10.2"}
::: {#ac2_10_1_question .ac_question}
:::
:::
:::

In this example `len`{.docutils .literal .notranslate} is a built-in
Python function that returns the number of characters in a string.

The *evaluation of an expression* produces a value, which is why
expressions can appear on the right hand side of assignment statements.
A literal all by itself is a simple expression, and so is a variable.

::: {.runestone .explainer .ac_section}
::: {#ac2_10_2 component="activecode" question_label="2.10.3"}
::: {#ac2_10_2_question .ac_question}
:::
:::
:::

In a program, anywhere that a literal value (a string or a number) is
acceptable, a more complicated expression is also acceptable. Here are
all the kinds of expressions we've seen so far:

literal

:   e.g., "Hello" or 3.14

variable name

:   e.g., x or len

operator expression

:   \<expression\> operator-name \<expression\>

function call expressions

:   \<expression\>(\<expressions separated by commas\>)

Notice that operator expressions (like `+`{.docutils .literal
.notranslate} and `*`{.docutils .literal .notranslate}) have
sub-expressions before and after the operator. Each of these can
themselves be simple or complex expressions. In that way, you can build
up to having pretty complicated expressions.

::: {.runestone .explainer .ac_section}
::: {#ac2_10_3 component="activecode" question_label="2.10.4"}
::: {#ac2_10_3_question .ac_question}
:::
:::
:::

Similarly, when calling a function, instead of putting a literal inside
the parentheses, a complex expression can be placed inside the
parentheses. (Again, we provide some hidden code that defines the
functions `square`{.docutils .literal .notranslate} and `sub`{.docutils
.literal .notranslate}).

::: {.runestone .explainer .ac_section}
::: {#ac2_10_4 component="activecode" question_label="2.10.5"}
::: {#ac2_10_4_question .ac_question}
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac2_10_5 component="activecode" question_label="2.10.6"}
::: {#ac2_10_5_question .ac_question}
:::
:::
:::

With a function call, it's even possible to have a complex expression
before the left parenthesis, as long as that expression evaluates to a
function object. For now, though, we will just use variable names (like
square, sub, and len) that are directly bound to function objects.

It is important to start learning to read code that contains complex
expressions. The Python interpreter examines any line of code and
*parses* it into components. For example, if it sees an `=`{.docutils
.literal .notranslate} symbol, it will try to treat the whole line as an
assignment statement. It will expect to see a valid variable name to the
left of the =, and will parse everything to the right of the = as an
expression. It will try to figure out whether the right side is a
literal, a variable name, an operator expression, or a function call
expression. If it's an operator expression, it will further try to parse
the sub-expressions before and after the operator. And so on. You should
learn to parse lines of code in the same way.

In order to evaluate an operator expression, the Python interpreter
first completely evaluates the expression before the operator, then the
one after, then combines the two resulting values using the operator. In
order to evaluate a function call expression, the interpreter evaluates
the expression before the parentheses (i.e., it looks up the name of the
function). Then it tries to evaluate each of the expressions inside the
parentheses. There may be more than one, separated by commas. The values
of those expressions are passed as inputs to the function when the
function is called.

If a function call expression is a sub-expression of some more
complicated expression, as `square(x)`{.docutils .literal .notranslate}
is in `sub(square(y), square(x))`{.docutils .literal .notranslate}, then
the return value from `square(x)`{.docutils .literal .notranslate} is
passed as an input to the `sub`{.docutils .literal .notranslate}
function. This is one of the tricky things that you will have to get
used to working out when you read (or write) code. In this example, the
`square`{.docutils .literal .notranslate} function is called (twice)
before the `sub`{.docutils .literal .notranslate} function is called,
even though the `sub`{.docutils .literal .notranslate} function comes
first when reading the code from left to right. In the following example
we will use the notation of -add- to indicate that Python has looked up
the name add and determined that it is a function object.

::: {#eval2_10_1 .runestone .explainer component="showeval" question_label="2.10.7" tracemode="true"}
Next Step

Reset

::: {.evalCont style="background-color: #FDFDFD;"}
x = 5\
y = 7\
add(square(y), square(x))\
:::

::: {.evalCont}
:::
:::

To start giving you some practice in reading and understanding
complicated expressions, try doing the two Parsons problems below. Be
careful not to indent any of the lines of code; that's something that
will come later in the course.

::: {.runestone .parsons-container}
::: {#pp2_10_1a .parsons component="parsons"}
::: {.parsons_question .parsons-text}
Please order the code fragments in the order in which the Python
interpreter would evaluate them. x is 2 and y is 3. Now the interpreter
is executing square(sub(1+y, x)).
:::

``` {.parsonsblocks question_label="2.10.8" style="visibility: hidden;"}
        look up the variable square to get the function object
---
look up the variable sub to get the function object
---
look up the variable y to get 3
---
add 1 and 3 to get 4
---
look up the variable x to get 2
---
run the sub function, passing inputs 4 and 2, returning the value 2
---
run the square function on input 2, returning the value 4
        
```
:::
:::

::: {.runestone .parsons-container}
::: {#pp2_10_1 .parsons component="parsons"}
::: {.parsons_question .parsons-text}
Please order the code fragments in the order in which the Python
interpreter would evaluate them. x is 2 and y is 3. Now the interpreter
is executing square(x + sub(square(y), 2 \*x)).
:::

``` {.parsonsblocks question_label="2.10.9" style="visibility: hidden;"}
        look up the variable square to get the function object
---
look up the variable x to get 2
---
look up the variable sub to get the function object
---
look up the variable square, again, to get the function object
---
look up the variable y to get 3
---
run the square function on input 3, returning the value 9
---
look up the variable x, again, to get 2
---
multiply 2 * 2 to get 4
---
run the sub function, passing inputs 9 and 4, returning the value 5
---
add 2 and 5 to get 7
---
run the square function, again, on input 7, returning the value 49
        
```
:::
:::
:::

::: {style="width: 100%"}
::: {ea-publisher="runestoneacademy" ea-type="image" style="display: flex; justify-content: center"}
:::
:::

::: {#scprogresscontainer}
You have attempted []{#scprogresstotal} of []{#scprogressposs}
activities on this page

::: {#subchapterprogress aria-label="Page progress"}
:::
:::

-   [[](WPChoosingtheRightVariableName.html)]{#relations-prev}
-   [[](OrderofOperations.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
