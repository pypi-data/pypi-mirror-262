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
        Problem](/runestone/default/reportabug?course=fopp&page=FunctionInvocation)
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
::: {#adcopy_1 .adcopy style="display: none;"}
#### Before you keep reading\...

Runestone Academy can only continue if we get support from individuals
like you. As a student you are well aware of the high cost of textbooks.
Our mission is to provide great books to you for free, but we ask that
you consider a \$10 donation, more if you can or less if \$10 is a
burden.

::: {.donateb}
[Support Runestone Academy Today](/runestone/default/donate?ad=1){.btn
.btn-info}
:::

::: {#adcopy_2 .adcopy style="display: none;"}
#### Before you keep reading\...

Making great stuff takes time and \$\$. If you appreciate the book you
are reading now and want to keep quality materials free for other
students please consider a donation to Runestone Academy. We ask that
you consider a \$10 donation, but if you can give more thats great, if
\$10 is too much for your budget we would be happy with whatever you can
afford as a show of support.

::: {.donateb}
[Support Runestone Academy Today](/runestone/default/donate?ad=2){.btn
.btn-info}
:::
:::
:::

::: {#function-invocation .section}
[12.3. ]{.section-number}Function Invocation[¶](#function-invocation "Permalink to this heading"){.headerlink}
==============================================================================================================

Defining a new function does not make the function run. To execute the
function, we need a **function call**. This is also known as a
**function invocation**.

::: {.admonition .note}
Note

This section is a review of something we learned in the beginning of the
textbook.
:::

The way to invoke a function is to refer to it by name, followed by
parentheses. Since there are no parameters for the function hello, we
won't need to put anything inside the parentheses when we call it. Once
we've defined a function, we can call it as often as we like and its
statements will be executed each time we call it.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="12.3.1"}
::: {#clens11_2_1_question .ac_question}
:::

::: {#clens11_2_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 12.3.1 (clens11\_2\_1)]{.runestone_caption_text}
:::
:::

Let's take a closer look at what happens when you define a function and
when you execute the function. Try stepping through the code above.

First, note that in Step 1, when it executes line 1, it does *not*
execute lines 2 and 3. Instead, as you can see in blue "Global
variables" area, it creates a variable named hello whose value is a
python function object. In the diagram that object is labeled hello()
with a notation above it that it is a function.

At Step 2, the next line of code to execute is line 5. Just to emphasize
that hello is a variable like any other, and that functions are python
objects like any other, just of a particular type, line 5 prints out the
type of the object referred to by the variable hello. It's type is
officially 'function'.

Line 6 is just there to remind you of the difference between referring
to the variable name (function name) hello and referring to the string
"hello".

At Step 4 we get to line 8, which has an invocation of the function. The
way function invocation works is that the code block inside the function
definition is executed in the usual way, but at the end, execution jumps
to the point after the function invocation.

You can see that by following the next few steps. At Step 5, the red
arrow has moved to line 2, which will execute next. We say that *control
has passed* from the top-level program to the function hello. After
Steps 5 and 6 print out two lines, at Step 7, control will be passed
back to the point after where the invocation was started. At Step 8,
that has happened.

The same process of invocation occurs again on line 10, with lines 2 and
3 getting executed a second time.

::: {.admonition-common-mistake-with-functions .admonition}
Common Mistake with Functions

It is a common mistake for beginners to forget their parenthesis after
the function name. This is particularly common in the case where there
parameters are not required. Because the hello function defined above
does not require parameters, it's easy to forget the parenthesis. This
is less common, but still possible, when trying to call functions that
require parameters.
:::

**Check your understanding**

::: {.runestone}
-   [A named sequence of statements.]{#question11_2_1_opt_a}
-   Yes, a function is a named sequence of statements.
-   [Any sequence of statements.]{#question11_2_1_opt_b}
-   While functions contain sequences of statements, not all sequences
    of statements are considered functions.
-   [A mathematical expression that calculates a
    value.]{#question11_2_1_opt_c}
-   While some functions do calculate values, the python idea of a
    function is slightly different from the mathematical idea of a
    function in that not all functions calculate values. Consider, for
    example, the turtle functions in this section. They made the turtle
    draw a specific shape, rather than calculating a value.
-   [A statement of the form x = 5 + 4.]{#question11_2_1_opt_d}
-   This statement is called an assignment statement. It assigns the
    value on the right (9), to the name on the left (x).
:::

::: {.runestone}
-   [To improve the speed of execution]{#question11_2_2_opt_a}
-   Functions have little effect on how fast the program runs.
-   [To help the programmer organize programs into chunks that match how
    they think about the solution to the
    problem.]{#question11_2_2_opt_b}
-   While functions are not required, they help the programmer better
    think about the solution by organizing pieces of the solution into
    logical chunks that can be reused.
-   [All Python programs must be written using
    functions]{#question11_2_2_opt_c}
-   In the first several chapters, you have seen many examples of Python
    programs written without the use of functions. While writing and
    using functions is desirable and essential for good programming
    style as your programs get longer, it is not required.
-   [To calculate values.]{#question11_2_2_opt_d}
-   Not all functions calculate values.
:::

::: {.runestone}
-   [0]{#question11_2_3_opt_a}
-   The code only defines the function. Nothing prints until the
    function is called.
-   [1]{#question11_2_3_opt_b}
-   Check again.
-   [2]{#question11_2_3_opt_c}
-   When the function is invoked, it will print two lines, but it has
    only been defined, not invoked.
:::

::: {.runestone}
-   [0]{#question11_2_4_opt_a}
-   Here the the function is invoked and there is also a separate print
    statement.
-   [1]{#question11_2_4_opt_b}
-   There is only one print statement outside the funciton, but the
    invocations of hello also cause lines to print.
-   [3]{#question11_2_4_opt_c}
-   There are three print statements, but the function is invoked more
    than once.
-   [4]{#question11_2_4_opt_d}
-   Each time the function is invoked, it will print two lines, not one.
-   [7]{#question11_2_4_opt_e}
-   Three invocations generate two lines each, plus the line \"It
    works\".
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

-   [[](FunctionDefinitions.html)]{#relations-prev}
-   [[](FunctionParameters.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
