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
        Problem](/runestone/default/reportabug?course=fopp&page=BooleanValuesandBooleanExpressions)
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
::: {#boolean-values-and-boolean-expressions .section}
[]{#index-0}

[8.2. ]{.section-number}Boolean Values and Boolean Expressions[¶](#boolean-values-and-boolean-expressions "Permalink to this heading"){.headerlink}
===================================================================================================================================================

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#booleanexpressions .align-left .youtube-video component="youtube" video-height="315" question_label="8.2.1" video-width="560" video-videoid="Y6CwThhquQs" video-divid="booleanexpressions" video-start="0" video-end="-1"}
:::
:::

The Python type for storing true and false values is called
`bool`{.docutils .literal .notranslate}, named after the British
mathematician, George Boole. George Boole created *Boolean Algebra*,
which is the basis of all modern computer arithmetic.

There are only two **boolean values**. They are `True`{.docutils
.literal .notranslate} and `False`{.docutils .literal .notranslate}.
Capitalization is important, since `true`{.docutils .literal
.notranslate} and `false`{.docutils .literal .notranslate} are not
boolean values (remember Python is case sensitive).

::: {.runestone .explainer .ac_section}
::: {#ac7_2_1 component="activecode" question_label="8.2.2"}
::: {#ac7_2_1_question .ac_question}
:::
:::
:::

::: {.admonition .note}
Note

Boolean values are not strings!

It is extremely important to realize that True and False are not
strings. They are not surrounded by quotes. They are the only two values
in the data type `bool`{.docutils .literal .notranslate}. Take a close
look at the types shown below.
:::

::: {.runestone .explainer .ac_section}
::: {#ac7_2_2 component="activecode" question_label="8.2.3"}
::: {#ac7_2_2_question .ac_question}
:::
:::
:::

A **boolean expression** is an expression that evaluates to a boolean
value. The equality operator, `==`{.docutils .literal .notranslate},
compares two values and produces a boolean value related to whether the
two values are equal to one another.

::: {.runestone .explainer .ac_section}
::: {#ac7_2_3 component="activecode" question_label="8.2.4"}
::: {#ac7_2_3_question .ac_question}
:::
:::
:::

In the first statement, the two operands are equal, so the expression
evaluates to `True`{.docutils .literal .notranslate}. In the second
statement, 5 is not equal to 6, so we get `False`{.docutils .literal
.notranslate}.

The `==`{.docutils .literal .notranslate} operator is one of six common
**comparison operators**; the others are:

::: {.highlight-python .notranslate}
::: {.highlight}
    x != y               # x is not equal to y
    x > y                # x is greater than y
    x < y                # x is less than y
    x >= y               # x is greater than or equal to y
    x <= y               # x is less than or equal to y
:::
:::

Although these operations are probably familiar to you, the Python
symbols are different from the mathematical symbols. A common error is
to use a single equal sign (`=`{.docutils .literal .notranslate})
instead of a double equal sign (`==`{.docutils .literal .notranslate}).
Remember that `=`{.docutils .literal .notranslate} is an assignment
operator and `==`{.docutils .literal .notranslate} is a comparison
operator. Also, there is no such thing as `=<`{.docutils .literal
.notranslate} or `=>`{.docutils .literal .notranslate}.

Note too that an equality test is symmetric, but assignment is not. For
example, if `a == 7`{.docutils .literal .notranslate} then
`7 == a`{.docutils .literal .notranslate}. But in Python, the statement
`a = 7`{.docutils .literal .notranslate} is legal and `7 = a`{.docutils
.literal .notranslate} is not. (Can you explain why?)

**Check your understanding**

::: {.runestone}
-   [True]{#question7_2_1_opt_a}
-   True and False are both Boolean literals.
-   [3 == 4]{#question7_2_1_opt_b}
-   The comparison between two numbers via == results in either True or
    False (in this case False), both Boolean values.
-   [3 + 4]{#question7_2_1_opt_c}
-   3+4 evaluates to 7, which is a number, not a Boolean value.
-   [3 + 4 == 7]{#question7_2_1_opt_d}
-   3+4 evaluates to 7. 7 == 7 then evaluates to True, which is a
    Boolean value.
-   [\"False\"]{#question7_2_1_opt_e}
-   With the double quotes surrounding it, False is interpreted as a
    string, not a Boolean value. If the quotes had not been included,
    False alone is in fact a Boolean value.
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

-   [[](intro-TurtlesandConditionals.html)]{#relations-prev}
-   [[](Logicaloperators.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
