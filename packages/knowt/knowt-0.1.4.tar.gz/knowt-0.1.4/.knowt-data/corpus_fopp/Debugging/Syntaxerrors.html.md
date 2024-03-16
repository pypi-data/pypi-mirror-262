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
        Problem](/runestone/default/reportabug?course=fopp&page=Syntaxerrors)
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
::: {#syntax-errors .section}
[]{#index-0}

[3.5. ]{.section-number}Syntax errors[¶](#syntax-errors "Permalink to this heading"){.headerlink}
=================================================================================================

Python can only execute a program if the program is syntactically
correct; otherwise, the process fails and returns an error message.
**Syntax** refers to the structure of a program and the rules about that
structure. For example, in English, a sentence must begin with a capital
letter and end with a period. this sentence contains a **syntax error**.
So does this one

In Python, rules of syntax include requirements like these: strings must
be enclosed in quotes; statements must generally be written one per
line; the print statement must enclose the value to be displayed in
parenthesis; expressions must be correctly formed. The following lines
contain syntax errors:

::: {.highlight-default .notranslate}
::: {.highlight}
    print(Hello, world!)
    print "Hello, world!"
    print(5 + )
:::
:::

For most readers of English, a few syntax errors are not a significant
problem, which is why we can read the poetry of e. e. cummings without
problems. Python is not so forgiving. When you run a Python program, the
interpreter checks it for syntax errors before beginning to execute the
first statement. If there is a single syntax error anywhere in your
program, Python will display an error message and quit without executing
*any* of the program.

To see a syntax error in action, look at the following program. Can you
spot the error? After locating the error, run the program to see the
error message.

::: {.runestone .explainer .ac_section}
::: {#debug_syntaxerr component="activecode" question_label="3.5.1"}
::: {#debug_syntaxerr_question .ac_question}
:::
:::
:::

Notice the following:

1.  The error message clearly indicates that the problem is a
    `SyntaxError`{.docutils .literal .notranslate}. This lets you know
    the problem is not one of the other two types of errors we'll
    discuss shortly.

2.  The error is on line 2 of the program. However, even though there is
    nothing wrong with line 1, the print statement does not execute ---
    **none** of the program successfully executes because of the
    presence of just one syntax error.

3.  The error gives the line number where Python believes the error
    exists. In this case, the error message pinpoints the location
    correctly. But in other cases, the line number can be inaccurate or
    entirely missing.

    To see an example of the latter, try removing just the **right**
    parenthesis `)`{.docutils .literal .notranslate} from line 2 and
    running the program again. Notice how the error message gives no
    line number at all. With syntax errors, you need to be prepared to
    hunt around a bit in order to locate the trouble.

One aspect of syntax you have to watch out for in Python involves
indentation. Python requires you to begin all statements at the
beginning of the line, unless you are using a flow control statement
like a `for`{.docutils .literal .notranslate} or an `if`{.docutils
.literal .notranslate} statement (we'll discuss these soon... stay
tuned!). To see an example of this kind of problem, modify the program
above by inserting a couple of spaces at the beginning of one of the
lines.

**Check your understanding**

::: {.runestone}
-   [Attempting to divide by 0.]{#question4_4_1_opt_a}
-   A syntax error is an error in the structure of the python code that
    can be detected before the program is executed. Python cannot
    usually tell if you are trying to divide by 0 until it is executing
    your program (e.g., you might be asking the user for a value and
    then dividing by that value---you cannot know what value the user
    will enter before you run the program).
-   [Forgetting a right-parenthesis ) when invoking a
    function.]{#question4_4_1_opt_b}
-   This is a problem with the formal structure of the program. Python
    knows where parentheses are required and can detect when one is
    missing simply by analyzing the code without running it.
-   [Forgetting to divide by 100 when printing a percentage
    amount.]{#question4_4_1_opt_c}
-   This will produce the wrong answer, but Python will not consider it
    an error at all. The programmer is the one who understands that the
    answer produced is wrong.
:::

::: {.runestone}
-   [The programmer.]{#question4_4_2_opt_a}
-   Programmers rarely find all the syntax errors, there is a computer
    program that will do it for us.
-   [The compiler / interpreter.]{#question4_4_2_opt_b}
-   The compiler and / or interpreter is a computer program that
    determines if your program is written in a way that can be
    translated into machine language for execution.
-   [The computer.]{#question4_4_2_opt_c}
-   Well, sort of. But it is a special thing in the computer that does
    it. The stand alone computer without this additional piece can not
    do it.
-   [The teacher / instructor.]{#question4_4_2_opt_d}
-   Your teacher and instructor may be able to find most of your syntax
    errors, but only because they have experience looking at code and
    possibly writing code. With experience syntax errors are easier to
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

-   [[](BeginningtipsforDebugging.html)]{#relations-prev}
-   [[](RuntimeErrors.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
