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
        Problem](/runestone/default/reportabug?course=fopp&page=Chainedconditionals)
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
::: {#chained-conditionals .section}
[]{#index-0}

[8.9. ]{.section-number}Chained conditionals[¶](#chained-conditionals "Permalink to this heading"){.headerlink}
===============================================================================================================

Python provides an alternative way to write nested selection such as the
one shown in the previous section. This is sometimes referred to as a
**chained conditional**.

::: {.highlight-python .notranslate}
::: {.highlight}
    if x < y:
        print("x is less than y")
    elif x > y:
        print("x is greater than y")
    else:
        print("x and y must be equal")
:::
:::

The flow of control can be drawn in a different orientation but the
resulting pattern is identical to the one shown above.

![](../_images/flowchart_chained_conditional.png)

`elif`{.docutils .literal .notranslate} is an abbreviation of
`else if`{.docutils .literal .notranslate}. Again, exactly one branch
will be executed. There is no limit of the number of `elif`{.docutils
.literal .notranslate} statements but only a single (and optional) final
`else`{.docutils .literal .notranslate} statement is allowed and it must
be the last branch in the statement.

![](../_images/conditionals_overview.png)

Each condition is checked in order. If the first is false, the next is
checked, and so on. If one of them is true, the corresponding branch
executes, and the statement ends. Even if more than one condition is
true, only the first true branch executes.

Here is the same program using `elif`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#ac7_9_1 component="activecode" question_label="8.9.1"}
::: {#ac7_9_1_question .ac_question}
:::
:::
:::

The following image highlights different kinds of valid conditionals
that can be used. Though there are other versions of conditionals that
Python can understand (imagine an if statement with twenty elif
statements), those other versions must follow the same order as seen
below.

![shows a unary conditiona, a binary conditional, a conditional with if,
elif, else, and a conditional with if, elif, and
elif.](../_images/valid_conditionals.png)

**Check your understanding**

::: {.runestone}
-   [I only]{#question7_9_1_opt_a}
-   You can not use a Boolean expression after an else.
-   [II only]{#question7_9_1_opt_b}
-   Yes, II will give the same result.
-   [III only]{#question7_9_1_opt_c}
-   No, III will not give the same result. The first if statement will
    be true, but the second will be false, so the else part will
    execute.
-   [II and III]{#question7_9_1_opt_d}
-   No, Although II is correct III will not give the same result. Try
    it.
-   [I, II, and III]{#question7_9_1_opt_e}
-   No, in I you can not have a Boolean expression after an else.
:::

::: {.runestone}
-   [a]{#question7_9_2_opt_a}
-   While the value in x is less than the value in y (3 is less than 5)
    it is not less than the value in z (3 is not less than 2).
-   [b]{#question7_9_2_opt_b}
-   The value in y is not less than the value in x (5 is not less than
    3).
-   [c]{#question7_9_2_opt_c}
-   Since the first two Boolean expressions are false the else will be
    executed.
:::

::: {.runestone .explainer .ac_section}
::: {#ac7_9_2 component="activecode" question_label="8.9.4"}
::: {#ac7_9_2_question .ac_question}
Create one conditional to find whether "false" is in string
`str1`{.docutils .literal .notranslate}. If so, assign variable
`output`{.docutils .literal .notranslate} the string "False. You aren't
you?". Check to see if "true" is in string `str1`{.docutils .literal
.notranslate} and if it is then assign "True! You are you!" to the
variable `output`{.docutils .literal .notranslate}. If neither are in
`str1`{.docutils .literal .notranslate}, assign "Neither true nor
false!" to `output`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac7_9_4 component="activecode" question_label="8.9.5"}
::: {#ac7_9_4_question .ac_question}
Create an empty list called `resps`{.docutils .literal .notranslate}.
Using the list `percent_rain`{.docutils .literal .notranslate}, for each
percent, if it is above 90, add the string 'Bring an umbrella.' to
`resps`{.docutils .literal .notranslate}, otherwise if it is above 80,
add the string 'Good for the flowers?' to `resps`{.docutils .literal
.notranslate}, otherwise if it is above 50, add the string 'Watch out
for clouds!' to `resps`{.docutils .literal .notranslate}, otherwise, add
the string 'Nice day!' to `resps`{.docutils .literal .notranslate}.
Note: if you're sure you've got the problem right but it doesn't pass,
then check that you've matched up the strings exactly.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac7_9_5 component="activecode" question_label="8.9.6"}
::: {#ac7_9_5_question .ac_question}
We have created conditionals for you to use. Do not change the provided
conditional statements. Find an integer value for `x`{.docutils .literal
.notranslate} that will cause `output`{.docutils .literal .notranslate}
to hold the values `True`{.docutils .literal .notranslate} and
`None`{.docutils .literal .notranslate}. (Drawing diagrams or flow
charts for yourself may help!)
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

-   [[](Nestedconditionals.html)]{#relations-prev}
-   [[](TheAccumulatorPatternwithConditionals.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
