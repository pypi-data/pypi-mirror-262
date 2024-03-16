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
        Problem](/runestone/default/reportabug?course=fopp&page=SemanticErrors)
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
::: {#semantic-errors .section}
[]{#index-0}

[3.7. ]{.section-number}Semantic Errors[¶](#semantic-errors "Permalink to this heading"){.headerlink}
=====================================================================================================

The third type of error is the **semantic error**, also called a **logic
error**. If there is a semantic error in your program, it will run
successfully in the sense that the computer will not generate any error
messages. However, your program will not do the right thing. It will do
something else. Specifically, it will do what you **told** it to do, not
what you **wanted** it to do.

The following program has a semantic error. Execute it to see what goes
wrong:

::: {.runestone .explainer .ac_section}
::: {#logicerr_sum component="activecode" question_label="3.7.1"}
::: {#logicerr_sum_question .ac_question}
:::
:::
:::

This program runs and produces a result. However, the result is not what
the programmer intended. It contains a semantic error. The error is that
the program performs concatenation instead of addition, because the
programmer failed to write the code necessary to convert the inputs to
integers.

With semantic errors, the problem is that the program you wrote is not
the program you wanted to write. The meaning of the program (its
semantics) is wrong. The computer is faithfully carrying out the
instructions you wrote, and its results are correct, given the
instructions that you provided. However, because your instructions have
a flaw in their design, the program does not behave as desired.

Identifying semantic errors can be tricky because no error message
appears to make it obvious that the results are incorrect. The only way
you can detect semantic errors is if you *know in advance* what the
program should do for a given set of input. Then, you run the program
with that input data and compare the output of the program with what you
expect. If there is a discrepancy between the actual output and the
expected output, you can conclude that there is either 1) a semantic
error or 2) an error in your expected results.

Once you've determined that you have a semantic error, locating it can
be tricky because you must work backward by looking at the output of the
program and trying to figure out what it is doing.

::: {#test-cases .section}
[3.7.1. ]{.section-number}Test Cases[¶](#test-cases "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------

To detect a semantic error in your program, you need the help of
something called a test case.

::: {.admonition-test-case .admonition}
Test Case

A **test case** is a set of input values for the program, together with
the output that you expect the program should produce when it is run
with those particular inputs.
:::

Here is an example of a test case for the program above:

::: {.highlight-default .notranslate}
::: {.highlight}
    Test Case
    ---------
    Input: 2, 3
    Expected Output: 5
:::
:::

If you give this test case to someone and ask them to test the program,
they can type in the inputs, observe the output, check it against the
expected output, and determine whether a semantic error exists based on
whether the actual output matches the expected output or not. The tester
doesn't even have to know what the program is supposed to do. For this
reason, software companies often have separate quality assurance
departments whose responsibility is to check that the programs written
by the programmers perform as expected. The testers don't have to be
programmers; they just have to be able to operate the program and
compare its results with the test cases they're given.

In this case, the program is so simple that we don't need to write down
a test case at all; we can compute the expected output in our heads with
very little effort. More complicated programs require effort to create
the test case (since you shouldn't use the program to compute the
expected output; you have to do it with a calculator or by hand), but
the effort pays off when the test case helps you to identify a semantic
error that you didn't know existed.

Semantic errors are the most dangerous of the three types of errors,
because in some cases they are not noticed by either the programmers or
the users who use the program. Syntax errors cannot go undetected (the
program won't run at all if they exist), and runtime errors are usually
also obvious and typically detected by developers before a program is
released for use (although it is possible for a runtime error to occur
for some inputs and not for others, so these can sometimes remain
undetected for a while). However, programs often go for years with
undetected semantic errors; no one realizes that the program has been
producing incorrect results. They just assume that because the results
seem reasonable, they are correct. Sometimes, these errors are
relatively harmless. But if they involve financial transactions or
medical equipment, the results can be harmful or even deadly. For this
reason, creating test cases is an important part of the work that
programmers perform in order to help them produce programs that work
correctly.

**Check your understanding**

::: {.runestone}
-   [Attempting to divide by 0.]{#question4_6_1_opt_a}
-   A semantic error is an error in logic. In this case the program does
    not produce the correct output because the problem is not solved
    correctly. This would be considered a run-time error.
-   [Forgetting a right-parenthesis ) when invoking a
    function.]{#question4_6_1_opt_b}
-   A semantic error is an error in logic. In this case the program does
    not produce the correct output because the code can not be processed
    by the compiler or interpreter. This would be considered a syntax
    error.
-   [Forgetting to divide by 100 when printing a percentage
    amount.]{#question4_6_1_opt_c}
-   This will produce the wrong answer because the programmer
    implemented the solution incorrectly. This is a semantic error.
:::

::: {.runestone}
-   [The programmer.]{#question4_6_2_opt_a}
-   You must fully understand the problem so that you can tell if your
    program properly solves it.
-   [The compiler / interpreter.]{#question4_6_2_opt_b}
-   The compiler and / or interpreter will only do what you instruct it
    to do. It does not understand what the problem is that you want to
    solve.
-   [The computer.]{#question4_6_2_opt_c}
-   The computer does not understand your problem. It just executes the
    instructions that it is given.
-   [The teacher / instructor.]{#question4_6_2_opt_d}
-   Your teacher and instructor may be able to find most of your
    semantic errors, but only because they have experience solving
    problems. However it is your responsibility to understand the
    problem so you can develop a correct solution.
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

-   [[](RuntimeErrors.html)]{#relations-prev}
-   [[](KnowyourerrorMessages.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
