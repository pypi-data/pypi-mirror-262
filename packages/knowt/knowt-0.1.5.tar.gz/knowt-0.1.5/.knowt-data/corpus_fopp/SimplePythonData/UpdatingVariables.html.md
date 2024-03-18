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
        Problem](/runestone/default/reportabug?course=fopp&page=UpdatingVariables)
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
::: {#updating-variables .section}
[2.13. ]{.section-number}Updating Variables[¶](#updating-variables "Permalink to this heading"){.headerlink}
============================================================================================================

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#updatevid .align-left .youtube-video component="youtube" video-height="315" question_label="2.13.1" video-width="560" video-videoid="Px1c-3GP-5o" video-divid="updatevid" video-start="0" video-end="-1"}
:::
:::

One of the most common forms of reassignment is an **update** where the
new value of the variable depends on the old. For example,

::: {.highlight-python .notranslate}
::: {.highlight}
    x = x + 1
:::
:::

This means get the current value of x, add one, and then update x with
the new value. The new value of x is the old value of x plus 1. Although
this assignment statement may look a bit strange, remember that
executing assignment is a two-step process. First, evaluate the
right-hand side expression. Second, let the variable name on the
left-hand side refer to this new resulting object. The fact that
`x`{.docutils .literal .notranslate} appears on both sides does not
matter. The semantics of the assignment statement makes sure that there
is no confusion as to the result. The visualizer makes this very clear.

::: {#se_ac2_14_1 .runestone .explainer component="showeval" question_label="2.13.2" tracemode="true"}
Next Step

Reset

::: {.evalCont style="background-color: #FDFDFD;"}
x = 6\
x = x + 1\
:::

::: {.evalCont}
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac2_14_1 component="activecode" question_label="2.13.3"}
::: {#ac2_14_1_question .ac_question}
:::
:::
:::

If you try to update a variable that doesn't exist, you get an error
because Python evaluates the expression on the right side of the
assignment operator before it assigns the resulting value to the name on
the left. Before you can update a variable, you have to **initialize**
it, usually with a simple assignment. In the above example,
`x`{.docutils .literal .notranslate} was initialized to 6.

Updating a variable by adding something to it is called an
**increment**; subtracting is called a **decrement**. Sometimes
programmers talk about incrementing or decrementing without specifying
by how much; when they do they usually mean by 1. Sometimes programmers
also talk about **bumping** a variable, which means the same as
incrementing it by 1.

Incrementing and decrementing are such common operations that
programming languages often include special syntax for it. In Python
`+=`{.docutils .literal .notranslate} is used for incrementing, and
`-=`{.docutils .literal .notranslate} for decrementing. In some other
languages, there is even a special syntax `++`{.docutils .literal
.notranslate} and `--`{.docutils .literal .notranslate} for incrementing
or decrementing by 1. Python does not have such a special syntax. To
increment x by 1 you have to write `x += 1`{.docutils .literal
.notranslate} or `x = x + 1`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#ac2_14_2 component="activecode" question_label="2.13.4"}
::: {#ac2_14_2_question .ac_question}
:::
:::
:::

Imagine that we wanted to not increment by one each time but instead add
together the numbers one through ten, but only one at a time.

::: {.runestone .explainer .ac_section}
::: {#ac2_14_3 component="activecode" question_label="2.13.5"}
::: {#ac2_14_3_question .ac_question}
:::
:::
:::

After the initial statement, where we assign `s`{.docutils .literal
.notranslate} to 1, we can add the current value of `s`{.docutils
.literal .notranslate} and the next number that we want to add (2 all
the way up to 10) and then finally reassign that that value to
`s`{.docutils .literal .notranslate} so that the variable is updated
after each line in the code.

This will be tedious when we have many things to add together. Later
you'll read about an easier way to do this kind of task.

**Check your understanding**

::: {.runestone}
-   [12]{#question2_14_1_opt_a}
-   The value of x changes in the second statement.
-   [-1]{#question2_14_1_opt_b}
-   In the second statement, substitute the current value of x before
    subtracting 1.
-   [11]{#question2_14_1_opt_c}
-   Yes, this statement sets the value of x equal to the current value
    minus 1.
-   [Nothing. An error occurs because x can never be equal to x -
    1.]{#question2_14_1_opt_d}
-   Remember that variables in Python are different from variables in
    math in that they (temporarily) hold values, but can be reassigned.
:::

::: {.runestone}
-   [12]{#question2_14_2_opt_a}
-   The value of x changes in the second statement.
-   [9]{#question2_14_2_opt_b}
-   Each statement changes the value of x, so 9 is not the final result.
-   [15]{#question2_14_2_opt_c}
-   Yes, starting with 12, subtract 3, than add 5, and finally add 1.
-   [Nothing. An error occurs because x cannot be used that many times
    in assignment statements.]{#question2_14_2_opt_d}
-   Remember that variables in Python are different from variables in
    math in that they (temporarily) hold values, but can be reassigned.
:::

::: {.runestone .parsons-container}
::: {#pp2_14_1 .parsons component="parsons"}
::: {.parsons_question .parsons-text}
Construct the code that will result in the value 134 being printed.
:::

``` {.parsonsblocks question_label="2.13.8" style="visibility: hidden;"}
        mybankbalance = 100
mybankbalance = mybankbalance + 34
print(mybankbalance)
        
```
:::
:::

::: {.runestone}
-   [x = x + y]{#question2_14_3_opt_a}
-   x is updated to be the old value of x plus the value of y.
-   [y += x]{#question2_14_3_opt_b}
-   y is updated to be the old value of y plus the value of x.
-   [x += x + y]{#question2_14_3_opt_c}
-   This updates x to be its old value (because of the +=) plus its old
    value again (because of the x on the right side) plus the value of
    y, so it\'s equivalent to x = x + x + y
-   [x += y]{#question2_14_3_opt_d}
-   x is updated to be the old value of x plus the value of y.
-   [x++ y]{#question2_14_3_opt_e}
-   ++ is not a syntax that means anything in Python.
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

-   [[](Reassignment.html)]{#relations-prev}
-   [[](HardCoding.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
