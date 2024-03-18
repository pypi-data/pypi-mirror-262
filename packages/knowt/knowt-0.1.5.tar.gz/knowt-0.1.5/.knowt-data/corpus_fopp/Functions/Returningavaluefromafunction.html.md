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
        Problem](/runestone/default/reportabug?course=fopp&page=Returningavaluefromafunction)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [12.1 Introduction to
        Functions](intro-Functions.html){.reference .internal}
    -   [12.2 Function Definition](FunctionDefinitions.html){.reference
        .internal}
    -   [12.3 Function Invocation](FunctionInvocation.html){.reference
        .internal}
    -   [12.4 Function Parameters](FunctionParameters.html){.reference
        .internal}
    -   [12.5 Returning a value from a
        function](Returningavaluefromafunction.html){.reference
        .internal}
    -   [12.6 👩‍💻 Decoding a
        Function](DecodingaFunction.html){.reference .internal}
    -   [12.7 Type Annotations](TypeAnnotations.html){.reference
        .internal}
    -   [12.8 A function that
        accumulates](Afunctionthataccumulates.html){.reference
        .internal}
    -   [12.9 Variables and parameters are
        local](Variablesandparametersarelocal.html){.reference
        .internal}
    -   [12.10 Global Variables](GlobalVariables.html){.reference
        .internal}
    -   [12.11 Functions can call other functions
        (Composition)](Functionscancallotherfunctions.html){.reference
        .internal}
    -   [12.12 Flow of Execution
        Summary](FlowofExecutionSummary.html){.reference .internal}
    -   [12.13 👩‍💻 Print vs. return](Printvsreturn.html){.reference
        .internal}
    -   [12.14 Passing Mutable
        Objects](PassingMutableObjects.html){.reference .internal}
    -   [12.15 Side Effects](SideEffects.html){.reference .internal}
    -   [12.16 Glossary](Glossary.html){.reference .internal}
    -   [12.17 Exercises](Exercises.html){.reference .internal}
    -   [12.18 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#returning-a-value-from-a-function .section}
[12.5. ]{.section-number}Returning a value from a function[¶](#returning-a-value-from-a-function "Permalink to this heading"){.headerlink}
==========================================================================================================================================

![gif of a box labeled function with three spaces on the top for input
and a space on the bottom for output. Three arrows enter the top and are
labeled as input or arguments. The function box shakes, and then one
arrow leaves the bottom of the function
box.](../_images/function_call.gif)

Not only can you pass a parameter value into a function, a function can
also produce a value. You have already seen this in some previous
functions that you have used. For example, `len`{.docutils .literal
.notranslate} takes a list or string as a parameter value and returns a
number, the length of that list or string. `range`{.docutils .literal
.notranslate} takes an integer as a parameter value and returns a list
containing all the numbers from 0 up to that parameter value.

Functions that return values are sometimes called **fruitful
functions**. In many other languages, a function that doesn't return a
value is called a **procedure**, but we will stick here with the Python
way of also calling it a function, or if we want to stress it, a
*non-fruitful* function.

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#goog_return_values .align-left .youtube-video component="youtube" video-height="315" question_label="12.5.1" video-width="560" video-videoid="LGOZyrRCJ1o" video-divid="goog_return_values" video-start="0" video-end="-1"}
:::
:::

![](../_images/blackboxfun.png)

How do we write our own fruitful function? Let's start by creating a
very simple mathematical function that we will call `square`{.docutils
.literal .notranslate}. The square function will take one number as a
parameter and return the result of squaring that number. Here is the
black-box diagram with the Python code following.

![](../_images/squarefun.png)

::: {.runestone .explainer .ac_section}
::: {#ac11_4_1 component="activecode" question_label="12.5.2"}
::: {#ac11_4_1_question .ac_question}
:::
:::
:::

The **return** statement is followed by an expression which is
evaluated. Its result is returned to the caller as the "fruit" of
calling this function. Because the return statement can contain any
Python expression we could have avoided creating the **temporary
variable** `y`{.docutils .literal .notranslate} and simply used
`return x*x`{.docutils .literal .notranslate}. Try modifying the square
function above to see that this works just the same. On the other hand,
using **temporary variables** like `y`{.docutils .literal .notranslate}
in the program above makes debugging easier. These temporary variables
are referred to as **local variables**.

Notice something important here. The name of the variable we pass as an
argument --- `toSquare`{.docutils .literal .notranslate} --- has nothing
to do with the name of the formal parameter --- `x`{.docutils .literal
.notranslate}. It is as if `x = toSquare`{.docutils .literal
.notranslate} is executed when `square`{.docutils .literal .notranslate}
is called. It doesn't matter what the value was named in the caller (the
place where the function was invoked). Inside `square`{.docutils
.literal .notranslate}, it's name is `x`{.docutils .literal
.notranslate}. You can see this very clearly in codelens, where the
global variables and the local variables for the square function are in
separate boxes.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="12.5.3"}
::: {#clens11_4_1_question .ac_question}
:::

::: {#clens11_4_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 12.5.3 (clens11\_4\_1)]{.runestone_caption_text}
:::
:::

There is one more aspect of function return values that should be noted.
All Python functions return the special value `None`{.docutils .literal
.notranslate} unless there is an explicit return statement with a value
other than `None`{.docutils .literal .notranslate}. Consider the
following common mistake made by beginning Python programmers. As you
step through this example, pay very close attention to the return value
in the local variables listing. Then look at what is printed when the
function is over.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="12.5.4"}
::: {#clens11_4_2_question .ac_question}
:::

::: {#clens11_4_2 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 12.5.4 (clens11\_4\_2)]{.runestone_caption_text}
:::
:::

The problem with this function is that even though it prints the value
of the squared input, that value will not be returned to the place where
the call was done. Instead, the value `None`{.docutils .literal
.notranslate} will be returned. Since line 6 uses the return value as
the right hand side of an assignment statement, `squareResult`{.docutils
.literal .notranslate} will have `None`{.docutils .literal .notranslate}
as its value and the result printed in line 7 is incorrect. Typically,
functions will return values that can be printed or processed in some
other way by the caller.

A return statement, once executed, immediately terminates execution of a
function, even if it is not the last statement in the function. In the
following code, when line 3 executes, the value 5 is returned and
assigned to the variable x, then printed. Lines 4 and 5 never execute.
Run the following code and try making some modifications of it to make
sure you understand why "there" and 10 never print out.

::: {.runestone .explainer .ac_section}
::: {#ac11_4_2 component="activecode" question_label="12.5.5"}
::: {#ac11_4_2_question .ac_question}
:::
:::
:::

The fact that a return statement immediately ends execution of the code
block inside a function is important to understand for writing complex
programs, and it can also be very useful. The following example is a
situation where you can use this to your advantage -- and understanding
this will help you understand other people's code better, and be able to
walk through code more confidently.

Consider a situation where you want to write a function to find out,
from a class attendance list, whether anyone's first name is longer than
five letters, called `longer_than_five`{.docutils .literal
.notranslate}. If there is anyone in class whose first name is longer
than 5 letters, the function should return `True`{.docutils .literal
.notranslate}. Otherwise, it should return `False`{.docutils .literal
.notranslate}.

In this case, you'll be using conditional statements in the code that
exists in the **function body**, the code block indented underneath the
function definition statement (just like the code that starts with the
line `print("here")`{.docutils .literal .notranslate} in the example
above -- that's the body of the function `weird`{.docutils .literal
.notranslate}, above).

**Bonus challenge for studying:** After you look at the explanation
below, stop looking at the code -- just the description of the function
above it, and try to write the code yourself! Then test it on different
lists and make sure that it works. But read the explanation first, so
you can be sure you have a solid grasp on these function mechanics.

First, an English plan for this new function to define called
`longer_than_five`{.docutils .literal .notranslate}:

-   You'll want to pass in a list of strings (representing people's
    first names) to the function.

-   You'll want to iterate over all the items in the list, each of the
    strings.

-   As soon as you get to one name that is longer than five letters, you
    know the function should return `True`{.docutils .literal
    .notranslate} -- yes, there is at least one name longer than five
    letters!

-   And if you go through the whole list and there was no name longer
    than five letters, then the function should return `False`{.docutils
    .literal .notranslate}.

Now, the code:

::: {.runestone .explainer .ac_section}
::: {#ac11_4_3 component="activecode" question_label="12.5.6"}
::: {#ac11_4_3_question .ac_question}
:::
:::
:::

So far, we have just seen return values being assigned to variables. For
example, we had the line `squareResult = square(toSquare)`{.docutils
.literal .notranslate}. As with all assignment statements, the right
hand side is executed first. It invokes the `square`{.docutils .literal
.notranslate} function, passing in a parameter value 10 (the current
value of `toSquare`{.docutils .literal .notranslate}). That returns a
value 100, which completes the evaluation of the right-hand side of the
assignment. 100 is then assigned to the variable
`squareResult`{.docutils .literal .notranslate}. In this case, the
function invocation was the entire expression that was evaluated.

Function invocations, however, can also be used as part of more
complicated expressions. For example,
`squareResult = 2 * square(toSquare)`{.docutils .literal .notranslate}.
In this case, the value 100 is returned and is then multiplied by 2 to
produce the value 200. When python evaluates an expression like
`x * 3`{.docutils .literal .notranslate}, it substitutes the current
value of x into the expression and then does the multiplication. When
python evaluates an expression like `2 * square(toSquare)`{.docutils
.literal .notranslate}, it substitutes the return value 100 for entire
function invocation and then does the multiplication.

To reiterate, when executing a line of code
`squareResult = 2 * square(toSquare)`{.docutils .literal .notranslate},
the python interpreter does these steps:

1.  It's an assignment statement, so evaluate the right-hand side
    expression `2 * square(toSquare)`{.docutils .literal .notranslate}.

2.  Look up the values of the variables square and toSquare: square is a
    function object and toSquare is 10

3.  Pass 10 as a parameter value to the function, get back the return
    value 100

4.  Substitute 100 for square(toSquare), so that the expression now
    reads `2 * 100`{.docutils .literal .notranslate}

5.  Assign 200 to variable `squareResult`{.docutils .literal
    .notranslate}

**Check your understanding**

::: {.runestone}
-   [You should never use a print statement in a function
    definition.]{#question11_4_1_opt_a}
-   Although you should not mistake print for return, you may include
    print statements inside your functions.
-   [You should not have any statements in a function after the return
    statement. Once the function gets to the return statement it will
    immediately stop executing the function.]{#question11_4_1_opt_b}
-   This is a very common mistake so be sure to watch out for it when
    you write your code!
-   [You must calculate the value of x+y+z before you return
    it.]{#question11_4_1_opt_c}
-   Python will automatically calculate the value x+y+z and then return
    it in the statement as it is written
-   [A function cannot return a number.]{#question11_4_1_opt_d}
-   Functions can return any legal data, including (but not limited to)
    numbers, strings, lists, dictionaries, etc.
:::

::: {.runestone}
-   [The value None]{#question11_4_2_opt_a}
-   We have accidentally used print where we mean return. Therefore, the
    function will return the value None by default. This is a VERY
    COMMON mistake so watch out! This mistake is also particularly
    difficult to find because when you run the function the output looks
    the same. It is not until you try to assign its value to a variable
    that you can notice a difference.
-   [The value of x+y+z]{#question11_4_2_opt_b}
-   Careful! This is a very common mistake. Here we have printed the
    value x+y+z but we have not returned it. To return a value we MUST
    use the return keyword.
-   [The string \'x+y+z\']{#question11_4_2_opt_c}
-   x+y+z calculates a number (assuming x+y+z are numbers) which
    represents the sum of the values x, y and z.
:::

::: {.runestone}
-   [25]{#question11_4_3_opt_a}
-   It squares 5 twice, and adds them together.
-   [50]{#question11_4_3_opt_b}
-   The two return values are added together.
-   [25 + 25]{#question11_4_3_opt_c}
-   The two results are substituted into the expression and then it is
    evaluated. The returned values are integers in this case, not
    strings.
:::

::: {.runestone}
-   [8]{#question11_4_4_opt_a}
-   It squares 2, yielding the value 4. But that doesn\'t mean the next
    value multiplies 2 and 4.
-   [16]{#question11_4_4_opt_b}
-   It squares 2, yielding the value 4. 4 is then passed as a value to
    square again, yeilding 16.
-   [Error: can\'t put a function invocation inside
    parentheses]{#question11_4_4_opt_c}
-   This is a more complicated expression, but still valid. The
    expression square(2) is evaluated, and the return value 4
    substitutes for square(2) in the expression.
:::

::: {.runestone}
-   [1]{#question11_4_5_opt_a}
-   cyu2 returns the value 1, but that\'s not what prints.
-   [Yes]{#question11_4_5_opt_b}
-   \"Yes\" is longer, but that\'s not what prints.
-   [First one was longer]{#question11_4_5_opt_c}
-   cyu2 returns the value 1, which is assigned to z.
-   [Second one was at least as long]{#question11_4_5_opt_d}
-   cyu2 returns the value 1, which is assigned to z.
-   [Error]{#question11_4_5_opt_e}
-   what do you think will cause an error.
:::

::: {.runestone}
-   [square]{#question11_4_6_opt_a}
-   Before executing square, it has to figure out what value to pass in,
    so g is executed first
-   [g]{#question11_4_6_opt_b}
-   g has to be executed and return a value in order to know what
    paramater value to provide to x.
-   [a number]{#question11_4_6_opt_c}
-   square and g both have to execute before the number is printed.
:::

::: {.runestone}
-   [3]{#question11_4_7_opt_a}
-   The function gets to a return statement after 2 lines are printed,
    so the third print statement will not run.
-   [2]{#question11_4_7_opt_b}
-   Yes! Two printed lines, and then the function body execution reaches
    a return statement.
-   [None]{#question11_4_7_opt_c}
-   The function returns an integer value! However, this code does not
    print out the result of the function invocation, so you can\'t see
    it (print is for people). The only lines you see printed are the
    ones that occur in the print statements before the return statement.
:::

::: {.runestone .explainer .ac_section}
::: {#ac11_4_4 component="activecode" question_label="12.5.14"}
::: {#ac11_4_4_question .ac_question}
**8.** Write a function named `same`{.docutils .literal .notranslate}
that takes a string as input, and simply returns that string.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac11_4_5 component="activecode" question_label="12.5.15"}
::: {#ac11_4_5_question .ac_question}
**9.** Write a function called `same_thing`{.docutils .literal
.notranslate} that returns the parameter, unchanged.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac11_4_6 component="activecode" question_label="12.5.16"}
::: {#ac11_4_6_question .ac_question}
**10.** Write a function called `subtract_three`{.docutils .literal
.notranslate} that takes an integer or any number as input, and returns
that number minus three.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac11_4_7 component="activecode" question_label="12.5.17"}
::: {#ac11_4_7_question .ac_question}
**11.** Write a function called `change`{.docutils .literal
.notranslate} that takes one number as its input and returns that
number, plus 7.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac11_4_8 component="activecode" question_label="12.5.18"}
::: {#ac11_4_8_question .ac_question}
**12.** Write a function named `intro`{.docutils .literal .notranslate}
that takes a string as input. This string ist intended to be a person's
name and the output is a standardized greeting. For example, given the
string "Becky" as input, the function should return: "Hello, my name is
Becky and I love SI 106."
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac11_4_9 component="activecode" question_label="12.5.19"}
::: {#ac11_4_9_question .ac_question}
**13.** Write a function called `s_change`{.docutils .literal
.notranslate} that takes one string as input and returns that string,
concatenated with the string " for fun.".
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac11_4_10 component="activecode" question_label="12.5.20"}
::: {#ac11_4_10_question .ac_question}
**14.** Write a function called `decision`{.docutils .literal
.notranslate} that takes a string as input, and then checks the number
of characters. If it has over 17 characters, return "This is a long
string", if it is shorter or has 17 characters, return "This is a short
string".
:::
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

-   [[](FunctionParameters.html)]{#relations-prev}
-   [[](DecodingaFunction.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
