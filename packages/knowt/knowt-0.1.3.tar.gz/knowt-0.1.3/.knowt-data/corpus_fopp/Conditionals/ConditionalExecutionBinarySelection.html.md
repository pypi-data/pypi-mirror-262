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
        Problem](/runestone/default/reportabug?course=fopp&page=ConditionalExecutionBinarySelection)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [8.1 Intro: What we can do with Turtles and
        Conditionals](intro-TurtlesandConditionals.html){.reference
        .internal}
    -   [8.2 Boolean Values and Boolean
        Expressions](BooleanValuesandBooleanExpressions.html){.reference
        .internal}
    -   [8.3 Logical operators](Logicaloperators.html){.reference
        .internal}
    -   [8.4 The in and not in
        operators](Theinandnotinoperators.html){.reference .internal}
    -   [8.5 Precedence of
        Operators](PrecedenceofOperators.html){.reference .internal}
    -   [8.6 Conditional Execution: Binary
        Selection](ConditionalExecutionBinarySelection.html){.reference
        .internal}
    -   [8.7 Omitting the else Clause: Unary
        Selection](OmittingtheelseClauseUnarySelection.html){.reference
        .internal}
    -   [8.8 Nested conditionals](Nestedconditionals.html){.reference
        .internal}
    -   [8.9 Chained conditionals](Chainedconditionals.html){.reference
        .internal}
    -   [8.10 The Accumulator Pattern with
        Conditionals](TheAccumulatorPatternwithConditionals.html){.reference
        .internal}
    -   [8.11 👩‍💻 Setting Up
        Conditionals](WPSettingUpConditionals.html){.reference
        .internal}
    -   [8.12 Glossary](Glossary.html){.reference .internal}
    -   [8.13 Exercises](Exercises.html){.reference .internal}
    -   [8.14 Chapter Assessment](week3a1.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#conditional-execution-binary-selection .section}
[]{#index-0}

[8.6. ]{.section-number}Conditional Execution: Binary Selection[¶](#conditional-execution-binary-selection "Permalink to this heading"){.headerlink}
====================================================================================================================================================

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#binaryselection .align-left .youtube-video component="youtube" video-height="315" question_label="8.6.1" video-width="560" video-videoid="OQ8uakCJ6yE" video-divid="binaryselection" video-start="0" video-end="-1"}
:::
:::

In order to write useful programs, we almost always need the ability to
check conditions and change the behavior of the program accordingly.
**Selection statements**, sometimes also referred to as **conditional
statements**, give us this ability. The simplest form of selection is
the **if statement**. This is sometimes referred to as **binary
selection** since there are two possible paths of execution.

::: {.runestone .explainer .ac_section}
::: {#ac7_6_1 component="activecode" question_label="8.6.2"}
::: {#ac7_6_1_question .ac_question}
:::
:::
:::

The syntax for an `if`{.docutils .literal .notranslate} statement looks
like this:

::: {.highlight-python .notranslate}
::: {.highlight}
    if BOOLEAN EXPRESSION:
        STATEMENTS_1        # executed if condition evaluates to True
    else:
        STATEMENTS_2        # executed if condition evaluates to False
:::
:::

The boolean expression after the `if`{.docutils .literal .notranslate}
statement is called the **condition**. If it is true, then the indented
statements get executed. If not, then the statements indented under the
`else`{.docutils .literal .notranslate} clause get executed.

Flowchart of a **if** statement with an **else**

![](../_images/flowchart_if_else.png)

As with the function definition from the last chapter and other compound
statements like `for`{.docutils .literal .notranslate}, the
`if`{.docutils .literal .notranslate} statement consists of a header
line and a body. The header line begins with the keyword `if`{.docutils
.literal .notranslate} followed by a *boolean expression* and ends with
a colon (:).

The indented statements that follow are called a **block**. The first
unindented statement marks the end of the block.

Each of the statements inside the first block of statements is executed
in order if the boolean expression evaluates to `True`{.docutils
.literal .notranslate}. The entire first block of statements is skipped
if the boolean expression evaluates to `False`{.docutils .literal
.notranslate}, and instead all the statements under the `else`{.docutils
.literal .notranslate} clause are executed.

There is no limit on the number of statements that can appear under the
two clauses of an `if`{.docutils .literal .notranslate} statement, but
there has to be at least one statement in each block.

**Check your understanding**

::: {.runestone}
-   [Just one.]{#question7_6_1_opt_a}
-   Each block may also contain more than one.
-   [Zero or more.]{#question7_6_1_opt_b}
-   Each block must contain at least one statement.
-   [One or more.]{#question7_6_1_opt_c}
-   Yes, a block must contain at least one statement and can have many
    statements.
-   [One or more, and each must contain the same
    number.]{#question7_6_1_opt_d}
-   The blocks may contain different numbers of statements.
:::

::: {.runestone}
-   [TRUE]{#question7_6_2_opt_a}
-   TRUE is printed by the if-block, which only executes if the
    conditional (in this case, 4+5 == 10) is true. In this case 5+4 is
    not equal to 10.
-   [FALSE]{#question7_6_2_opt_b}
-   Since 4+5==10 evaluates to False, Python will skip over the if block
    and execute the statement in the else block.
-   [TRUE on one line and FALSE on the next]{#question7_6_2_opt_c}
-   Python would never print both TRUE and FALSE because it will only
    execute one of the if-block or the else-block, but not both.
-   [Nothing will be printed]{#question7_6_2_opt_d}
-   Python will always execute either the if-block (if the condition is
    true) or the else-block (if the condition is false). It would never
    skip over both blocks.
:::

::: {.runestone}
-   [Output a]{#question7_6_3_opt_a}
-   Although TRUE is printed after the if-else statement completes, both
    blocks within the if-else statement print something too. In this
    case, Python would have had to have skipped both blocks in the
    if-else statement, which it never would do.
-   [Output b]{#question7_6_3_opt_b}
-   Because there is a TRUE printed after the if-else statement ends,
    Python will always print TRUE as the last statement.
-   [Output c]{#question7_6_3_opt_c}
-   Python will print FALSE from within the else-block (because 5+4 does
    not equal 10), and then print TRUE after the if-else statement
    completes.
-   [Output d]{#question7_6_3_opt_d}
-   To print these three lines, Python would have to execute both blocks
    in the if-else statement, which it can never do.
:::

::: {.runestone .explainer .ac_section}
::: {#ac7_6_2 component="activecode" question_label="8.6.6"}
::: {#ac7_6_2_question .ac_question}
Write code to assign the string `"You can apply to SI!"`{.docutils
.literal .notranslate} to `output`{.docutils .literal .notranslate} *if*
the string `"SI 106"`{.docutils .literal .notranslate} is in the list
`courses`{.docutils .literal .notranslate}. If it is not in
`courses`{.docutils .literal .notranslate}, assign the value
`"Take SI 106!"`{.docutils .literal .notranslate} to the variable
`output`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac7_6_4 component="activecode" question_label="8.6.7"}
::: {#ac7_6_4_question .ac_question}
Create a variable, `b`{.docutils .literal .notranslate}, and assign it
the value of `15`{.docutils .literal .notranslate}. Then, write code to
see if the value `b`{.docutils .literal .notranslate} is greater than
that of `a`{.docutils .literal .notranslate}. If it is, `a`{.docutils
.literal .notranslate}'s value should be multiplied by 2. If the value
of `b`{.docutils .literal .notranslate} is less than or equal to
`a`{.docutils .literal .notranslate}, nothing should happen. Finally,
create variable `c`{.docutils .literal .notranslate} and assign it the
value of the sum of `a`{.docutils .literal .notranslate} and
`b`{.docutils .literal .notranslate}.
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

-   [[](PrecedenceofOperators.html)]{#relations-prev}
-   [[](OmittingtheelseClauseUnarySelection.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
