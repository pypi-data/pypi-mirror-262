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
        Problem](/runestone/default/reportabug?course=fopp&page=RuntimeErrors)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [3.1 Introduction to
        Debugging](intro-DebuggingGeneral.html){.reference .internal}
    -   [3.2 👩‍💻 Programming in the Real
        World](intro-HowtobeaSuccessfulProgrammer.html){.reference
        .internal}
    -   [3.4 👩‍💻 Beginning tips for
        Debugging](BeginningtipsforDebugging.html){.reference .internal}
    -   [3.5 Syntax errors](Syntaxerrors.html){.reference .internal}
    -   [3.6 Runtime Errors](RuntimeErrors.html){.reference .internal}
    -   [3.7 Semantic Errors](SemanticErrors.html){.reference .internal}
    -   [3.8 👩‍💻 Know Your Error
        Messages](KnowyourerrorMessages.html){.reference .internal}
    -   [3.9 Exercises](Exercises.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#runtime-errors .section}
[]{#index-0}

[3.6. ]{.section-number}Runtime Errors[¶](#runtime-errors "Permalink to this heading"){.headerlink}
===================================================================================================

The second type of error is a **runtime error**. A program with a
runtime error is one that passed the interpreter's syntax checks, and
started to execute. However, during the execution of one of the
statements in the program, an error occurred that caused the interpreter
to stop executing the program and display an error message. Runtime
errors are also called **exceptions** because they usually indicate that
something exceptional (and bad) has happened.

Here are some examples of common runtime errors you are sure to
encounter:

-   Misspelled or incorrectly capitalized variable and function names

-   Attempts to perform operations (such as math operations) on data of
    the wrong type (ex. attempting to subtract two variables that hold
    string values)

-   Dividing by zero

-   Attempts to use a type conversion function such as `int`{.docutils
    .literal .notranslate} on a value that can't be converted to an int

The following program contains various runtime errors. Can you spot any
of them? After locating the error, run the program to see the error
message.

::: {.runestone .explainer .ac_section}
::: {#debug_rterr component="activecode" question_label="3.6.1"}
::: {#debug_rterr_question .ac_question}
:::
:::
:::

Notice the following important differences between syntax errors and
runtime errors that can help you as you try to diagnose and repair the
problem:

-   If the error message mentions `SyntaxError`{.docutils .literal
    .notranslate}, you know that the problem has to do with syntax: the
    structure of the code, the punctuation, etc.

-   If the program runs partway and then crashes, you know the problem
    is a runtime error. Programs with syntax errors don't execute even
    one line.

Stay tuned for more details on the various types of runtime errors. We
have a whole section of this chapter dedicated to that topic.

**Check your understanding**

::: {.runestone}
-   [Attempting to divide by 0.]{#question4_5_1_opt_a}
-   Python cannot reliably tell if you are trying to divide by 0 until
    it is executing your program (e.g., you might be asking the user for
    a value and then dividing by that value---you cannot know what value
    the user will enter before you run the program).
-   [Forgetting a right-parenthesis ) when invoking a
    function.]{#question4_5_1_opt_b}
-   This is a problem with the formal structure of the program. Python
    knows where colons are required and can detect when one is missing
    simply by looking at the code without running it.
-   [Forgetting to divide by 100 when printing a percentage
    amount.]{#question4_5_1_opt_c}
-   This will produce the wrong answer, but Python will not consider it
    an error at all. The programmer is the one who understands that the
    answer produced is wrong.
:::

::: {.runestone}
-   [The programmer.]{#question4_5_2_opt_a}
-   Programmers rarely find all the runtime errors, there is a computer
    program that will do it for us.
-   [The interpreter.]{#question4_5_2_opt_b}
-   If an instruction is illegal to perform at that point in the
    execution, the interpreter will stop with a message describing the
    exception.
-   [The computer.]{#question4_5_2_opt_c}
-   Well, sort of. But it is a special thing in the computer that does
    it. The stand alone computer without this additional piece can not
    do it.
-   [The teacher / instructor.]{#question4_5_2_opt_d}
-   Your teacher and instructor may be able to find most of your runtime
    errors, but only because they have experience looking at code and
    possibly writing code. With experience runtime errors are easier to
    find. But we also have an automated way of finding these types of
    errors.
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

-   [[](Syntaxerrors.html)]{#relations-prev}
-   [[](SemanticErrors.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
