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
        Problem](/runestone/default/reportabug?course=fopp&page=intro-exceptions)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [19.1 What is an exception?](intro-exceptions.html){.reference
        .internal}
    -   [19.3 👩‍💻 When to use
        try/except](using-exceptions.html){.reference .internal}
    -   [19.4 Standard Exceptions](standard-exceptions.html){.reference
        .internal}
    -   [19.5 Exercises](Exercises.html){.reference .internal}
    -   [19.6 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#what-is-an-exception .section}
[]{#exceptions-chap}

[19.1. ]{.section-number}What is an exception?[¶](#what-is-an-exception "Permalink to this heading"){.headerlink}
=================================================================================================================

An *exception* is a signal that a condition has occurred that can't be
easily handled using the normal flow-of-control of a Python program.
*Exceptions* are often defined as being "errors" but this is not always
the case. All errors in Python are dealt with using *exceptions*, but
not all *exceptions* are errors.
:::

::: {#exception-handling-flow-of-control .section}
[19.2. ]{.section-number}Exception Handling Flow-of-control[¶](#exception-handling-flow-of-control "Permalink to this heading"){.headerlink}
============================================================================================================================================

To explain what an *exception* does, let's review the normal "flow of
control" in a Python program. In normal operation Python executes
statements sequentially, one after the other. For three constructs,
if-statements, loops and function invocations, this sequential execution
is interrupted.

-   For *if-statements*, only one of several statement blocks is
    executed and then flow-of-control jumps to the first statement after
    the if-statement.

-   For *loops*, when the end of the loop is reached, flow-of-control
    jumps back to the start of the loop and a test is used to determine
    if the loop needs to execute again. If the loop is finished,
    flow-of-control jumps to the first statement after the loop.

-   For *function invocations*, flow-of-control jumps to the first
    statement in the called function, the function is executed, and the
    flow-of-control jumps back to the next statement after the function
    call.

Do you see the pattern? If the flow-of-control is not purely sequential,
it always executes the first statement immediately following the altered
flow-of-control. That is why we can say that Python flow-of-control is
sequential. But there are cases where this sequential flow-of-control
does not work well.

Exceptions provide us with way way to have a non-sequential point where
we can handle something out of the ordinary (exceptional).

::: {#raising-and-catching-errors .section}
[19.2.1. ]{.section-number}Raising and Catching Errors[¶](#raising-and-catching-errors "Permalink to this heading"){.headerlink}
--------------------------------------------------------------------------------------------------------------------------------

The try/except control structure provides a way to process a run-time
error and continue on with program execution. Until now, any run-time
error, such asking for the 8th item in a list with only 3 items, or
dividing by 0, has caused the program execution to stop. In the browser
ActiveCode windows, you get an error message in a box below. When you
are executing python programs from the command-line, you also get an
error message saying something about what went wrong and what line it
occurred on. After the run-time error is encountered, the python
interpreter does not try to execute the rest of the code. You have to
make some change in your code and rerun the whole program.

With try/except, you tell the python interpreter:

-   

    Try to execute a block of code, the "try" clause.

    :   -   If the whole block of code executes without any run-time
            errors, just carry on with the rest of the program after the
            try/except statement.

-   

    If a run-time error does occur during execution of the block of code:

    :   -   skip the rest of that block of code (but don't exit the
            whole program)

        -   execute a block of code in the "except" clause

        -   then carry on with the rest of the program after the
            try/except statement

::: {.highlight-python .notranslate}
::: {.highlight}
    try:
       <try clause code block>
    except <ErrorType>:
       <exception handler code block>
:::
:::

The syntax is fairly straightforward. The only tricky part is that after
the word except, there can optionally be a specification of the kinds of
errors that will be handled. The catchall is the class Exception. If you
write `except Exception:`{.docutils .literal .notranslate} all runtime
errors will be handled. If you specify a more restricted class of
errors, only those errors will be handled; any other kind of error will
still cause the program to stop running and an error message to be
printed.

The code below causes an error of type IndexError, by trying to access
the third element of a two-element list.

::: {.runestone .explainer .ac_section}
::: {#exceptions_1 component="activecode" question_label="19.2.1.1"}
::: {#exceptions_1_question .ac_question}
:::
:::
:::

The code below causes an error of type ZeroDivisionError, or less
specifically ArithmeticError.

::: {.runestone .explainer .ac_section}
::: {#exceptions_2 component="activecode" question_label="19.2.1.2"}
::: {#exceptions_2_question .ac_question}
:::
:::
:::

Let's see what happens if we wrap some of this problematic code in a
try/except statement. Note that `this won't print`{.docutils .literal
.notranslate} doesn't print: when the error is encountered, the rest of
the try block is skipped and the exception block is executed. When the
except block is done, it continues on with the next line of code that's
outdented to the same level as the try: `continuing`{.docutils .literal
.notranslate} is printed.

::: {.runestone .explainer .ac_section}
::: {#exceptions_3 component="activecode" question_label="19.2.1.3"}
::: {#exceptions_3_question .ac_question}
:::
:::
:::

If we catch only IndexEror, and we actually have a divide by zero error,
the program does stop executing.

::: {.runestone .explainer .ac_section}
::: {#exceptions_4 component="activecode" question_label="19.2.1.4"}
::: {#exceptions_4_question .ac_question}
:::
:::
:::

There's one other useful feature. The exception code can access a
variable that contains information about exactly what the error was.
Thus, for example, in the except clause you could print out the
information that would normally be printed as an error message but
continue on with execution of the rest of the program. To do that, you
specify a variable name after the exception class that's being handled.
The exception clause code can refer to that variable name.

::: {.runestone .explainer .ac_section}
::: {#exceptions_5 component="activecode" question_label="19.2.1.5"}
::: {#exceptions_5_question .ac_question}
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [syntax]{#exceptions_mc_1_opt_a}
-   Syntax errors are things like missing colons or strings that are not
    terminated. Try/except will not help with those. The program still
    will not run.
-   [run-time]{#exceptions_mc_1_opt_b}
-   Run-time errors like index out of bounds can be caught and handled
    gracefully with try/except.
-   [semantic]{#exceptions_mc_1_opt_c}
-   If your program runs to completion but does the wrong thing,
    try/except won\'t help you.
:::

::: {.runestone}
-   [True]{#exceptions_mc_2_opt_a}
-   If your code is only catching IndexError errors, then the exception
    will not be handled, and execution will terminate.
-   [False]{#exceptions_mc_2_opt_b}
-   If your code is only catching IndexError errors, then the exception
    will not be handled, and execution will terminate.
:::

::: {.runestone}
-   [True]{#exceptions_mc_3_opt_a}
-   The rest of the code after the whole try/except statement will
    execute, but not the rest of the code in the try block.
-   [False]{#exceptions_mc_3_opt_b}
-   The rest of the code after the whole try/except statement will
    execute, but not the rest of the code in the try block.
:::

::: {.runestone}
-   [0]{#exceptions_mc_4_opt_a}
-   Try i = 0; that should print out .3333
-   [1]{#exceptions_mc_4_opt_b}
-   Keep trying.
-   [3]{#exceptions_mc_4_opt_c}
-   When i=3, it will no longer be able to pring 1.0/ (3-i), but it will
    still print one more line in the except clause.
-   [4]{#exceptions_mc_4_opt_d}
-   It will print the fraction for three values of i, and then one error
    message.
-   [5]{#exceptions_mc_4_opt_e}
-   When i=3, it will get a run-time error, and execution stops after
    that.
:::

::: {.runestone .explainer .ac_section}
::: {#ee_exceptions_012 component="activecode" question_label="19.2.1.10"}
::: {#ee_exceptions_012_question .ac_question}
5.  Below, we have provided a list of tuples that consist of student
    names, final exam scores, and whether or not they will pass the
    class. For some students, the tuple does not have a third element
    because it is unknown whether or not they will pass. Currently, the
    for loop does not work. Add a try/except clause so the code runs
    without an error - if there is no third element in the tuple, no
    changes should be made to the dictionary.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ee_exceptions_022 component="activecode" question_label="19.2.1.11"}
::: {#ee_exceptions_022_question .ac_question}
6.  Below, we have provided code that does not run. Add a try/except
    clause so the code runs without errors. If an element is not able to
    undergo the addition operation, the string 'Error' should be
    appended to plus\_four.
:::
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

-   [[](toctree.html)]{#relations-prev}
-   [[](using-exceptions.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
