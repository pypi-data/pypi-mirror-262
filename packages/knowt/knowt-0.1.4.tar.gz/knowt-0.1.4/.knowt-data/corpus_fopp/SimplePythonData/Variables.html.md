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
        Problem](/runestone/default/reportabug?course=fopp&page=Variables)
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
::: {#variables .section}
[]{#id1}

[2.7. ]{.section-number}Variables[¶](#variables "Permalink to this heading"){.headerlink}
=========================================================================================

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#assignvid .align-left .youtube-video component="youtube" video-height="315" question_label="2.7.1" video-width="560" video-videoid="TrrzfHUtyVw" video-divid="assignvid" video-start="0" video-end="-1"}
:::
:::

One of the most powerful features of a programming language is the
ability to manipulate **variables**. A variable is a name that refers to
a value.

**Assignment statements** create new variables and also give them values
to refer to.

::: {.highlight-python .notranslate}
::: {.highlight}
    message = "What's up, Doc?"
    n = 17
    pi = 3.14159
:::
:::

This example makes three assignments. The first assigns the string value
`"What's up, Doc?"`{.docutils .literal .notranslate} to a new variable
named `message`{.docutils .literal .notranslate}. The second assigns the
integer `17`{.docutils .literal .notranslate} to `n`{.docutils .literal
.notranslate}, and the third assigns the floating-point number
`3.14159`{.docutils .literal .notranslate} to a variable called
`pi`{.docutils .literal .notranslate}.

The **assignment token**, `=`{.docutils .literal .notranslate}, should
not be confused with *equality* (we will see later that equality uses
the `==`{.docutils .literal .notranslate} token). The assignment
statement links a *name*, on the left hand side of the operator, with a
*value*, on the right hand side. This is why you will get an error if
you enter:

::: {.highlight-python .notranslate}
::: {.highlight}
    17 = n
:::
:::

::: {.admonition .tip}
Tip

When reading or writing code, say to yourself "n is assigned 17" or "n
gets the value 17" or "n is a reference to the object 17" or "n refers
to the object 17". **Don't say "n equals 17"**.
:::

A common way to represent variables on paper is to write the name with
an arrow pointing to the variable's value. This kind of figure, known as
a **reference diagram**, is often called a **state snapshot** because it
shows what state each of the variables is in at a particular instant in
time. (Think of it as the variable's state of mind). This diagram shows
the result of executing the assignment statements shown above.

![Reference Diagram](../_images/refdiagram1.png)

If your program includes a variable in any expression, whenever that
expression is executed it will produce the value that is linked to the
variable at the time of execution. In other words, evaluating a variable
looks up its value.

::: {.runestone .explainer .ac_section}
::: {#ac2_7_1 component="activecode" question_label="2.7.2"}
::: {#ac2_7_1_question .ac_question}
:::
:::
:::

In each case the result is the value of the variable. To see this in
even more detail, we can run the program using codelens.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="2.7.3"}
::: {#clens2_7_1_question .ac_question}
:::

::: {#clens2_7_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 2.7.3 (clens2\_7\_1)]{.runestone_caption_text}
:::
:::

Now, as you step through the statements, you can see the variables and
the values they reference as those references are created.

We use variables in a program to "remember" things, like the current
score at the football game. But variables are *variable*. This means
they can change over time, just like the scoreboard at a football game.
You can assign a value to a variable, and later assign a different value
to the same variable.

::: {.admonition .note}
Note

This is different from math. In algebra, if you give `x`{.docutils
.literal .notranslate} the value 3, it cannot change to refer to a
different value half-way through your calculations!
:::

To see this, read and then run the following program. You'll notice we
change the value of `day`{.docutils .literal .notranslate} three times,
and on the third assignment we even give it a value that is of a
different type.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="2.7.4"}
::: {#clens2_7_2_question .ac_question}
:::

::: {#clens2_7_2 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 2.7.4 (clens2\_7\_2)]{.runestone_caption_text}
:::
:::

A great deal of programming is about having the computer remember
things. For example, we might want to keep track of the number of missed
calls on your phone. Each time another call is missed, we will arrange
to update or change the variable so that it will always reflect the
correct value.

Any place in a Python program where a number or string is expected, you
can put a variable name instead. The python interpreter will substitute
the value for the variable name.

For example, we can find out the data type of the current value of a
variable by putting the variable name inside the parentheses following
the function name `type`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#ac2_7_2 component="activecode" question_label="2.7.5"}
::: {#ac2_7_2_question .ac_question}
:::
:::
:::

::: {.admonition .note}
Note

If you have programmed in another language such as Java or C++, you may
be used to the idea that *variables* have types that are declared when
the variable name is first introduced in a program. Python doesn't do
that. Variables don't have types in Python; *values* do. That means that
it is acceptable in Python to have a variable name refer to an integer
and later have the same variable name refer to a string. This is almost
never a good idea, because it will confuse human readers (including
you), but the Python interpreter will not complain.
:::

**Check your understanding**

::: {.runestone}
-   [Nothing is printed. A runtime error occurs.]{#question2_7_1_opt_a}
-   It is legal to change the type of data that a variable holds in
    Python.
-   [Thursday]{#question2_7_1_opt_b}
-   This is the first value assigned to the variable day, but the next
    statements reassign that variable to new values.
-   [32.5]{#question2_7_1_opt_c}
-   This is the second value assigned to the variable day, but the next
    statement reassigns that variable to a new value.
-   [19]{#question2_7_1_opt_d}
-   The variable day will contain the last value assigned to it when it
    is printed.
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

-   [[](ConvertTypeFunctions.html)]{#relations-prev}
-   [[](VariableNamesandKeywords.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
