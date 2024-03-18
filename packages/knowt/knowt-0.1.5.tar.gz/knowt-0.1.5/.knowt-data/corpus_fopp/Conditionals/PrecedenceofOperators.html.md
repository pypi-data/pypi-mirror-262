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
        Problem](/runestone/default/reportabug?course=fopp&page=PrecedenceofOperators)
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
::: {#precedence-of-operators .section}
[]{#index-0}

[8.5. ]{.section-number}Precedence of Operators[¶](#precedence-of-operators "Permalink to this heading"){.headerlink}
=====================================================================================================================

Arithmetic operators take precedence over logical operators. Python will
always evaluate the arithmetic operators first (\*\* is highest, then
multiplication/division, then addition/subtraction). Next comes the
relational operators. Finally, the logical operators are done last. This
means that the expression `x*5 >= 10 and y-6 <= 20`{.docutils .literal
.notranslate} will be evaluated so as to first perform the arithmetic
and then check the relationships. The `and`{.docutils .literal
.notranslate} will be done last. Many programmers might place
parentheses around the two relational expressions,
`(x*5 >= 10) and (y-6 <= 20)`{.docutils .literal .notranslate}. It is
not necessary to do so, but causes no harm and may make it easier for
people to read and understand the code.

The following table summarizes the operator precedence from highest to
lowest. A complete table for the entire language can be found in the
[Python
Documentation](http://docs.python.org/py3k/reference/expressions.html#expression-lists){.reference
.external}.

  Level     Category         Operators
  --------- ---------------- ---------------------
  7(high)   exponent         \*\*
  6         multiplication   \*,/,//,%
  5         addition         +,-
  4         relational       ==,!=,\<=,\>=,\>,\<
  3         logical          not
  2         logical          and
  1(low)    logical          or

::: {.admonition .note}
Note

This workspace is provided for your convenience. You can use this
activecode window to try out anything you like.

::: {.runestone .explainer .ac_section}
::: {#ac7_5_1 component="activecode" question_label="8.5.1"}
::: {#ac7_5_1_question .ac_question}
:::
:::
:::
:::

::: {.admonition-common-mistake .admonition}
Common Mistake!

Students often incorrectly combine the in and or operators. For example,
if they want to check that the letter x is inside of either of two
variables then they tend to write it the following way:
`'x' in y or z`{.docutils .literal .notranslate}

Written this way, the code would not always do what the programmer
intended. This is because the `in`{.docutils .literal .notranslate}
operator is only on the left side of the or statement. It doesn't get
implemented on both sides of the or statement. In order to properly
check that x is inside of either variable, the in operator must be used
on both sides which looks like this:

::: {.highlight-python .notranslate}
::: {.highlight}
    'x' in y or 'x' in z
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [((5\*3) \> 10) and ((4+6) == 11)]{#question7_5_1_opt_a}
-   Yes, \* and + have higher precedence, followed by \> and ==, and
    then the keyword \"and\"
-   [(5\*(3 \> 10)) and (4 + (6 == 11))]{#question7_5_1_opt_b}
-   Arithmetic operators (\*, +) have higher precedence than comparison
    operators (\>, ==)
-   [((((5\*3) \> 10) and 4)+6) == 11]{#question7_5_1_opt_c}
-   This grouping assumes Python simply evaluates from left to right,
    which is incorrect. It follows the precedence listed in the table in
    this section.
-   [((5\*3) \> (10 and (4+6))) == 11]{#question7_5_1_opt_d}
-   This grouping assumes that \"and\" has a higher precedence than ==,
    which is not true.
:::

Here is an animation for the above expression:

::: {#se_ac7_5_1 .runestone .explainer component="showeval" question_label="8.5.3" tracemode="true"}
Next Step

Reset

::: {.evalCont style="background-color: #FDFDFD;"}
5 \* 3 \> 10 and 4 + 6 == 11\
:::

::: {.evalCont}
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

-   [[](Theinandnotinoperators.html)]{#relations-prev}
-   [[](ConditionalExecutionBinarySelection.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
